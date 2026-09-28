# 🛡️ Smart Contract Security Audit Portfolio

Welcome to my Smart Contract Security Audit Portfolio. This repository showcases my published security audit reports, vulnerability research, exploit Proof-of-Concepts (PoCs), and protocol security reviews across competitive audits (CodeHawks, Sherlock, Code4rena) and private engagements.

**Auditor:** Farhan Davin  
**Methodology:** The Tincho Method (8-Phase Phase-Driven Adversarial Review)  
**Standards:** Cyfrin / CodeHawks Severity Classification  

---

## 📑 Security Audit Reports

| Protocol | Date | Scope | Findings Summary | Report PDF | Report MD |
| :--- | :---: | :--- | :---: | :---: | :---: |
| **Vault Guardians** | Sep 2026 | `VaultGuardians.sol`, `VaultShares.sol`, Adapters (589 nSLOC) | **7 High, 4 Med, 2 Low, 1 Info** | [📄 Download PDF](./reports/VaultGuardians-Security-Audit-Report.pdf) | [📝 Read Markdown](./reports/VaultGuardians-Security-Audit-Report.md) |
| **Thunder Loan** | Sep 2026 | `ThunderLoan.sol`, `AssetToken.sol`, Oracle (475 nSLOC) | **7 High, 2 Med, 1 Low, 5 Info** | [📄 Download PDF](./reports/ThunderLoan-Security-Audit-Report.pdf) | [📝 Read Markdown](./reports/ThunderLoan-Security-Audit-Report.md) |
| **Boss Bridge** | Sep 2026 | `L1BossBridge.sol`, `L1Vault.sol`, TokenFactory (215 nSLOC) | **4 High, 2 Med, 2 Low** | [📄 Download PDF](./reports/BossBridge-Security-Audit-Report.pdf) | [📝 Read Markdown](./reports/BossBridge-Security-Audit-Report.md) |
| **T-Swap** | Sep 2026 | `TSwapPool.sol`, `PoolFactory.sol` (345 nSLOC) | **4 High, 3 Med, 3 Low, 10 Info** | [📄 Download PDF](./reports/TSwap-Security-Audit-Report.pdf) | [📝 Read Markdown](./reports/TSwap-Security-Audit-Report.md) |
| **Algo Stablecoin** | Sep 2026 | `dsc_engine.vy`, `oracle_lib.vy`, `dsc.vy` (390 SLoC Vyper) | **2 High, 4 Med, 2 Low** | [📄 Download PDF](./reports/AlgoStablecoin-Security-Audit-Report.pdf) | [📝 Read Markdown](./reports/AlgoStablecoin-Security-Audit-Report.md) |
| **Puppy Raffle** | Sep 2026 | `PuppyRaffle.sol` (143 nSLOC) | **5 High, 3 Med, 2 Low, 1 Gas, 2 Info** | [📄 Download PDF](./reports/PuppyRaffle-Security-Audit-Report.pdf) | [📝 Read Markdown](./reports/PuppyRaffle-Security-Audit-Report.md) |
| **PasswordStore** | Sep 2026 | `PasswordStore.sol` (25 nSLOC) | **2 High, 1 Gas, 3 Info** | [📄 Download PDF](./reports/PasswordStore-Security-Audit-Report.pdf) | [📝 Read Markdown](./reports/PasswordStore-Security-Audit-Report.md) |

---

## 🔍 Featured Audit Highlights

