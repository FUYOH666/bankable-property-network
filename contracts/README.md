# AttestRWA — Smart Contracts

> Foundry workspace. Will hold `SettlementEscrow.sol` and `MockUSDC.sol`
> starting Week 2 of the AttestRWA pivot.

## Status

Week 0: scaffold only (this README + empty `src/`, `test/`, `script/`).
Week 2: contracts, fuzz tests, invariants, slither audit, deploy script.

## Planned layout (Week 2)

```text
contracts/
├── README.md
├── foundry.toml
├── slither.config.json
├── remappings.txt
├── lib/                          # foundry-installed deps (eas, openzeppelin)
├── src/
│   ├── SettlementEscrow.sol      # main contract
│   └── MockUSDC.sol              # demo stablecoin (mint to anyone)
├── test/
│   ├── SettlementEscrow.t.sol    # unit + integration
│   └── invariants/
│       └── SettlementEscrow.invariants.t.sol
└── script/
    └── Deploy.s.sol              # deploy to Base Sepolia
```

## Dependencies (planned)

- [EAS Contracts](https://github.com/ethereum-attestation-service/eas-contracts) — `IEAS` interface
- [OpenZeppelin Contracts](https://github.com/OpenZeppelin/openzeppelin-contracts) — `ERC20`, `ReentrancyGuard`, `Ownable`
- [forge-std](https://github.com/foundry-rs/forge-std) — testing utilities

## Quick commands (after Week 2)

```bash
cd contracts
forge install              # install deps
forge build                # compile
forge test -vvv            # run all tests with stack traces
forge test --gas-report    # gas analysis
forge coverage             # coverage report
slither .                  # static analysis (zero high/medium target)

# deploy to Base Sepolia
forge script script/Deploy.s.sol --rpc-url https://sepolia.base.org --broadcast --verify
```

## Target metrics (Week 2 acceptance gate)

| Metric | Target |
|--------|--------|
| Foundry test coverage | ≥85% |
| Slither high findings | 0 |
| Slither medium findings | 0 |
| Gas: `release()` | <120k gas |
| Gas: `deposit()` | <90k gas |
| Fuzz runs per invariant | ≥10000 |
| BaseScan verification | green checkmark |
