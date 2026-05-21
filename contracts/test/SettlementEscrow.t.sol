// SPDX-License-Identifier: Apache-2.0
pragma solidity ^0.8.26;

import {Test} from "forge-std/Test.sol";
import {Attestation} from "@eas/Common.sol";

import {MockUSDC} from "../src/MockUSDC.sol";
import {SettlementEscrow} from "../src/SettlementEscrow.sol";
import {MockEAS} from "./MockEAS.sol";

contract SettlementEscrowTest is Test {
    SettlementEscrow internal escrow;
    MockUSDC internal usdc;
    MockEAS internal eas;

    bytes32 internal constant SCHEMA = keccak256("AttestRWA.SettlementApproval.v1");

    address internal owner = address(0xC0FFEE);
    address internal attester = address(0xA77E57E2);
    address internal buyer = address(0xB0B);
    address internal payee = address(0xDEAD);
    address internal stranger = address(0x57A);

    uint256 internal constant DEFAULT_AMOUNT = 580 * 1e6; // 580 USDC
    uint64 internal constant ONE_DAY = 1 days;

    function setUp() public {
        eas = new MockEAS();
        vm.prank(owner);
        escrow = new SettlementEscrow(address(eas), SCHEMA, owner);
        usdc = new MockUSDC();

        vm.prank(owner);
        escrow.setAttester(attester, true);

        usdc.mint(buyer, 10_000 * 1e6);
        vm.prank(buyer);
        usdc.approve(address(escrow), type(uint256).max);
    }

    // ---- constructor ----

    function test_constructor_reverts_on_zero_eas() public {
        vm.expectRevert(SettlementEscrow.InvalidEasAddress.selector);
        new SettlementEscrow(address(0), SCHEMA, owner);
    }

    function test_constructor_reverts_on_zero_schema() public {
        vm.expectRevert(SettlementEscrow.InvalidSchema.selector);
        new SettlementEscrow(address(eas), bytes32(0), owner);
    }

    function test_constructor_records_inputs() public view {
        assertEq(address(escrow.eas()), address(eas));
        assertEq(escrow.schemaUid(), SCHEMA);
        assertEq(escrow.owner(), owner);
    }

    // ---- admin ----

    function test_setAttester_only_owner() public {
        vm.prank(stranger);
        vm.expectRevert();
        escrow.setAttester(stranger, true);
    }

    function test_setAttester_toggles_and_emits() public {
        vm.prank(owner);
        vm.expectEmit(true, false, false, true, address(escrow));
        emit SettlementEscrow.AttesterTrustChanged(stranger, true);
        escrow.setAttester(stranger, true);
        assertTrue(escrow.trustedAttesters(stranger));
    }

    // ---- deposit ----

    function test_deposit_happy_path() public {
        bytes32 dealId = keccak256("deal-1");
        uint64 deadline = uint64(block.timestamp + ONE_DAY);

        vm.prank(buyer);
        vm.expectEmit(true, true, true, true, address(escrow));
        emit SettlementEscrow.Deposited(dealId, buyer, payee, address(usdc), DEFAULT_AMOUNT, deadline);
        escrow.deposit(dealId, payee, address(usdc), DEFAULT_AMOUNT, deadline);

        SettlementEscrow.Deal memory d = escrow.getDeal(dealId);
        assertEq(d.buyer, buyer);
        assertEq(d.payee, payee);
        assertEq(d.amount, DEFAULT_AMOUNT);
        assertEq(usdc.balanceOf(address(escrow)), DEFAULT_AMOUNT);
    }

    function test_deposit_rejects_zero_dealId() public {
        vm.prank(buyer);
        vm.expectRevert(SettlementEscrow.DealNotFound.selector);
        escrow.deposit(bytes32(0), payee, address(usdc), DEFAULT_AMOUNT, uint64(block.timestamp + ONE_DAY));
    }

    function test_deposit_rejects_zero_payee() public {
        vm.prank(buyer);
        vm.expectRevert(SettlementEscrow.PayeeZero.selector);
        escrow.deposit(
            keccak256("d"), address(0), address(usdc), DEFAULT_AMOUNT, uint64(block.timestamp + ONE_DAY)
        );
    }

    function test_deposit_rejects_zero_token() public {
        vm.prank(buyer);
        vm.expectRevert(SettlementEscrow.TokenZero.selector);
        escrow.deposit(
            keccak256("d"), payee, address(0), DEFAULT_AMOUNT, uint64(block.timestamp + ONE_DAY)
        );
    }

    function test_deposit_rejects_zero_amount() public {
        vm.prank(buyer);
        vm.expectRevert(SettlementEscrow.AmountZero.selector);
        escrow.deposit(keccak256("d"), payee, address(usdc), 0, uint64(block.timestamp + ONE_DAY));
    }

    function test_deposit_rejects_dust_amount() public {
        vm.prank(buyer);
        vm.expectRevert(SettlementEscrow.AmountTooSmall.selector);
        escrow.deposit(keccak256("d"), payee, address(usdc), 1, uint64(block.timestamp + ONE_DAY));
    }

    function test_deposit_rejects_past_deadline() public {
        vm.warp(1000);
        vm.prank(buyer);
        vm.expectRevert(SettlementEscrow.InvalidDeadline.selector);
        escrow.deposit(keccak256("d"), payee, address(usdc), DEFAULT_AMOUNT, uint64(999));
    }

    function test_deposit_rejects_duplicate_dealId() public {
        bytes32 dealId = keccak256("d-dup");
        uint64 deadline = uint64(block.timestamp + ONE_DAY);
        vm.startPrank(buyer);
        escrow.deposit(dealId, payee, address(usdc), DEFAULT_AMOUNT, deadline);
        vm.expectRevert(SettlementEscrow.DealAlreadyExists.selector);
        escrow.deposit(dealId, payee, address(usdc), DEFAULT_AMOUNT, deadline);
        vm.stopPrank();
    }

    // ---- release happy ----

    function test_release_happy_transfers_to_payee() public {
        bytes32 dealId = keccak256("deal-happy");
        uint64 deadline = uint64(block.timestamp + ONE_DAY);
        _doDeposit(dealId, deadline);

        bytes32 attUid = _seedAttestation(
            dealId,
            attester,
            payee,
            address(usdc),
            DEFAULT_AMOUNT,
            0, // green
            true, // payeeVerified
            uint64(block.timestamp + ONE_DAY),
            0 // not revoked
        );

        vm.expectEmit(true, true, false, true, address(escrow));
        emit SettlementEscrow.SettlementReleased(dealId, payee, DEFAULT_AMOUNT, attUid);
        escrow.release(dealId, attUid);

        assertEq(usdc.balanceOf(payee), DEFAULT_AMOUNT);
        assertEq(usdc.balanceOf(address(escrow)), 0);
        SettlementEscrow.Deal memory d = escrow.getDeal(dealId);
        assertTrue(d.released);
    }

    // ---- release reject paths ----

    function test_release_reverts_on_wrong_schema() public {
        bytes32 dealId = keccak256("d");
        uint64 deadline = uint64(block.timestamp + ONE_DAY);
        _doDeposit(dealId, deadline);

        bytes32 attUid = keccak256("bad-schema");
        eas.setAttestation(
            attUid,
            Attestation({
                uid: attUid,
                schema: keccak256("WRONG_SCHEMA"),
                time: uint64(block.timestamp),
                expirationTime: uint64(block.timestamp + ONE_DAY),
                revocationTime: 0,
                refUID: bytes32(0),
                recipient: address(0),
                attester: attester,
                revocable: true,
                data: _encodeData(dealId, attester, payee, address(usdc), DEFAULT_AMOUNT, 0, true, deadline)
            })
        );

        vm.expectRevert(SettlementEscrow.AttestationWrongSchema.selector);
        escrow.release(dealId, attUid);
    }

    function test_release_reverts_on_revoked_attestation() public {
        bytes32 dealId = keccak256("d");
        uint64 deadline = uint64(block.timestamp + ONE_DAY);
        _doDeposit(dealId, deadline);

        bytes32 attUid = _seedAttestation(
            dealId, attester, payee, address(usdc), DEFAULT_AMOUNT, 0, true, deadline, uint64(block.timestamp)
        );

        vm.expectRevert(SettlementEscrow.AttestationRevoked.selector);
        escrow.release(dealId, attUid);
    }

    function test_release_reverts_on_expired_attestation() public {
        vm.warp(1_000_000);
        bytes32 dealId = keccak256("d");
        uint64 deadline = uint64(block.timestamp + ONE_DAY);
        _doDeposit(dealId, deadline);

        bytes32 attUid = _seedAttestation(
            dealId, attester, payee, address(usdc), DEFAULT_AMOUNT, 0, true, uint64(block.timestamp - 1), 0
        );

        vm.expectRevert(SettlementEscrow.AttestationExpired.selector);
        escrow.release(dealId, attUid);
    }

    function test_release_reverts_on_untrusted_attester() public {
        bytes32 dealId = keccak256("d");
        uint64 deadline = uint64(block.timestamp + ONE_DAY);
        _doDeposit(dealId, deadline);

        address rogue = address(0xFADED);
        bytes32 attUid = _seedAttestation(
            dealId, rogue, payee, address(usdc), DEFAULT_AMOUNT, 0, true, deadline, 0
        );

        vm.expectRevert(SettlementEscrow.AttesterNotTrusted.selector);
        escrow.release(dealId, attUid);
    }

    function test_release_reverts_on_payee_mismatch() public {
        bytes32 dealId = keccak256("d");
        uint64 deadline = uint64(block.timestamp + ONE_DAY);
        _doDeposit(dealId, deadline);

        address impostor = address(0xBADA55);
        bytes32 attUid = _seedAttestation(
            dealId, attester, impostor, address(usdc), DEFAULT_AMOUNT, 0, true, deadline, 0
        );

        vm.expectRevert(SettlementEscrow.AttestationPayeeMismatch.selector);
        escrow.release(dealId, attUid);
    }

    function test_release_reverts_on_capital_red() public {
        bytes32 dealId = keccak256("d");
        uint64 deadline = uint64(block.timestamp + ONE_DAY);
        _doDeposit(dealId, deadline);

        bytes32 attUid = _seedAttestation(
            dealId, attester, payee, address(usdc), DEFAULT_AMOUNT, 2, true, deadline, 0
        );

        vm.expectRevert(SettlementEscrow.CapitalClassRed.selector);
        escrow.release(dealId, attUid);
    }

    function test_release_reverts_on_payee_not_verified() public {
        bytes32 dealId = keccak256("d");
        uint64 deadline = uint64(block.timestamp + ONE_DAY);
        _doDeposit(dealId, deadline);

        bytes32 attUid = _seedAttestation(
            dealId, attester, payee, address(usdc), DEFAULT_AMOUNT, 0, false, deadline, 0
        );

        vm.expectRevert(SettlementEscrow.PayeeNotVerified.selector);
        escrow.release(dealId, attUid);
    }

    function test_release_reverts_on_replay_across_deals() public {
        bytes32 dealA = keccak256("deal-A");
        bytes32 dealB = keccak256("deal-B");
        uint64 deadline = uint64(block.timestamp + ONE_DAY);

        _doDeposit(dealA, deadline);
        _doDeposit(dealB, deadline);

        bytes32 attUidForA = _seedAttestation(
            dealA, attester, payee, address(usdc), DEFAULT_AMOUNT, 0, true, deadline, 0
        );

        vm.expectRevert(SettlementEscrow.AttestationDealMismatch.selector);
        escrow.release(dealB, attUidForA);
    }

    function test_release_twice_reverts() public {
        bytes32 dealId = keccak256("dup-release");
        uint64 deadline = uint64(block.timestamp + ONE_DAY);
        _doDeposit(dealId, deadline);

        bytes32 attUid = _seedAttestation(
            dealId, attester, payee, address(usdc), DEFAULT_AMOUNT, 0, true, deadline, 0
        );
        escrow.release(dealId, attUid);

        vm.expectRevert(SettlementEscrow.DealAlreadyReleased.selector);
        escrow.release(dealId, attUid);
    }

    // ---- refund ----

    function test_refund_after_deadline_no_attestation() public {
        bytes32 dealId = keccak256("d-refund-time");
        uint64 deadline = uint64(block.timestamp + ONE_DAY);
        _doDeposit(dealId, deadline);

        vm.warp(deadline + 1);
        vm.prank(buyer);
        escrow.refund(dealId, bytes32(0));

        assertEq(usdc.balanceOf(buyer), 10_000 * 1e6);
        SettlementEscrow.Deal memory d = escrow.getDeal(dealId);
        assertTrue(d.refunded);
    }

    function test_refund_reverts_before_deadline_no_attestation() public {
        bytes32 dealId = keccak256("d-too-early");
        uint64 deadline = uint64(block.timestamp + ONE_DAY);
        _doDeposit(dealId, deadline);

        vm.prank(buyer);
        vm.expectRevert(SettlementEscrow.DeadlineNotReached.selector);
        escrow.refund(dealId, bytes32(0));
    }

    function test_refund_with_payee_not_verified_attestation() public {
        bytes32 dealId = keccak256("d-payee-bad");
        uint64 deadline = uint64(block.timestamp + ONE_DAY);
        _doDeposit(dealId, deadline);

        bytes32 attUid = _seedAttestation(
            dealId, attester, payee, address(usdc), DEFAULT_AMOUNT, 0, false, deadline, 0
        );

        vm.prank(buyer);
        escrow.refund(dealId, attUid);
        assertEq(usdc.balanceOf(buyer), 10_000 * 1e6);
    }

    function test_refund_with_capital_red_attestation() public {
        bytes32 dealId = keccak256("d-capred");
        uint64 deadline = uint64(block.timestamp + ONE_DAY);
        _doDeposit(dealId, deadline);

        bytes32 attUid = _seedAttestation(
            dealId, attester, payee, address(usdc), DEFAULT_AMOUNT, 2, true, deadline, 0
        );

        vm.prank(buyer);
        escrow.refund(dealId, attUid);
        assertEq(usdc.balanceOf(buyer), 10_000 * 1e6);
    }

    function test_refund_only_buyer() public {
        bytes32 dealId = keccak256("d-only-buyer");
        uint64 deadline = uint64(block.timestamp + ONE_DAY);
        _doDeposit(dealId, deadline);
        vm.warp(deadline + 1);

        vm.prank(stranger);
        vm.expectRevert(SettlementEscrow.CallerNotBuyer.selector);
        escrow.refund(dealId, bytes32(0));
    }

    // ---- fuzz ----

    function testFuzz_deposit_amount_and_deadline(uint128 amount, uint32 deadlineDelta) public {
        amount = uint128(bound(uint256(amount), escrow.MIN_DEPOSIT(), uint256(type(uint96).max)));
        deadlineDelta = uint32(bound(uint256(deadlineDelta), 1, 365 days));

        usdc.mint(buyer, amount);
        vm.prank(buyer);
        usdc.approve(address(escrow), amount);

        bytes32 dealId = keccak256(abi.encode("fuzz", amount, deadlineDelta));
        uint64 deadline = uint64(block.timestamp + deadlineDelta);

        vm.prank(buyer);
        escrow.deposit(dealId, payee, address(usdc), amount, deadline);

        SettlementEscrow.Deal memory d = escrow.getDeal(dealId);
        assertEq(d.amount, amount);
        assertEq(d.deadline, deadline);
    }

    // ---- helpers ----

    function _doDeposit(bytes32 dealId, uint64 deadline) internal {
        vm.prank(buyer);
        escrow.deposit(dealId, payee, address(usdc), DEFAULT_AMOUNT, deadline);
    }

    function _seedAttestation(
        bytes32 dealId,
        address attesterAddr,
        address attPayee,
        address tokenAddr,
        uint256 amount,
        uint8 capitalClass,
        bool payeeVerified,
        uint64 expiresAt,
        uint64 revocationTime
    ) internal returns (bytes32 uid) {
        uid = keccak256(abi.encode(dealId, attesterAddr, expiresAt, capitalClass, payeeVerified, gasleft()));
        eas.setAttestation(
            uid,
            Attestation({
                uid: uid,
                schema: SCHEMA,
                time: uint64(block.timestamp),
                expirationTime: expiresAt,
                revocationTime: revocationTime,
                refUID: bytes32(0),
                recipient: address(0),
                attester: attesterAddr,
                revocable: true,
                data: _encodeData(
                    dealId, attesterAddr, attPayee, tokenAddr, amount, capitalClass, payeeVerified, expiresAt
                )
            })
        );
    }

    function _encodeData(
        bytes32 dealId,
        address attesterAddr,
        address attPayee,
        address tokenAddr,
        uint256 amount,
        uint8 capitalClass,
        bool payeeVerified,
        uint64 expiresAt
    ) internal pure returns (bytes memory) {
        return abi.encode(
            dealId,
            attesterAddr,
            attPayee,
            tokenAddr,
            amount,
            capitalClass,
            keccak256("evidence"),
            "TH",
            expiresAt,
            payeeVerified
        );
    }
}