### 1. [Vault Guardians Protocol Audit](./reports/VaultGuardians-Security-Audit-Report.pdf)
- **Target:** Decentralized asset management and yield-generation protocol utilizing ERC4626 vaults, Aave V3 lending adapters, and Uniswap V2 liquidity pools.
- **Key Vulnerabilities Identified:**
  - **[H-01] Mainnet Exit Freeze DoS via Null Uniswap WETH Pair:** Uncovered unhandled revert when unwinding Uniswap liquidity for WETH-paired vaults, permanently freezing user redemptions.
  - **[H-02] Protocol Fee & State Bypass via `ERC4626::mint()`:** Discovered direct ERC4626 standard minting bypassed custom fee-collection logic and guardian stake distribution.
  - **[H-03] Investor Exit Freeze via Zero Idle Balance (`maxWithdraw == 0`):** Demonstrated vault liquidity starvation where zero idle funds prevents investor withdrawals even when invested assets are solvent.
  - **[H-04] Excessive `amountADesired` Token Over-Request in `_uniswapInvest`:** Proved math calculation flaw forcing token transactions to demand more funds than deposited.
  - **[H-05] Divestment Exit Freeze via Missing Counterparty Approval:** Identified missing router token allowances preventing divestment calls from succeeding.
  - **[H-06] USDC Vault Deadlock via 18-Decimal Stake Price Requirement:** Proved guardian stake calculation hardcoded 18 decimals, reverting registration for 6-decimal token vaults.
  - **[H-07] Permissionless Rebalance Execution With Zero Slippage Protection:** Exposed front-runnable rebalancing exposing LP positions to sandwich extraction.
  - **[M-01 - M-04] Active Vault Overwriting, Div-by-Zero DoS, Uncollected Registration Fees, Governance Timelock Omission:** Severe governance and vault lifecycle accounting bugs.
- **Verification:** Foundry unit exploit test suite, invariant fuzz testing with `fail_on_revert = true`, and mutation validation.

### 2. [Thunder Loan Protocol Audit](./reports/ThunderLoan-Security-Audit-Report.pdf)
- **Target:** Uncollateralized flash loan protocol featuring dynamic AMM fee pricing, interest-bearing `AssetToken` vaults, and UUPS upgradeable proxies.
- **Key Vulnerabilities Identified:**
  - **[H-01] Flash Loan Deposit Reentrancy Allows Full Drainage of Underlying Pool Liquidity:** Reentrancy vulnerability during `flashLoan` execution allowing borrowers to deposit borrowed funds and steal vault capital upon repayment verification.
  - **[H-02] AMM Spot Price Oracle Manipulation Collapses Flash Loan Fees to Zero:** Exploited spot-price oracle vulnerability using Uniswap/TSwap flash-swaps to manipulate fee queries to zero.
  - **[H-03] Currency Denomination Mismatch in Fee Calculation Corrupts Accounting:** Fixed-point precision mismatch bricking fee collection on WETH loans.
  - **[H-04] Phantom Fee & Erroneous Exchange Rate Inflation in `deposit()` Guarantees Protocol Insolvency:** Accounting flaw artificially inflating deposit exchange rates without backing liquidity.
  - **[H-05] Storage Layout Collision in `ThunderLoanUpgraded.sol` Shifts Slot 2 and Inflates Fees to 100%:** Identified proxy upgrade collision causing catastrophic state corruption and fee skyrocketing.
  - **[H-06] Uninitialized Proxy in `DeployThunderLoan.s.sol` Allows Frontrunning Protocol Takeover:** Demonstrated malicious actor initialization hijacking contract ownership.
  - **[H-07] Token Whitelist Revocation Deletes Mapping and Permanently Freezes LP Liquidity:** Removing asset from whitelist deleted custody tracking, locking LP capital permanently.
  - **[M-01 - M-02] Solvency Deficit Invariant Violations & Dust Denial of Service:** Exchange rate rounding degradation and zero-amount flash loan reverts.
- **Verification:** 384,000 stateful invariant calls in Foundry (`Handler.t.sol` + `Invariant.t.sol`), ghost accounting deficit tracking, and full exploit PoCs.

### 3. [Boss Bridge Protocol Audit](./reports/BossBridge-Security-Audit-Report.pdf)
- **Target:** Cross-chain bridge infrastructure for transferring ERC20 assets between Ethereum Mainnet (L1) and ZKsync Layer 2.
- **Key Vulnerabilities Identified:**
  - **[H-01] Missing Signature Replay Protection in `sendToL1` Allows Complete Drainage of Vault Funds:** Discovered validator signatures lacked nonces, chain IDs, and replay tracking, allowing attackers to replay a single withdrawal signature until vault is depleted.
  - **[H-02] Arbitrary `from` Address in `depositTokensToL2` Enables Theft of User-Approved ERC20 Tokens:** Parameter allowed any third party to specify victim address in `transferFrom` calls, draining approved balances to attacker's L2 account.
  - **[H-03] Vault-to-Vault Self-Transfer via Bridge Allowance Enables Minting Unbacked L2 Tokens:** Attacker could initiate deposit from bridge vault address to itself, triggering L2 mint events without supplying collateral.
  - **[H-04] Unconstrained Arbitrary Low-Level Call in `sendToL1` Allows Attacker to Hijack Vault Custody:** Flawed call target specification enabling arbitrary contract calls with bridge privileges.
  - **[M-01 - M-02] Unsupported EVM `create` Opcode on ZKsync Era in `TokenFactory` & DoS via Direct Vault Donations:** Deployment failure on target rollup and balance invariant disruption via token donation.
