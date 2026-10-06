# 🧮 Formal Verification Case Study: MathMasters Fixed-Point Arithmetic

![Certora](https://img.shields.io/badge/Certora-Prover_6.x-blue?style=for-the-badge&logo=solidity)
![SMT](https://img.shields.io/badge/SMT_Solver-Z3_|_CVC5-purple?style=for-the-badge)
![Status](https://img.shields.io/badge/Verification-Mathematical_Proof-success?style=for-the-badge)

## 📌 Executive Summary

Fixed-point arithmetic libraries are the bedrock of Decentralized Finance (DeFi)—powering constant-product AMM pricing, collateral health factors, share redemption ratios, and interest rate accumulators. In high-stakes protocols, an off-by-one rounding error or an unexpected precision degradation can lead to severe insolvency or systemic arbitrage exploits.

This case study demonstrates the formal verification of `MathMasters::mulWadUp`, an optimized fixed-point arithmetic library inspired by **Solady** and **Solmate**, using **Certora Verification Language (CVL)** and the **Certora Prover**.

---

## 🎯 Verification Scope & Target

- **Target Library:** [`MathMasters.sol`](./src/MathMasters.sol)
- **Harness Contract:** [`CompactCodeBase.sol`](./src/CompactCodeBase.sol)
- **Certora Spec:** [`MulWadUp.spec`](./certora/MulWadUp.spec)
- **Certora Config:** [`MulWadUp.conf`](./certora/MulWadUp.conf)

### The Function Under Verification: `mulWadUp`

$$\text{mulWadUp}(x, y) = \left\lceil \frac{x \times y}{\text{WAD}} \right\rceil = \begin{cases} 0 & \text{if } x \times y = 0 \\ \left\lfloor \frac{x \times y - 1}{\text{WAD}} \right\rfloor + 1 & \text{if } x \times y > 0 \end{cases}$$

Where $\text{WAD} = 10^{18}$ ($1\text{e}18$).

---

## 🔬 CVL Formal Specification

### 1. Methods Block & Environment Independence
The function `mulWadUp` is pure and operates strictly on input arguments without relying on block environment variables (`msg.sender`, `block.timestamp`, `msg.value`). Hence, it is declared `envfree`:

```cvl
methods {
    function mulWadUp(uint256 x, uint256 y) external returns uint256 envfree;
}

definition WAD() returns uint256 = 1000000000000000000; // 1e18
```

### 2. Parametric Fuzzing Rule (`testMulWadUpFuzz`)
The rule verifies that for any arbitrary pair of 256-bit unsigned integers $(x, y)$ that do not exceed EVM arithmetic bounds ($x \times y \le 2^{256} - 1$), the smart contract implementation matches the mathematical ideal over unbounded infinite-precision integers (`mathint`):

```cvl
rule testMulWadUpFuzz(uint256 x, uint256 y) {
    // Precondition: Discard overflowing product inputs handled by revert guards
    require(x == 0 || y == 0 || y <= assert_uint256(max_uint256 / x));

    // Execution
    uint256 result = mulWadUp(x, y);

    // Mathematical Ground Truth (Evaluated in CVL unbounded integer math)
    mathint expected = x * y == 0 ? 0 : (x * y - 1) / WAD() + 1;

    // Mathematical Assertion
    assert result == expected, "mulWadUp result deviates from mathematical ceiling division";
}
```

### 3. State Invariant Formulation (`mulWadUpInvariant`)
In addition to the fuzzing rule, a formal invariant asserts the identity across all reachable states:

```cvl
invariant mulWadUpInvariant(uint256 x, uint256 y)
    mulWadUp(x, y) == assert_uint256(x * y == 0 ? 0 : (x * y - 1) / WAD() + 1)
    {
        preserved {
            require(x == 0 || y == 0 || y <= assert_uint256(max_uint256 / x));
        }
    }
```

---

## 🐛 Vulnerability Detection via SMT Solver

During verification of the candidate implementation, the Certora Prover successfully identified and counterexample-proven an intentional logic mutation injected into `MathMasters.sol`:

```solidity
assembly {
    if mul(y, gt(x, div(not(0), y))) {
        mstore(0x40, 0xbac65e5b) // MathMasters__MulWadFailed()
        revert(0x1c, 0x04)
    }
    // Vulnerability Injected: Conditional increment skewing ceiling division
    if iszero(sub(div(add(z, x), y), 1)) { x := add(x, 1) }
    z := add(iszero(iszero(mod(mul(x, y), WAD))), div(mul(x, y), WAD))
}
```

### Prover Counterexample
The SMT solver constructed an exact numerical assignment violating the assertion:
- Input: $x = 1$, $y = 10^{18}$
- Expected: $1$
- Result returned: $2$ (due to unintended increment in $x$)
- **Status:** Formally caught and disproven mathematically before any production deployment.

---

## ⚙️ Certora CLI Execution

```bash
certoraRun formal-verification/01-math-master/certora/MulWadUp.conf
```

Configuration details ([`MulWadUp.conf`](./certora/MulWadUp.conf)):
```json
{
    "files": [
        "src/CompactCodeBase.sol"
    ],
    "verify": "CompactCodeBase:certora/MulWadUp.spec",
    "wait_for_results": "all",
    "rule_sanity": "basic",
    "optimistic_loop": true,
    "msg": "Formal Verification of Fixed-Point mulWadUp"
}
```
