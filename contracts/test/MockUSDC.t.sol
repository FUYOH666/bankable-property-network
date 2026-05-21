// SPDX-License-Identifier: Apache-2.0
pragma solidity ^0.8.26;

import {Test} from "forge-std/Test.sol";

import {MockUSDC} from "../src/MockUSDC.sol";

contract MockUSDCTest is Test {
    MockUSDC internal usdc;

    address internal alice = address(0xA11CE);
    address internal bob = address(0xB0B);

    function setUp() public {
        usdc = new MockUSDC();
    }

    function test_metadata() public view {
        assertEq(usdc.name(), "Mock USDC (AttestRWA demo)");
        assertEq(usdc.symbol(), "mUSDC");
        assertEq(usdc.decimals(), 6);
    }

    function test_mint_any_amount_to_any_address() public {
        usdc.mint(alice, 1_000_000_000);
        assertEq(usdc.balanceOf(alice), 1_000_000_000);
    }

    function test_transfer_works_after_mint() public {
        usdc.mint(alice, 500_000_000);
        vm.prank(alice);
        usdc.transfer(bob, 200_000_000);
        assertEq(usdc.balanceOf(alice), 300_000_000);
        assertEq(usdc.balanceOf(bob), 200_000_000);
    }

    function testFuzz_mint(address to, uint96 amount) public {
        vm.assume(to != address(0));
        usdc.mint(to, amount);
        assertEq(usdc.balanceOf(to), amount);
    }
}
