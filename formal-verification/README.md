# 🔬 Formal Verification (Certora CVL & Invariant Proving)

This directory contains production-grade **Formal Verification** specifications, harnesses, and mathematical proofs developed with the **Certora Prover** and **Certora Verification Language (CVL)**.

Formal verification complements adversarial manual review and stateful fuzzing by using SMT solvers (Z3, CVC5) to **mathematically prove** that smart contract invariants hold true across **all possible inputs and all reachable execution states** ($2^{256}$ search space).

---

## 📚 Verification Case Studies

| Case Study | Category | Core Technique | Key Invariants / Rules | Directory |
| :--- | :--- | :--- | :--- | :---: |
| **01. Math Masters** | Pure Fixed-Point Math | SMT Solver Proofs, Bounded Arithmetic | `mulWadUp` Precision Monotonicity, Solady/Solmate Equivalence, Overflow Boundary Invariant | [📂 Explore](./01-math-master) |
| **02. GasBad NFT Marketplace** | Differential Formal Verification | Equivalence Checking, Opcode Hooks, Persistent Ghosts | State Equivalence (Assembly vs Solidity), Storage Hook Invariant (`Sstore` $\le$ `LOG4`), Anti-Havoc Dispatchers | [📂 Explore](./02-gas-bad-nft-marketplace) |

---

## 🛠️ Key Capabilities & Techniques Demonstrated

### 1. Differential Formal Verification (Equivalence Proofs)
- Mathematically verifying that hyper-optimized inline assembly (Yul/Huff) matches the exact functional semantics of audited reference Solidity contracts.
- Parametric rules quantifying over all functions (`method f`, `method f2`) where `f.selector == f2.selector`.

### 2. Ghost Variables & Opcode Hooks
- Out-of-band state tracking (`ghost mathint`) with initial state axioms (`init_state axiom ghostVar == 0`).
- Direct EVM opcode instrumentation: intercepting low-level storage modifications (`hook Sstore`) and event emissions (`hook LOG4`).

### 3. Anti-Havoc Protocols & Method Summaries
- Handling external and unpredictable call boundaries using wildcard summaries:
  ```cvl
  function _.onERC721Received(address, address, uint256, bytes) external => DISPATCHER(true);
  function _.safeTransferFrom(address, address, uint256) external => DISPATCHER(true);
  ```
- Balancing sound proof verification with `optimistic_fallback` configurations.

### 4. Arithmetic Boundary & Fixed-Point Verification
- Validating rounding directions (rounding up vs down), ceiling division invariants, and overflow prevention in fixed-point decimal arithmetic (WAD/RAY).

---

## 🚀 Running Certora Verification

### Prerequisites
- Python 3.9+ & `certora-cli` installed: `pip install certora-cli`
- Valid Certora API key set: `export CERTORAKEY=<your_key>`
- Foundry / Solc installed

### Commands
```bash
# Verify Math Masters Fixed-Point Library
certoraRun formal-verification/01-math-master/certora/MulWadUp.conf

# Verify GasBad NFT Marketplace Equivalence
certoraRun formal-verification/02-gas-bad-nft-marketplace/certora/conf/GasBadNft.conf
```
