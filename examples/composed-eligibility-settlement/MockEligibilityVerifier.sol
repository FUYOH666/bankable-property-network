# SPDX-License-Identifier: Apache-2.0
pragma solidity ^0.8.26;

/// @notice Minimal eligibility gate — production: Shibui EASClaimVerifier.
interface IEligibilityVerifier {
    function isVerified(address wallet) external view returns (bool);
}

/// @dev Demo: returns true for any non-zero wallet.
contract MockEligibilityVerifier is IEligibilityVerifier {
    function isVerified(address wallet) external pure returns (bool) {
        return wallet != address(0);
    }
}

/// @notice Example composed gate for integrators (not deployed by default).
abstract contract ComposedSettlementGate {
    IEligibilityVerifier public immutable eligibility;

    constructor(IEligibilityVerifier eligibility_) {
        eligibility = eligibility_;
    }

    function _requireEligibleBuyer(address buyer) internal view {
        require(eligibility.isVerified(buyer), "BUYER_NOT_ELIGIBLE");
    }
}
