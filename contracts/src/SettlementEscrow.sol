// SPDX-License-Identifier: Apache-2.0
pragma solidity ^0.8.26;

import {IERC20} from "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import {SafeERC20} from "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";
import {ReentrancyGuard} from "@openzeppelin/contracts/utils/ReentrancyGuard.sol";
import {Ownable} from "@openzeppelin/contracts/access/Ownable.sol";

import {IEAS} from "@eas/IEAS.sol";
import {Attestation} from "@eas/Common.sol";

/// @title SettlementEscrow
/// @notice Programmable escrow for AttestRWA — Settlement Attestation Layer for RWA.
///         Holds stablecoin deposits and releases them only when a valid EAS
///         attestation from a trusted attester is on-chain and proves the deal
///         is bank-grade. On rejection or expiry, the buyer can refund.
/// @dev    The schema is pinned at deploy time. Trusted attesters are managed
///         by the contract owner. Attestation data layout is the canonical
///         AttestRWA SettlementApproval schema:
///
///         (bytes32 dealId, address attester, address payeeAddress,
///          address tokenAddress, uint256 amount, uint8 capitalClass,
///          bytes32 evidenceHash, string jurisdiction,
///          uint64 expiresAt, bool payeeVerified)
contract SettlementEscrow is ReentrancyGuard, Ownable {
    using SafeERC20 for IERC20;

    /// @notice State of a settlement deposit.
    /// @param buyer       Address that funded the escrow for this deal.
    /// @param payee       Address that the buyer expected to receive funds.
    /// @param token       ERC-20 token in custody.
    /// @param amount      Amount in token base units.
    /// @param deadline    Unix timestamp after which buyer can refund.
    /// @param released    True once the funds have been released to the payee.
    /// @param refunded    True once the funds have been refunded to the buyer.
    struct Deal {
        address buyer;
        address payee;
        address token;
        uint256 amount;
        uint64 deadline;
        bool released;
        bool refunded;
    }

    /// @notice EAS contract on the active chain (Base Sepolia canonical address).
    IEAS public immutable eas;

    /// @notice UID of the SettlementApproval schema; immutable to prevent
    ///         schema-impostor attacks.
    bytes32 public immutable schemaUid;

    /// @notice Minimum deposit, in token base units, to prevent dust DoS.
    uint256 public constant MIN_DEPOSIT = 1e6; // 1 USDC

    /// @notice Trusted attesters allowed to sign valid attestations.
    mapping(address attester => bool trusted) public trustedAttesters;

    /// @notice Active deals keyed by dealId.
    mapping(bytes32 dealId => Deal deal) public deals;

    // ---- Events --------------------------------------------------------

    /// @notice Emitted on a new deposit.
    event Deposited(
        bytes32 indexed dealId,
        address indexed buyer,
        address indexed payee,
        address token,
        uint256 amount,
        uint64 deadline
    );

    /// @notice Emitted when the escrow releases funds to the verified payee.
    event SettlementReleased(
        bytes32 indexed dealId,
        address indexed payee,
        uint256 amount,
        bytes32 attestationUid
    );

    /// @notice Emitted when the escrow refunds the buyer after rejection or expiry.
    event SettlementRefunded(
        bytes32 indexed dealId,
        address indexed buyer,
        uint256 amount,
        string reason
    );

    /// @notice Emitted when the owner toggles an attester.
    event AttesterTrustChanged(address indexed attester, bool trusted);

    // ---- Errors --------------------------------------------------------

    error InvalidEasAddress();
    error InvalidSchema();
    error InvalidDeadline();
    error AmountTooSmall();
    error AmountZero();
    error PayeeZero();
    error TokenZero();
    error DealAlreadyExists();
    error DealNotFound();
    error DealAlreadyReleased();
    error DealAlreadyRefunded();
    error AttestationWrongSchema();
    error AttestationRevoked();
    error AttestationExpired();
    error AttestationDealMismatch();
    error AttestationTokenMismatch();
    error AttestationPayeeMismatch();
    error AttestationAmountMismatch();
    error AttesterNotTrusted();
    error PayeeNotVerified();
    error CapitalClassRed();
    error DeadlineNotReached();
    error CallerNotBuyer();

    // ---- Constructor ---------------------------------------------------

    /// @notice Deploy the escrow.
    /// @param easAddress     Canonical EAS contract on this chain.
    /// @param settlementUid  UID of the SettlementApproval schema. Immutable.
    /// @param initialOwner   Initial admin who can adjust trusted attesters.
    constructor(address easAddress, bytes32 settlementUid, address initialOwner) Ownable(initialOwner) {
        if (easAddress == address(0)) revert InvalidEasAddress();
        if (settlementUid == bytes32(0)) revert InvalidSchema();
        eas = IEAS(easAddress);
        schemaUid = settlementUid;
    }

    // ---- Admin ---------------------------------------------------------

    /// @notice Toggle whether an attester is trusted. Owner-only.
    function setAttester(address attester, bool trusted) external onlyOwner {
        trustedAttesters[attester] = trusted;
        emit AttesterTrustChanged(attester, trusted);
    }

    // ---- Buyer flow ----------------------------------------------------

    /// @notice Deposit stablecoin under a `dealId`. Buyer pulls funds in via
    ///         a preceding ERC-20 approve.
    /// @param  dealId    Deterministic identifier of the deal.
    /// @param  payee     Expected recipient on the happy path.
    /// @param  token     ERC-20 token used for the deposit.
    /// @param  amount    Amount in token base units (>= MIN_DEPOSIT).
    /// @param  deadline  Unix timestamp by which release must occur; after
    ///                   this, buyer can refund unconditionally.
    function deposit(
        bytes32 dealId,
        address payee,
        address token,
        uint256 amount,
        uint64 deadline
    ) external nonReentrant {
        if (dealId == bytes32(0)) revert DealNotFound();
        if (payee == address(0)) revert PayeeZero();
        if (token == address(0)) revert TokenZero();
        if (amount == 0) revert AmountZero();
        if (amount < MIN_DEPOSIT) revert AmountTooSmall();
        if (deadline <= block.timestamp) revert InvalidDeadline();
        if (deals[dealId].amount != 0) revert DealAlreadyExists();

        deals[dealId] = Deal({
            buyer: msg.sender,
            payee: payee,
            token: token,
            amount: amount,
            deadline: deadline,
            released: false,
            refunded: false
        });

        IERC20(token).safeTransferFrom(msg.sender, address(this), amount);

        emit Deposited(dealId, msg.sender, payee, token, amount, deadline);
    }

    /// @notice Release escrowed funds to the payee using a valid attestation.
    /// @dev    Anyone can trigger; the protection is the attestation, not the caller.
    function release(bytes32 dealId, bytes32 attestationUid) external nonReentrant {
        Deal storage d = deals[dealId];
        if (d.amount == 0) revert DealNotFound();
        if (d.released) revert DealAlreadyReleased();
        if (d.refunded) revert DealAlreadyRefunded();

        Attestation memory a = eas.getAttestation(attestationUid);
        _checkAttestation(a, dealId, d);

        d.released = true;

        IERC20(d.token).safeTransfer(d.payee, d.amount);

        emit SettlementReleased(dealId, d.payee, d.amount, attestationUid);
    }

    /// @notice Refund buyer after expiry, or if the attester has explicitly
    ///         signed a rejection attestation (payeeVerified=false or
    ///         capitalClass=2).
    function refund(bytes32 dealId, bytes32 attestationUid) external nonReentrant {
        Deal storage d = deals[dealId];
        if (d.amount == 0) revert DealNotFound();
        if (d.released) revert DealAlreadyReleased();
        if (d.refunded) revert DealAlreadyRefunded();
        if (msg.sender != d.buyer) revert CallerNotBuyer();

        string memory reason;
        if (attestationUid == bytes32(0)) {
            if (uint64(block.timestamp) < d.deadline) revert DeadlineNotReached();
            reason = "deadline_reached_no_attestation";
        } else {
            Attestation memory a = eas.getAttestation(attestationUid);
            if (a.schema != schemaUid) revert AttestationWrongSchema();
            if (!trustedAttesters[a.attester]) revert AttesterNotTrusted();

            (
                bytes32 attDealId,
                ,
                ,
                ,
                ,
                uint8 capitalClass,
                ,
                ,
                ,
                bool payeeVerified
            ) = abi.decode(
                a.data,
                (bytes32, address, address, address, uint256, uint8, bytes32, string, uint64, bool)
            );

            if (attDealId != dealId) revert AttestationDealMismatch();

            if (capitalClass >= 2) {
                reason = "attester_signed_capital_red";
            } else if (!payeeVerified) {
                reason = "attester_signed_payee_not_verified";
            } else if (uint64(block.timestamp) >= d.deadline) {
                reason = "deadline_reached_valid_attestation";
            } else {
                revert DeadlineNotReached();
            }
        }

        d.refunded = true;

        IERC20(d.token).safeTransfer(d.buyer, d.amount);

        emit SettlementRefunded(dealId, d.buyer, d.amount, reason);
    }

    // ---- Views ---------------------------------------------------------

    /// @notice Returns a snapshot of the deal state.
    function getDeal(bytes32 dealId) external view returns (Deal memory) {
        return deals[dealId];
    }

    // ---- Internal ------------------------------------------------------

    /// @dev Verify all attestation requirements for release.
    function _checkAttestation(Attestation memory a, bytes32 dealId, Deal storage d) private view {
        if (a.schema != schemaUid) revert AttestationWrongSchema();
        if (a.revocationTime != 0) revert AttestationRevoked();
        if (a.expirationTime != 0 && a.expirationTime <= uint64(block.timestamp)) {
            revert AttestationExpired();
        }
        if (!trustedAttesters[a.attester]) revert AttesterNotTrusted();

        (
            bytes32 attDealId,
            ,
            address attPayee,
            address attToken,
            uint256 attAmount,
            uint8 capitalClass,
            ,
            ,
            ,
            bool payeeVerified
        ) = abi.decode(
            a.data,
            (bytes32, address, address, address, uint256, uint8, bytes32, string, uint64, bool)
        );

        if (attDealId != dealId) revert AttestationDealMismatch();
        if (attToken != d.token) revert AttestationTokenMismatch();
        if (attPayee != d.payee) revert AttestationPayeeMismatch();
        if (attAmount != d.amount) revert AttestationAmountMismatch();
        if (!payeeVerified) revert PayeeNotVerified();
        if (capitalClass >= 2) revert CapitalClassRed();
    }
}
