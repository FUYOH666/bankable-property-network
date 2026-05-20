# Property Settlement Policy Snippets

Data classification: synthetic demo data.

These snippets model the bank policy knowledge base used by the demo.

## Deposit Payee Authority

A booking deposit should not be released when the payment recipient differs from the represented seller or developer unless authority documentation is present.

Required evidence:
- seller or developer legal name;
- receiving entity legal name;
- written authorization to collect funds;
- bank account ownership evidence;
- buyer protection or refund clause.

## Capital Bankability

Green capital:
- bank transfer with clear source-of-funds evidence;
- regulated institution statement;
- consistent buyer identity.

Amber capital:
- stablecoin funds with explainable wallet history;
- foreign exchange route requiring review;
- partial source-of-funds evidence.

Red capital:
- cash-like P2P conversion;
- unclear counterparty;
- unsupported payment trail;
- mismatched source and buyer identity.

## Escrow Release

Escrow release should require:
- verified payee legal authority;
- approved settlement route;
- documented buyer capital classification;
- compliance officer approval;
- evidence pack hash retained for audit.
