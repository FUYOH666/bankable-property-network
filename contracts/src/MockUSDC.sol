// SPDX-License-Identifier: Apache-2.0
pragma solidity ^0.8.26;

import {ERC20} from "@openzeppelin/contracts/token/ERC20/ERC20.sol";

/// @title MockUSDC
/// @notice Minimal 6-decimal ERC-20 stand-in for USDC, used only on the dev
///         fork and Base Sepolia testnet. Anyone may mint any amount; this is
///         a demo asset and never should ship to mainnet.
/// @dev    Production replaces this with a real USDC address. The decimals
///         and ABI match the canonical USDC ERC-20 surface so the escrow
///         logic stays identical.
contract MockUSDC is ERC20 {
    /// @notice Emitted on every mint to make demo flows easy to follow.
    event MockMint(address indexed to, uint256 amount);

    /// @notice Construct the demo token.
    constructor() ERC20("Mock USDC (AttestRWA demo)", "mUSDC") {}

    /// @notice USDC uses 6 decimals; we mirror that so amount math matches.
    function decimals() public pure override returns (uint8) {
        return 6;
    }

    /// @notice Mint tokens to any address. Demo-only — never restrict, never
    ///         deploy on mainnet.
    /// @param to     Recipient of the mint.
    /// @param amount Amount in base units (10^6 = 1 USDC).
    function mint(address to, uint256 amount) external {
        _mint(to, amount);
        emit MockMint(to, amount);
    }
}