- **Verification:** Deterministic Foundry unit PoCs (`test/unit/PoCAuditTest.t.sol`), stateful invariant fuzzing (32,768 calls across 256 runs), and mutation testing score of 85.71%.

### 4. [T-Swap Protocol Audit](./reports/TSwap-Security-Audit-Report.pdf)
- **Target:** Constant-product Automated Market Maker (AMM) modeled after Uniswap V1 ($x \cdot y = k$) with liquidity provisioning and incentive distribution.
- **Key Vulnerabilities Identified:**
  - **[H-01] Unaccounted Swap Incentive Reward in `_swap` Breaks Constant Product Invariant ($x \cdot y = k$):** Discovered protocol incentive transfer directly drained pool reserve without updating invariant state, enabling recursive liquidity draining.
  - **[H-02] Incorrect Numerator Constant (10000 vs 1000) in `getInputAmountBasedOnOutput` Overcharges Traders by ~10x:** Math flaw resulting in astronomical pricing for exact output swaps.
  - **[H-03] Inverted Call in `sellPoolTokens` Passes Input Amount as Desired Output:** Inverted function call causing catastrophic token deduction or unexpected execution reverts.
  - **[H-04] Hardcoded 18-Decimal Swap Reward in `_swap` Permanently Blocks All Swaps for Non-18 Decimal Pools:** Reverts all swaps on USDC/USDT/WBTC pairs due to decimal incompatibility.
  - **[M-01 - M-03] Missing Slippage Protection in `swapExactOutput`, Unenforced `deadline` in `deposit`, and Unassigned Return Variable in `swapExactInput`:** Exposing users to sandwich MEV and stale transaction exploitation.
- **Verification:** Comprehensive Foundry test suite, invariant testing, and mathematical AMM reserve curve verification.

### 5. [Algo Stablecoin Protocol Audit](./reports/AlgoStablecoin-Security-Audit-Report.pdf)
- **Target:** Decentralized, exogenous collateral-backed algorithmic stablecoin protocol written in Vyper (`^0.4.0`) deployed on ZKsync Era.
- **Key Vulnerabilities Identified:**
  - **[H-01] Hardcoded 18-Decimal Scaling Causes 10-Order-of-Magnitude WBTC Collateral Undervaluation:** Hardcoded 18 decimals priced 8-decimal WBTC deposits at \$0.000006 per token, bricking minting and liquidation transfers.
  - **[H-02] Flawed Health Factor Monotonicity Assertion Blocks Liquidation of Underwater Accounts ($HF \le 0.55$):** Mathematical proof showing 10% liquidation bonus causes ending HF to drop below starting HF when borrower is deeply underwater, reverting liquidation calls and accumulating permanent bad debt.
  - **[M-01 - M-04] Missing Non-Zero Oracle Price Validation, CEI Violation in `liquidate()`, Permanent DSC Token Minter Role Lock, and Missing ZKsync L2 Sequencer Uptime Feed:** Oracle circuit breaker and reentrancy hardening.
- **Verification:** Moccasin / Titanoboa Python & Pytest PoC suite (`tests/unit/test_poc_audit.py`), stateful fuzzing, and mathematical liquidation boundary proofs.

