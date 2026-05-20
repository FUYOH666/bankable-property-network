// SPDX-License-Identifier: Apache-2.0
pragma solidity ^0.8.26;

import {Script, console2} from "forge-std/Script.sol";

import {MockUSDC} from "../src/MockUSDC.sol";
import {SettlementEscrow} from "../src/SettlementEscrow.sol";

/// @title Deploy
/// @notice Deploys MockUSDC + SettlementEscrow + wires the attester whitelist.
///         Reads canonical Base Sepolia addresses from constants; reads the
///         schema UID and attester address from environment variables.
///
/// Required env vars:
///   - PRIVATE_KEY                : deployer (also receives MockUSDC initial supply)
///   - EAS_SCHEMA_UID_SETTLEMENT_APPROVAL : 0x1f64ec96... (or whichever UID is current)
///   - ATTESTER_ADDRESS           : trusted attester (Anvil acc 0 on dev fork)
///
/// Usage:
///   forge script script/Deploy.s.sol \
///       --rpc-url http://127.0.0.1:8545 \
///       --broadcast \
///       --skip-simulation
contract Deploy is Script {
    /// @notice Canonical EAS on Base mainnet, Base Sepolia, Optimism. Same
    ///         address inside the Anvil fork.
    address internal constant EAS_BASE = 0x4200000000000000000000000000000000000021;

    function run() external {
        uint256 deployerKey = vm.envUint("PRIVATE_KEY");
        address deployer = vm.addr(deployerKey);
        bytes32 schemaUid = vm.envBytes32("EAS_SCHEMA_UID_SETTLEMENT_APPROVAL");
        address attester = vm.envAddress("ATTESTER_ADDRESS");

        require(schemaUid != bytes32(0), "Deploy: schema uid is zero");
        require(attester != address(0), "Deploy: attester is zero");

        vm.startBroadcast(deployerKey);

        MockUSDC usdc = new MockUSDC();
        SettlementEscrow escrow = new SettlementEscrow(EAS_BASE, schemaUid, deployer);
        escrow.setAttester(attester, true);

        // Pre-mint a healthy demo bag to the deployer for fast booth testing
        usdc.mint(deployer, 1_000_000 * 1e6);

        vm.stopBroadcast();

        console2.log("===============================================");
        console2.log("AttestRWA deploy complete");
        console2.log("===============================================");
        console2.log("Network chainId :", block.chainid);
        console2.log("Deployer        :", deployer);
        console2.log("MockUSDC        :", address(usdc));
        console2.log("SettlementEscrow:", address(escrow));
        console2.log("EAS             :", EAS_BASE);
        console2.log("Schema UID      :");
        console2.logBytes32(schemaUid);
        console2.log("Trusted attester:", attester);
    }
}
