// SPDX-License-Identifier: Apache-2.0
pragma solidity ^0.8.26;

import {IEAS, AttestationRequest, MultiAttestationRequest, RevocationRequest, MultiRevocationRequest, DelegatedAttestationRequest, MultiDelegatedAttestationRequest, DelegatedRevocationRequest, MultiDelegatedRevocationRequest} from "@eas/IEAS.sol";
import {ISchemaRegistry} from "@eas/ISchemaRegistry.sol";
import {Attestation} from "@eas/Common.sol";

/// @title MockEAS
/// @notice Test-only stub of IEAS used by SettlementEscrow tests. We do not
///         exercise the real EAS verification surface here; we just let the
///         test author seed arbitrary Attestation records and have getAttestation
///         return them deterministically.
/// @dev    All non-getAttestation IEAS functions revert. The escrow contract
///         only reads attestations, so that is enough.
contract MockEAS is IEAS {
    /// @notice Schema registry stub (returned unused).
    ISchemaRegistry private immutable _registry;

    mapping(bytes32 uid => Attestation att) public attestations;

    constructor() {
        _registry = ISchemaRegistry(address(0));
    }

    function setAttestation(bytes32 uid, Attestation memory att) external {
        att.uid = uid;
        attestations[uid] = att;
    }

    function getAttestation(bytes32 uid) external view returns (Attestation memory) {
        return attestations[uid];
    }

    function getSchemaRegistry() external view returns (ISchemaRegistry) {
        return _registry;
    }

    // ---- IEAS surface we do not exercise ------------------------------------

    function attest(AttestationRequest calldata) external payable returns (bytes32) {
        revert("MockEAS: not implemented");
    }

    function attestByDelegation(DelegatedAttestationRequest calldata) external payable returns (bytes32) {
        revert("MockEAS: not implemented");
    }

    function multiAttest(MultiAttestationRequest[] calldata) external payable returns (bytes32[] memory) {
        revert("MockEAS: not implemented");
    }

    function multiAttestByDelegation(MultiDelegatedAttestationRequest[] calldata)
        external
        payable
        returns (bytes32[] memory)
    {
        revert("MockEAS: not implemented");
    }

    function revoke(RevocationRequest calldata) external payable {
        revert("MockEAS: not implemented");
    }

    function revokeByDelegation(DelegatedRevocationRequest calldata) external payable {
        revert("MockEAS: not implemented");
    }

    function multiRevoke(MultiRevocationRequest[] calldata) external payable {
        revert("MockEAS: not implemented");
    }

    function multiRevokeByDelegation(MultiDelegatedRevocationRequest[] calldata) external payable {
        revert("MockEAS: not implemented");
    }

    function timestamp(bytes32) external pure returns (uint64) {
        return 0;
    }

    function revokeOffchain(bytes32) external pure returns (uint64) {
        return 0;
    }

    function multiTimestamp(bytes32[] calldata) external pure returns (uint64) {
        return 0;
    }

    function multiRevokeOffchain(bytes32[] calldata) external pure returns (uint64) {
        return 0;
    }

    function isAttestationValid(bytes32 uid) external view returns (bool) {
        return attestations[uid].uid != bytes32(0);
    }

    function getTimestamp(bytes32) external pure returns (uint64) {
        return 0;
    }

    function getRevokeOffchain(address, bytes32) external pure returns (uint64) {
        return 0;
    }

    function version() external pure returns (string memory) {
        return "MockEAS/1.0";
    }
}
