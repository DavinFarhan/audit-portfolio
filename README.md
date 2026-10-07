<p align="center">
  <img src="./.github/assets/logo.svg" alt="Farhan Davin - Smart Contract Auditor" width="680"/>
</p>

<p align="center">
  <strong>Smart Contract Security Researcher</strong><br/>
  Specializing in <em>Stateful Invariant Fuzzing (Foundry)</em> &amp; <em>Formal Verification (Certora / CVL)</em>
</p>

<p align="center">
  <a href="#-core-principles--ethics"><img src="https://img.shields.io/badge/Ethics-Transparent_%26_Amanah-059669?style=flat-square" alt="Ethics"/></a>
  <a href="#-core-specializations"><img src="https://img.shields.io/badge/Focus-Invariant_Fuzzing_%26_Certora-0B1F3A?style=flat-square" alt="Focus"/></a>
  <a href="#-security-audit-reports"><img src="https://img.shields.io/badge/Reports-6_PDFs-blue?style=flat-square" alt="Reports"/></a>
  <a href="https://github.com/farhandavin"><img src="https://img.shields.io/badge/GitHub-farhandavin-181717?style=flat-square&logo=github" alt="GitHub"/></a>
</p>

---

## 🧭 About Me

Hi, I'm **Farhan Davin**, an independent smart contract security auditor. I focus on uncovering complex logic flaws, breaking system invariants, and mathematically proving protocol correctness on Ethereum and EVM-compatible blockchains.

---

## ⚖️ Core Principles & Ethics

I hold myself to the highest standard of integrity, transparency, and Islamic professional ethics:

- **Honesty (*Jujur*) & Transparency**: Zero inflated claims. The reports below are intensive educational & training audits (Cyfrin Updraft curricula and deep adversarial practice).
- **Trustworthiness (*Amanah*)**: Strict confidentiality and care with protocol codebases and client engagements.
- **Reliability (*Menepati Janji*)**: Punctual delivery, honoring timelines, and meeting every commitment.
- **Professional Quality**: Mathematical and adversarial depth going far beyond surface-level static analysis.
- **Developer-Friendly (*Mempermudah*)**: Clear findings, reproducible Foundry PoCs, and actionable remediation steps.
- **Generosity (*Murah Hati*)**: Value-first collaboration, sharing knowledge, and actively helping teams level up their security.

---

## 🔬 Core Specializations

### 1. Stateful Invariant Fuzzing (Foundry)
- **Handler-Based Architecture**: Simulating real-world interactions across multiple actors (LPs, borrowers, liquidators).
- **System Invariants**: Defining and testing strict conservation laws (e.g. reserve backing, solvency equations, $x \cdot y \ge k$).
- **Ghost Accounting**: Tracking internal state deficits and fee compounding with strict `fail_on_revert = true` enforcement.

### 2. Formal Verification (Certora / CVL)
- **Exhaustive Mathematical Proofs**: Using SMT solvers to verify rules across all possible inputs ($2^{256}$ space).
- **Equivalence Verification**: Proving that gas-optimized contracts behave identically to reference implementations.
- **Storage Hooks & Ghosts**: Tracking low-level EVM storage mutations (`hook Sstore`) and event integrity (`hook LOG4`).

---

## 📑 Security Audit Reports

> [!NOTE]
> The reports below are comprehensive educational audits conducted during rigorous security training, demonstrating end-to-end vulnerability discovery, PoC construction, and executive reporting.

| Protocol | Date | Scope | Key Focus | Audit Report |
| :--- | :---: | :--- | :--- | :---: |
| **Vault Guardians** | Sep 2026 | ERC4626 Vaults, Uniswap V2, Aave V3 (589 nSLOC) | Reentrancy, Fee Bypass via `mint()`, Liquidity Starvation DoS | [📄 View PDF](./VaultGuardians-Security-Audit-Report.pdf) |
| **Thunder Loan** | Sep 2026 | Flash Loans, AMM Oracle, UUPS Proxy (475 nSLOC) | Flash Loan Reentrancy, Oracle Manipulation, Storage Layout | [📄 View PDF](./ThunderLoan-Security-Audit-Report.pdf) |
| **Boss Bridge** | Sep 2026 | Cross-Chain L1-L2 Token Bridge (215 nSLOC) | Signature Replay, Arbitrary `transferFrom`, Low-Level Call Hijack | [📄 View PDF](./BossBridge-Security-Audit-Report.pdf) |
| **T-Swap** | Sep 2026 | Constant-Product AMM ($x \cdot y = k$) (345 nSLOC) | Pool Reserve Drain, Math Precision Flaws, Missing Slippage | [📄 View PDF](./TSwap-Security-Audit-Report.pdf) |
| **Puppy Raffle** | Sep 2026 | NFT Raffle & Lottery System (143 nSLOC) | Reentrancy in `refund()`, Weak PRNG, Unbounded Loop DoS | [📄 View PDF](./PuppyRaffle-Security-Audit-Report.pdf) |
| **PasswordStore** | Sep 2026 | Private Password Vault (25 nSLOC) | On-Chain Storage Visibility, Missing Access Control | [📄 View PDF](./PasswordStore-Security-Audit-Report.pdf) |

---

## 🧰 Tools & Technology Stack

- **Testing & Execution Framework:** Foundry (`forge`, `cast`, `anvil`)
- **Formal Verification:** Certora Prover, CVL (Certora Verification Language)
- **Static Analysis:** Slither, Aderyn
- **Smart Contract & Low-Level Languages:** Solidity, Yul, Huff, CVL
- **Report Compilation:** Pandoc, Eisvogel LaTeX Engine, KaTeX

---

## 📬 Contact & Engagements

Available for private smart contract security audits, invariant fuzzing harness development, and formal verification reviews:

- **GitHub:** [@farhandavin](https://github.com/farhandavin)
- **CodeHawks:** [farhandavin](https://codehawks.com)
- **Email:** [farhandavin14@gmail.com](mailto:farhandavin14@gmail.com)

---

<p align="center">
  <sub>Upholding Truth, Precision, and Trust in Web3 Security.</sub>
</p>