### 6. [Puppy Raffle Protocol Audit](./reports/PuppyRaffle-Security-Audit-Report.pdf)
- **Target:** On-chain lottery and NFT reward distribution protocol on EVM.
- **Key Vulnerabilities Identified:**
  - **[H-01] State Update After External Call in `refund` Enables Reentrancy:** Exploited CEI violation to drain all contract deposits recursively.
  - **[H-02] Predictable Pseudo-Randomness in `selectWinner`:** Demonstrated simulation of `block.timestamp` and `block.difficulty` to manipulate winner selection and NFT rarity tiers.
  - **[H-03] Integer Truncation & Overflow in `totalFees`:** Uncovered `uint64(fee)` bit truncation above ~18.44 ETH, permanently corrupting fee accounting and locking protocol funds.
  - **[H-04] Strict Contract Balance Equality Check in `withdrawFees`:** Demonstrated permanent DoS via `selfdestruct` force-feeding.
  - **[H-05] Unbounded Loop for Duplicate Player Checks in `enterRaffle`:** Proved quadratic gas scaling ($O(n^2)$) causing Denial of Service via block gas limit exhaustion.
  - **[M-01 - M-03] Push Payment Freezes, Index 0 Ambiguity, & CEI Violations:** Identified contract-bricking push payments and state inconsistencies during NFT minting callbacks.
- **Verification:** 100% test pass rate on Foundry with custom reentrancy, overflow, and gas exhaustion exploit contracts.

### 7. [PasswordStore Protocol Audit](./reports/PasswordStore-Security-Audit-Report.pdf)
- **Target:** Personal private password vault protocol on EVM.
- **Key Vulnerabilities Identified:**
  - **[H-01] Storing Plaintext Password in On-Chain Storage Violates Confidentiality:** Demonstrated extraction of private variables directly from EVM storage slot 1 using `vm.load` and `cast storage`.
  - **[H-02] Missing Access Control in `setPassword`:** Identified arbitrary state mutation allowing any unauthenticated account to overwrite the vault owner's password.
  - **[G-01] State Variable `s_owner` Non-Immutable:** Optimized SLOAD gas overhead by transitioning initialization to immutable bytecode storage.
  - **[I-01 - I-03] NatSpec Inconsistencies, Event Typo, & Solc Compiler Bugs:** Code quality hardening and event synchronization improvements.
- **Verification:** 100% Line, Branch, and Function coverage with Foundry reproducible exploit test cases.

---

## 🔬 Audit Methodology (The Tincho Method)

My security engagements follow a structured 8-phase auditing framework:

1. **Phase 0: Audit Readiness (The Rekt Test)** — Evaluating codebase maturity, documentation, test suite health, static analysis baselines, and dependency pinning.
2. **Phase 1: Scoping & Complexity Mapping** — Quantifying nSLOC, dependency mapping, and complexity tiering.
3. **Phase 2: Reconnaissance & Invariant Hypothesis** — Threat modeling, privileged actor analysis, and protocol invariant definitions.
4. **Phase 3: Line-by-Line Code Review** — Systematic manual inspection of control flows, state transitions, and arithmetic operations (FREI-PI / CEI patterns).
5. **Phase 4: Adversarial Attack Vectoring** — Modeling front-running/MEV, access control bypasses, storage transparency, reentrancy, and flash loan manipulations.
6. **Phase 5: Automated Testing & PoC Construction** — Writing deterministic Foundry & Moccasin exploit test cases proving vulnerability validity and financial impact.
7. **Phase 6 & 7: Classification & Executive PDF Reporting** — Formatting findings according to CodeHawks severity standards and compiling publication-grade PDF reports with Pandoc & LaTeX (Eisvogel).
8. **Phase 8: Mitigation Review & Re-Testing** — Verifying that client remediation patches resolve root causes without introducing regression issues.

---

## 🛠️ Security Tooling & Stack

- **Testing & Execution Frameworks:** Foundry (`forge`, `cast`, `anvil`), Moccasin / Titanoboa, Hardhat
- **Static Analysis & Linters:** Slither, Aderyn, Solhint
- **Fuzzing & Invariant Testing:** Echidna, Foundry Invariant Testing (`vm.assume`, handler-based stateful fuzzing)
- **Report Generation:** Pandoc, Eisvogel LaTeX Engine, KaTeX

---

## 📬 Contact & Profiles

- **GitHub:** [@farhandavin](https://github.com/farhandavin)
- **CodeHawks:** [farhandavin](https://codehawks.com)
- **Specialization:** Solidity, Vyper, EVM Architecture, DeFi Security, AMM & Lending Math, Access Control & Storage Security
