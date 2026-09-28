---
title: TSwap Protocol Security Audit Report
author: Farhan Davin
date: \today
header-includes:
  - \usepackage{titling}
  - \usepackage{graphicx}
---

\begin{titlepage}
    \centering
    \begin{figure}[h]
        \centering
        \includegraphics[width=0.45\textwidth]{logo.pdf} 
    \end{figure}
    \vspace*{1.5cm}
    {\Huge\bfseries TSwap Protocol\par}
    \vspace{0.4cm}
    {\LARGE\bfseries Security Audit Report\par}
    \vspace{0.8cm}
    {\Large Version 1.0\par}
    \vspace{1.5cm}
    {\Large\itshape Prepared by: Farhan Davin (Lead Auditor)\par}
    \vfill
    {\large \today\par}
\end{titlepage}

\maketitle

<!-- Report Content Begins -->

Prepared by: Farhan Davin (Lead Security Researcher)  
Audited Codebase: [Cyfrin / 5-t-swap-audit](https://github.com/Cyfrin/5-t-swap-audit)  
Commit Hash: e643a8d4c2c802490976b538dd009b351b1c8dda  
Methodology: The Tincho Method  

# Table of Contents
- [Table of Contents](#table-of-contents)
- [Protocol Summary](#protocol-summary)
- [Disclaimer](#disclaimer)
- [Risk Classification](#risk-classification)
- [Audit Details](#audit-details)
  - [Scope](#scope)
  - [Roles](#roles)
- [Executive Summary](#executive-summary)
  - [Issues found](#issues-found)
- [Findings](#findings)
  - [High Severity Findings](#high-severity-findings)
    - [[H-1] Unaccounted Swap Incentive Reward in `_swap` Breaks Constant Product Invariant ($x \cdot y = k$) and Enables Liquidity Reserve Draining](#h-1-unaccounted-swap-incentive-reward-in-_swap-breaks-constant-product-invariant-x-cdot-y--k-and-enables-liquidity-reserve-draining)
    - [[H-2] Incorrect Numerator Constant (10000 vs 1000) in `getInputAmountBasedOnOutput` Overcharges Traders by ~10x](#h-2-incorrect-numerator-constant-10000-vs-1000-in-getinputamountbasedonoutput-overcharges-traders-by-10x)
    - [[H-3] Inverted Call in `sellPoolTokens` Passes Input Amount as Desired Output, Causing Catastrophic Token Loss or Revert](#h-3-inverted-call-in-sellpooltokens-passes-input-amount-as-desired-output-causing-catastrophic-token-loss-or-revert)
    - [[H-4] Hardcoded 18-Decimal Swap Reward in `_swap` Permanently Blocks All Swaps for Non-18 Decimal Token Pools (USDC, WBTC)](#h-4-hardcoded-18-decimal-swap-reward-in-_swap-permanently-blocks-all-swaps-for-non-18-decimal-token-pools-usdc-wbtc)
  - [Medium Severity Findings](#medium-severity-findings)
    - [[M-1] Absence of `maxInputAmount` Slippage Protection in `swapExactOutput` Exposes Users to Extreme Capital Theft via Sandwich Attacks](#m-1-absence-of-maxinputamount-slippage-protection-in-swapexactoutput-exposes-users-to-extreme-capital-theft-via-sandwich-attacks)
    - [[M-2] Unused `deadline` Parameter in `deposit` Fails to Enforce Transaction Expiration, Enabling Execution of Stale Mempool Transactions](#m-2-unused-deadline-parameter-in-deposit-fails-to-enforce-transaction-expiration-enabling-execution-of-stale-mempool-transactions)
    - [[M-3] Unassigned Named Return Variable in `swapExactInput` Always Evaluates to Zero, Breaking Composability](#m-3-unassigned-named-return-variable-in-swapexactinput-always-evaluates-to-zero-breaking-composability)
  - [Low Severity Findings](#low-severity-findings)
    - [[L-1] Swapped Arguments in `LiquidityAdded` Event Emission Corrupts Off-Chain Accounting](#l-1-swapped-arguments-in-liquidityadded-event-emission-corrupts-off-chain-accounting)
    - [[L-2] `PoolFactory.createPool` Permits WETH/WETH Pairs and Zero Address Token Deployments](#l-2-poolfactorycreatepool-permits-wethweth-pairs-and-zero-address-token-deployments)
    - [[L-3] `PoolFactory.createPool` Concatenates Token Name Instead of Symbol for LP Token Symbol](#l-3-poolfactorycreatepool-concatenates-token-name-instead-of-symbol-for-lp-token-symbol)
  - [Informational Findings](#informational-findings)
    - [[I-1] Missing Zero Address Validation in `PoolFactory` Constructor Risks Permanent Misconfiguration](#i-1-missing-zero-address-validation-in-poolfactory-constructor-risks-permanent-misconfiguration)
    - [[I-2] Unused Custom Error `PoolFactory__PoolDoesNotExist` Increases Bytecode Size](#i-2-unused-custom-error-poolfactory__pooldoesnotexist-increases-bytecode-size)
    - [[I-3] Unused Storage Read `poolTokenReserves` in `deposit` Wastes Gas (Compiler Warning 2072)](#i-3-unused-storage-read-pooltokenreserves-in-deposit-wastes-gas-compiler-warning-2072)
    - [[I-4] Unindexed Event Parameters in `PoolFactory.PoolCreated` and `TSwapPool.Swap` Prevent Efficient Log Filtering](#i-4-unindexed-event-parameters-in-poolfactorypoolcreated-and-tswappoolswap-prevent-efficient-log-filtering)
    - [[I-5] Strict Equality Comparison in `revertIfZero` Modifier](#i-5-strict-equality-comparison-in-revertifzero-modifier)
    - [[I-6] Erroneous Mathematical Explanation in NatSpec / Comments Misleads Developers](#i-6-erroneous-mathematical-explanation-in-natspec--comments-misleads-developers)
    - [[I-7] Redundant Wrapper Function `totalLiquidityTokenSupply()` Adds Bytecode Overhead](#i-7-redundant-wrapper-function-totalliquiditytokensupply-adds-bytecode-overhead)
    - [[I-8] Unnamed Magic Numbers Obscure Business Logic and Contribute to Math Errors](#i-8-unnamed-magic-numbers-obscure-business-logic-and-contribute-to-math-errors)
    - [[I-9] Private Function Declarations Preceding Public View Functions Violates Solidity Style Guide](#i-9-private-function-declarations-preceding-public-view-functions-violates-solidity-style-guide)
    - [[I-10] License Identifier Discrepancy Between Protocol (GPL-3.0) and Dependencies (MIT)](#i-10-license-identifier-discrepancy-between-protocol-gpl-30-and-dependencies-mit)
    - [[I-11] Unused Function Parameter `deadline` in `deposit` Triggers Compiler Warning (5667)](#i-11-unused-function-parameter-deadline-in-deposit-triggers-compiler-warning-5667)
- [Test Suite Quality & Mutation Testing Review](#test-suite-quality--mutation-testing-review)
- [General Recommendations](#general-recommendations)

---

# Protocol Summary

TSwap is an Automated Market Maker (AMM) protocol loosely modeled after Uniswap v1. It facilitates permissionless token swaps between arbitrary ERC20 tokens and Wrapped Ether (WETH). 

The protocol operates via a core factory contract, `PoolFactory`, which handles the permissionless deployment and registry of individual token pools (`TSwapPool`). Each pool maintains balances of two assets: a single ERC20 token and WETH.

Liquidity providers deposit both assets in equal proportion to the current reserve ratio and receive ERC20 LP shares representing their proportional claims on the underlying reserves and accumulated 0.3% trading fees. Traders interact with each pool via `swapExactInput` and `swapExactOutput` functions, with prices dictated by the constant product formula:

$$(x + \Delta x \cdot (1 - \rho)) \cdot (y - \Delta y) \ge x \cdot y$$

where $\rho = 0.003$ (representing the 0.3% trading fee).

---

# Disclaimer

The audit team makes all effort to find as many vulnerabilities in the code in the given time period, but holds no responsibilities for the findings provided in this document. A security audit is not an endorsement of the underlying business or product. The review of the code was solely on the security aspects of the Solidity implementation of the contracts.

---

# Risk Classification

| Likelihood \ Impact | High | Medium | Low |
| :--- | :---: | :---: | :---: |
| **High** | High | High/Medium | Medium |
| **Medium** | High/Medium | Medium | Medium/Low |
| **Low** | Medium | Medium/Low | Low |

We use the [CodeHawks](https://docs.codehawks.com/hawks-auditors/how-to-evaluate-a-finding-severity) severity matrix to determine severity based on Impact and Likelihood.

---

# Audit Details 

## Scope 

- **Repository:** Cyfrin / 5-t-swap-audit
- **Commit Hash:** `e643a8d4c2c802490976b538dd009b351b1c8dda`
- **Solidity Version:** 0.8.20

### In-Scope Contracts

```text
src/
|-- PoolFactory.sol    (64 lines, Registry and pair deployment)
#-- TSwapPool.sol      (429 lines, Core AMM pricing and liquidity logic)
```

## Roles

- **Liquidity Provider (LP):** Unprivileged actor depositing dual assets to earn pro-rata swap fees.
- **Trader (Swapper):** Unprivileged actor executing swaps via exact-input or exact-output paths.
- **Factory Deployer:** Unprivileged initial deployer of `PoolFactory`.

---

# Executive Summary

During September 2026, a security review of the **TSwap** protocol was conducted using **The Tincho Method**. The audit identified **4 High Severity**, **3 Medium Severity**, **3 Low Severity**, and **11 Informational** vulnerabilities.

Multiple critical vulnerabilities directly violate core economic invariants, allow draining of liquidity reserves, cause massive pricing overcharges (~10x), and trigger complete Denial of Service for common non-18 decimal ERC20 tokens like USDC.

## Issues found

| Severity | Number of issues found | Resolved | Acknowledged |
| :--- | :---: | :---: | :---: |
| High | 4 | 0 | 4 |
| Medium | 3 | 0 | 3 |
| Low | 3 | 0 | 3 |
| Informational | 11 | 0 | 11 |
| **Total** | **21** | **0** | **21** |

---

# Findings

## High Severity Findings

### [H-1] Unaccounted Swap Incentive Reward in `_swap` Breaks Constant Product Invariant ($x \cdot y = k$) and Enables Liquidity Reserve Draining

**Description:**

In `TSwapPool.sol`, every 10 swaps (`SWAP_COUNT_MAX`), the contract awards the trader an additional `1e18` (1 token) of `outputToken` directly from pool reserves:

```solidity
swap_count++;
if (swap_count >= SWAP_COUNT_MAX) {
    swap_count = 0;
    outputToken.safeTransfer(msg.sender, 1_000_000_000_000_000_000);
}
```

This transfer is executed from the pool's core asset reserves without receiving any corresponding input tokens or adjusting invariant accounting.

**Impact:**

1. **Protocol Invariant Violation:** Directly breaks $(x + \Delta x) \cdot (y - \Delta y) \ge x \cdot y$. Pool reserves decrease without any price compensation, causing the invariant $k$ to decay over time. This is the exact root cause triggering failure in stateful fuzz tests (`statefulFuzz_constantProductFormulaStaysTheSameX`).
2. **Liquidity Drain:** An attacker can submit 9 micro-swaps (e.g. 10 wei of input tokens) and on the 10th swap extract an entire `1e18` of WETH or Pool Token, effectively draining honest liquidity providers' capital.
3. **MEV Exploitation:** Front-running bots can monitor the mempool when `swap_count == 9` and siphon the reward before legitimate users interact with the pool.

**Proof of Concept:**

An attacker executes 9 dust trades (100 wei each) and extracts an extra 1 WETH on the 10th swap:

```solidity
function test_PoC_InvariantBrokenAndReservesDrainedBySwapIncentive() public {
    vm.startPrank(attacker);
    poolToken.approve(address(pool), type(uint256).max);

    uint256 attackerWethBefore = weth.balanceOf(attacker);
    uint256 poolWethBefore = weth.balanceOf(address(pool));

    // Attacker executes 9 minimal dust trades
    for (uint256 i = 0; i < 9; i++) {
        pool.swapExactInput(poolToken, 100, weth, 0, uint64(block.timestamp));
    }

    // On the 10th swap, attacker extracts standard output + 1e18 free WETH
    pool.swapExactInput(poolToken, 100, weth, 0, uint64(block.timestamp));
    vm.stopPrank();

    uint256 attackerWethAfter = weth.balanceOf(attacker);
    uint256 poolWethAfter = weth.balanceOf(address(pool));

    // Attacker extracted > 1 WETH while spending negligible dust
    assertGt(attackerWethAfter - attackerWethBefore, 1e18);
    assertGt(poolWethBefore - poolWethAfter, 1e18);
}
```

**Recommended Mitigation:**

Remove the arbitrary swap reward mechanism from core AMM swap logic. If trader incentives are required, handle them through a dedicated external rewards contract funded separately:

```diff
--- a/src/TSwapPool.sol
+++ b/src/TSwapPool.sol
@@ -43,8 +43,6 @@ contract TSwapPool is ERC20 {
     IERC20 private immutable i_wethToken;
     IERC20 private immutable i_poolToken;
     uint256 private constant MINIMUM_WETH_LIQUIDITY = 1_000_000_000;
-    uint256 private swap_count = 0;
-    uint256 private constant SWAP_COUNT_MAX = 10;
 
@@ -396,11 +394,6 @@ contract TSwapPool is ERC20 {
             revert TSwapPool__InvalidToken();
         }
 
-        swap_count++;
-        if (swap_count >= SWAP_COUNT_MAX) {
-            swap_count = 0;
-            outputToken.safeTransfer(msg.sender, 1_000_000_000_000_000_000);
-        }
         emit Swap(
```

---

### [H-2] Incorrect Numerator Constant (10000 vs 1000) in `getInputAmountBasedOnOutput` Overcharges Traders by ~10x

**Description:**

In `TSwapPool.sol`, the pricing formula in `getInputAmountBasedOnOutput()` calculates the input tokens required to receive a given `outputAmount`:

```solidity
return
    ((inputReserves * outputAmount) * 10000) /
    ((outputReserves - outputAmount) * 997);
```

Under standard constant product AMM math with a 0.3% trading fee, the numerator multiplier must be `1000`, not `10000`.

**Impact:**

Every trader calling `swapExactOutput()` or using `sellPoolTokens()` is overcharged by a factor of approximately $10\times$. For example, purchasing 10 WETH in a 100/100 pool costs $\approx 111.4$ tokens instead of the mathematically correct $\approx 11.14$ tokens, causing immediate financial loss to traders.

**Proof of Concept:**

```solidity
function test_PoC_TenXFeeCalculationOvercharge() public view {
    uint256 inputReserves = 100e18;
    uint256 outputReserves = 100e18;
    uint256 outputAmount = 10e18;

    // Expected input under Uniswap CPAMM with 0.3% fee:
    uint256 expectedInputAmount = ((inputReserves * outputAmount * 1000) / 
        ((outputReserves - outputAmount) * 997)) + 1;

    // TSwap actual calculated input:
    uint256 actualInputAmount = pool.getInputAmountBasedOnOutput(outputAmount, inputReserves, outputReserves);

    // Actual input is ~10x greater than mathematically intended
    assertGt(actualInputAmount, expectedInputAmount * 9);
}
```

**Recommended Mitigation:**

Correct the numerator constant from `10000` to `1000` and add `+ 1` to round up in favor of pool solvency:

```diff
--- a/src/TSwapPool.sol
+++ b/src/TSwapPool.sol
@@ -291,7 +291,7 @@ contract TSwapPool is ERC20 {
         returns (uint256 inputAmount)
     {
         return
-            ((inputReserves * outputAmount) * 10000) /
-            ((outputReserves - outputAmount) * 997);
+            (((inputReserves * outputAmount) * 1000) /
+            ((outputReserves - outputAmount) * 997)) + 1;
     }
```

---

### [H-3] Inverted Call in `sellPoolTokens` Passes Input Amount as Desired Output, Causing Catastrophic Token Loss or Revert

**Description:**

The NatSpec documentation for `sellPoolTokens()` describes its purpose as allowing users to sell a specified `poolTokenAmount` of pool tokens to receive WETH:

```solidity
function sellPoolTokens(
    uint256 poolTokenAmount
) external returns (uint256 wethAmount) {
    return
        swapExactOutput(
            i_poolToken,
            i_wethToken,
            poolTokenAmount,
            uint64(block.timestamp)
        );
}
```

However, `swapExactOutput()` treats its 3rd argument as `outputAmount`. Passing `poolTokenAmount` causes the function to interpret the value as the desired *WETH output*, rather than the pool tokens being sold.

**Impact:**

When a user attempts to sell 10 Pool Tokens (`10e18`), the contract interprets this as "user wants to receive 10 WETH output". Combined with the 10x fee error, the user is charged $\approx 111.4$ Pool Tokens instead of 10. If the user lacks sufficient tokens or approval, the transaction reverts; if they possess them, they suffer catastrophic and unintended token deductions.

**Proof of Concept:**

```solidity
function test_PoC_SellPoolTokensInvertedLogic() public {
    poolToken.mint(user, 200e18);
    vm.startPrank(user);
    poolToken.approve(address(pool), type(uint256).max);

    uint256 poolTokenBalanceBefore = poolToken.balanceOf(user);
    // User intends to sell 10 pool tokens
    pool.sellPoolTokens(10e18);
    uint256 poolTokenBalanceAfter = poolToken.balanceOf(user);

    uint256 tokensDeducted = poolTokenBalanceBefore - poolTokenBalanceAfter;
    // Over 111 pool tokens were deducted instead of 10
    assertGt(tokensDeducted, 100e18);
    vm.stopPrank();
}
```

**Recommended Mitigation:**

Rewrite `sellPoolTokens` to invoke `swapExactInput()` rather than `swapExactOutput()`, and include slippage protection:

```diff
--- a/src/TSwapPool.sol
+++ b/src/TSwapPool.sol
@@ -363,13 +363,14 @@ contract TSwapPool is ERC20 {
      * @return wethAmount amount of WETH received by caller
      */
     function sellPoolTokens(
-        uint256 poolTokenAmount
+        uint256 poolTokenAmount,
+        uint256 minWethToReceive,
+        uint64 deadline
     ) external returns (uint256 wethAmount) {
         return
-            swapExactOutput(
+            swapExactInput(
                 i_poolToken,
-                i_wethToken,
                 poolTokenAmount,
-                uint64(block.timestamp)
+                i_wethToken,
+                minWethToReceive,
+                deadline
             );
     }
```

---

### [H-4] Hardcoded 18-Decimal Swap Reward in `_swap` Permanently Blocks All Swaps for Non-18 Decimal Token Pools (USDC, WBTC)

**Description:**

In `TSwapPool.sol`, `_swap()` attempts to transfer a hardcoded reward of `1_000_000_000_000_000_000` units of `outputToken`:

```solidity
outputToken.safeTransfer(msg.sender, 1_000_000_000_000_000_000);
```

While this corresponds to 1 token for an 18-decimal token, for tokens with fewer decimals (e.g. USDC with 6 decimals or WBTC with 8 decimals), this represents an astronomical quantity:
- USDC (6 decimals): `1e18` units = $1,000,000,000,000$ (1 Trillion) USDC.

**Impact:**

When a pool paired with a non-18 decimal token reaches 10 swaps where the non-18 decimal token is the `outputToken`, `safeTransfer()` attempts to transfer 1 trillion tokens. Because the pool reserves are vastly lower than 1 trillion tokens, the ERC20 transfer reverts due to insufficient balance. Because `swap_count` is 9, every subsequent swap attempting to purchase the token will hit this revert condition, causing permanent Denial of Service (DoS) and trapping remaining liquidity.

**Proof of Concept:**

```solidity
function test_PoC_Non18DecimalTokenCausesPermanentDoS() public {
    MockUSDC usdc = new MockUSDC(); // 6 decimals
    TSwapPool usdcPool = TSwapPool(factory.createPool(address(usdc)));

    usdc.mint(liquidityProvider, 10_000 * 1e6);
    weth.mint(liquidityProvider, 10e18);

    vm.startPrank(liquidityProvider);
    usdc.approve(address(usdcPool), type(uint256).max);
    weth.approve(address(usdcPool), type(uint256).max);
    usdcPool.deposit(10e18, 10e18, 10_000 * 1e6, uint64(block.timestamp));
    vm.stopPrank();

    weth.mint(user, 10e18);
    vm.startPrank(user);
    weth.approve(address(usdcPool), type(uint256).max);

    // First 9 swaps succeed
    for (uint256 i = 0; i < 9; i++) {
        usdcPool.swapExactInput(weth, 100, usdc, 0, uint64(block.timestamp));
    }

    // 10th swap attempts to transfer 1e18 USDC (1 trillion units) and reverts permanently
    vm.expectRevert();
    usdcPool.swapExactInput(weth, 100, usdc, 0, uint64(block.timestamp));
    vm.stopPrank();
}
```

**Recommended Mitigation:**

Eliminate the swap incentive transfer completely as recommended in **[H-1]**.

---

## Medium Severity Findings

### [M-1] Absence of `maxInputAmount` Slippage Protection in `swapExactOutput` Exposes Users to Extreme Capital Theft via Sandwich Attacks

**Description:**

In `TSwapPool.sol`, `swapExactOutput()` accepts only `inputToken`, `outputToken`, `outputAmount`, and `deadline`. It calculates `inputAmount` dynamically based on current pool reserves without a maximum bound.

**Impact:**

Traders have zero slippage protection. A malicious MEV searcher can sandwich the victim's transaction:
1. Front-run by swapping to severely deplete output reserves and inflate input reserves.
2. The victim's transaction executes at the manipulated exchange rate, consuming excessive input tokens.
3. Back-run by selling the output tokens back to the pool at the elevated price, extracting value directly from the victim.

**Proof of Concept:**

```solidity
function test_PoC_SwapExactOutputMissingSlippageProtection_SandwichAttack() public {
    poolToken.mint(user, 1000e18);
    poolToken.mint(attacker, 1000e18);

    // Initial expected cost for 5 WETH: ~52.79 Pool Tokens
    uint256 expectedInputCost = pool.getInputAmountBasedOnOutput(
        5e18,
        poolToken.balanceOf(address(pool)),
        weth.balanceOf(address(pool))
    );

    // Attacker front-runs by buying 40 WETH
    vm.startPrank(attacker);
    poolToken.approve(address(pool), type(uint256).max);
    pool.swapExactOutput(poolToken, weth, 40e18, uint64(block.timestamp));
    vm.stopPrank();

    // User executes transaction without slippage bound
    vm.startPrank(user);
    poolToken.approve(address(pool), type(uint256).max);
    uint256 userBalanceBefore = poolToken.balanceOf(user);
    pool.swapExactOutput(poolToken, weth, 5e18, uint64(block.timestamp));
    uint256 actualInputCost = userBalanceBefore - poolToken.balanceOf(user);
    vm.stopPrank();

    // User paid 700.89 Pool Tokens (>13x higher than initial expected 52.79)
    assertGt(actualInputCost, expectedInputCost * 3);
}
```

**Recommended Mitigation:**

Add a `maxInputAmount` parameter and revert if `inputAmount > maxInputAmount`:

```diff
--- a/src/TSwapPool.sol
+++ b/src/TSwapPool.sol
@@ -34,6 +34,7 @@ contract TSwapPool is ERC20 {
     );
     error TSwapPool__InvalidToken();
     error TSwapPool__OutputTooLow(uint256 actual, uint256 min);
+    error TSwapPool__InputTooHigh(uint256 actual, uint256 max);
     error TSwapPool__MustBeMoreThanZero();
 
@@ -340,6 +341,7 @@ contract TSwapPool is ERC20 {
         IERC20 inputToken,
         IERC20 outputToken,
         uint256 outputAmount,
+        uint256 maxInputAmount,
         uint64 deadline
     )
         public
@@ -355,6 +357,9 @@ contract TSwapPool is ERC20 {
             inputReserves,
             outputReserves
         );
+        if (inputAmount > maxInputAmount) {
+            revert TSwapPool__InputTooHigh(inputAmount, maxInputAmount);
+        }
 
         _swap(inputToken, inputAmount, outputToken, outputAmount);
     }
```

---

### [M-2] Unused `deadline` Parameter in `deposit` Fails to Enforce Transaction Expiration, Enabling Execution of Stale Mempool Transactions

**Description:**

In `TSwapPool.sol`, `deposit()` accepts a `uint64 deadline` parameter. However, **the `deadline` parameter is never used anywhere in the function body or modifier list**. Unlike `withdraw`, `swapExactInput`, and `swapExactOutput`, `deposit()` completely omits the `revertIfDeadlinePassed(deadline)` modifier.

The Solidity compiler explicitly flags this with:
```text
Warning (5667): Unused function parameter. Remove or comment out the variable name to silence this warning.
   --> src/TSwapPool.sol:117:9:
    |
117 |         uint64 deadline
    |         ^^^^^^^^^^^^^^^
```

**Impact:**

Because the `deadline` parameter is passed but never enforced, liquidity deposit transactions submitted with a deadline have no actual expiration. During network congestion, a deposit transaction submitted with a low gas fee can remain pending in the mempool indefinitely. Miners/validators or MEV bots can hold and execute the stale transaction hours or days later when pool reserve ratios and market prices have shifted substantially, inflicting unexpected slippage and severe impermanent loss on the liquidity provider.

**Proof of Concept:**

```solidity
function test_PoC_DepositMissingDeadlineCheck() public {
    vm.warp(100 days);
    uint64 pastDeadline = uint64(block.timestamp - 1 days);

    vm.startPrank(liquidityProvider);
    weth.approve(address(pool), 10e18);
    poolToken.approve(address(pool), 10e18);

    // Succeeds despite deadline being 1 day in the past
    pool.deposit(10e18, 0, 10e18, pastDeadline);
    vm.stopPrank();
}
```

**Recommended Mitigation:**

Add the `revertIfDeadlinePassed(deadline)` modifier to the `deposit()` function declaration:

```diff
--- a/src/TSwapPool.sol
+++ b/src/TSwapPool.sol
@@ -118,6 +118,7 @@ contract TSwapPool is ERC20 {
     )
         external
         revertIfZero(wethToDeposit)
+        revertIfDeadlinePassed(deadline)
         returns (uint256 liquidityTokensToMint)
     {
```

---

### [M-3] Unassigned Named Return Variable in `swapExactInput` Always Evaluates to Zero, Breaking Composability

**Description:**

In `TSwapPool.sol`, `swapExactInput()` declares a named return value `returns (uint256 output)`. The function computes `outputAmount` as an internal local variable, but never assigns it to `output` or provides an explicit `return` statement.

**Impact:**

External contracts, aggregator routers, and keeper bots integrating with `TSwapPool.swapExactInput` receive `0` as the return value even when the trade successfully transfers tokens. Smart contract integrations asserting non-zero returns or tracking returned balances will revert, breaking composability with the broader DeFi ecosystem.

**Proof of Concept:**

```solidity
function test_PoC_SwapExactInputReturnsZero() public {
    vm.startPrank(user);
    poolToken.approve(address(pool), 10e18);

    uint256 returnedOutput = pool.swapExactInput(poolToken, 10e18, weth, 0, uint64(block.timestamp));
    // Output returns 0 despite valid swap execution
    assertEq(returnedOutput, 0);
    vm.stopPrank();
}
```

**Recommended Mitigation:**

Assign `output = outputAmount;` before function completion or return `outputAmount` directly:

```diff
--- a/src/TSwapPool.sol
+++ b/src/TSwapPool.sol
@@ -321,5 +321,6 @@ contract TSwapPool is ERC20 {
         }
 
         _swap(inputToken, inputAmount, outputToken, outputAmount);
+        output = outputAmount;
     }
```

---

## Low Severity Findings

### [L-1] Swapped Arguments in `LiquidityAdded` Event Emission Corrupts Off-Chain Accounting

**Description:**

The `LiquidityAdded` event is declared as `(address indexed liquidityProvider, uint256 wethDeposited, uint256 poolTokensDeposited)`. However, in `_addLiquidityMintAndTransfer()`, it is emitted with parameter values inverted:

```solidity
emit LiquidityAdded(msg.sender, poolTokensToDeposit, wethToDeposit);
```

**Impact:**

Off-chain indexing services (The Graph, Dune Analytics, DeFi Llama) and web3 user interfaces ingest transposed token amounts, reporting WETH deposits as Pool Tokens and vice versa.

**Proof of Concept:**

```solidity
function test_PoC_LiquidityAddedEventSwappedParameters() public {
    ERC20Mock asymmetricToken = new ERC20Mock();
    TSwapPool asymPool = TSwapPool(factory.createPool(address(asymmetricToken)));
    weth.mint(liquidityProvider, 100e18);
    asymmetricToken.mint(liquidityProvider, 200e18);

    vm.startPrank(liquidityProvider);
    weth.approve(address(asymPool), 100e18);
    asymmetricToken.approve(address(asymPool), 200e18);

    vm.expectEmit(true, false, false, true, address(asymPool));
    emit LiquidityAdded(liquidityProvider, 200e18, 100e18);
    asymPool.deposit(100e18, 100e18, 200e18, uint64(block.timestamp));
    vm.stopPrank();
}
```

**Recommended Mitigation:**

Invert the argument order to match the event definition:

```diff
--- a/src/TSwapPool.sol
+++ b/src/TSwapPool.sol
@@ -193,7 +193,7 @@ contract TSwapPool is ERC20 {
         uint256 liquidityTokensToMint
     ) private {
         _mint(msg.sender, liquidityTokensToMint);
-        emit LiquidityAdded(msg.sender, poolTokensToDeposit, wethToDeposit);
+        emit LiquidityAdded(msg.sender, wethToDeposit, poolTokensToDeposit);
 
         // Interactions
```

---

### [L-2] `PoolFactory.createPool` Permits WETH/WETH Pairs and Zero Address Token Deployments

**Description:**

`PoolFactory.createPool()` lacks validation to ensure `tokenAddress != address(0)` and `tokenAddress != i_wethToken`.

**Impact:**

Users can deploy useless pools paired with `address(0)` or duplicate pairs of `WETH/WETH`. Any interaction with a WETH/WETH pool attempts to execute with `inputToken == outputToken`, triggering `TSwapPool__InvalidToken()` reverts and cluttering factory state with defunct contracts.

**Proof of Concept:**

```solidity
function test_PoC_PoolFactoryAllowsDuplicateWethPool() public {
    address wethPool = factory.createPool(address(weth));
    assertEq(factory.getPool(address(weth)), wethPool);
}
```

**Recommended Mitigation:**

Add validation checks rejecting zero address and WETH address:

```diff
--- a/src/PoolFactory.sol
+++ b/src/PoolFactory.sol
@@ -21,6 +21,8 @@ contract PoolFactory {
     error PoolFactory__PoolAlreadyExists(address tokenAddress);
     error PoolFactory__PoolDoesNotExist(address tokenAddress);
+    error PoolFactory__ZeroAddress();
+    error PoolFactory__CannotCreateWethPool();
 
@@ -47,6 +49,12 @@ contract PoolFactory {
     function createPool(address tokenAddress) external returns (address) {
+        if (tokenAddress == address(0)) {
+            revert PoolFactory__ZeroAddress();
+        }
+        if (tokenAddress == i_wethToken) {
+            revert PoolFactory__CannotCreateWethPool();
+        }
         if (s_pools[tokenAddress] != address(0)) {
             revert PoolFactory__PoolAlreadyExists(tokenAddress);
         }
```

---

### [L-3] `PoolFactory.createPool` Concatenates Token Name Instead of Symbol for LP Token Symbol

**Description:**

In `PoolFactory.sol`, the LP token symbol is defined as:

```solidity
string memory liquidityTokenSymbol = string.concat("ts", IERC20(tokenAddress).name());
```

**Impact:**

For tokens with lengthy names (e.g. DAI whose name is `"Dai Stablecoin"` and symbol is `"DAI"`), the LP symbol becomes `"tsDai Stablecoin"` rather than `"tsDAI"`, degrading user experience across wallets and block explorers.

**Recommended Mitigation:**

Use `.symbol()` instead of `.name()`:

```diff
--- a/src/PoolFactory.sol
+++ b/src/PoolFactory.sol
@@ -51,7 +51,7 @@ contract PoolFactory {
         string memory liquidityTokenName = string.concat("T-Swap ", IERC20(tokenAddress).name());
-        string memory liquidityTokenSymbol = string.concat("ts", IERC20(tokenAddress).name());
+        string memory liquidityTokenSymbol = string.concat("ts", IERC20(tokenAddress).symbol());
```

---

## Informational Findings

### [I-1] Missing Zero Address Validation in `PoolFactory` Constructor Risks Permanent Misconfiguration

**Description:**

The constructor in `PoolFactory.sol` sets `i_wethToken = wethToken` without checking `if (wethToken == address(0))`. If deployed with `address(0)`, every pool deployed by the factory will pair against `address(0)`, rendering the factory unusable.

**Recommended Mitigation:**

Add zero address check in constructor:

```solidity
constructor(address wethToken) {
    if (wethToken == address(0)) {
        revert PoolFactory__ZeroAddress();
    }
    i_wethToken = wethToken;
}
```

---

### [I-2] Unused Custom Error `PoolFactory__PoolDoesNotExist` Increases Bytecode Size

**Description:**

`PoolFactory.sol` declares `error PoolFactory__PoolDoesNotExist(address tokenAddress);` at line 22, but this error is never referenced or thrown anywhere in the contract.

**Recommended Mitigation:**

Remove the unused custom error from `PoolFactory.sol`.

---

### [I-3] Unused Storage Read `poolTokenReserves` in `deposit` Wastes Gas (Compiler Warning 2072)

**Description:**

In `TSwapPool.sol` line 131:

```solidity
uint256 poolTokenReserves = i_poolToken.balanceOf(address(this));
```

This local variable is never read or used in any subsequent lines of `deposit()`, triggering Solc compiler warning `Warning (2072): Unused local variable` and wasting gas on an unnecessary external call.

**Recommended Mitigation:**

Delete line 131 from `TSwapPool.sol`.

---

### [I-4] Unindexed Event Parameters in `PoolFactory.PoolCreated` and `TSwapPool.Swap` Prevent Efficient Log Filtering

**Description:**

Events should index up to 3 address/topic parameters to allow lightweight filtering and querying by off-chain indexers. Several events in the protocol omit the `indexed` keyword on critical address parameters:
1. `PoolFactory.PoolCreated`: Neither `tokenAddress` nor `poolAddress` is indexed.
2. `TSwapPool.Swap`: `tokenIn` and `tokenOut` addresses are not indexed.

**Recommended Mitigation:**

Add `indexed` keyword to address parameters in `PoolFactory.sol` and `TSwapPool.sol`.

---

### [I-5] Strict Equality Comparison in `revertIfZero` Modifier

**Description:**

`TSwapPool.sol` modifier `revertIfZero` uses a strict equality check `if (amount == 0)` flagged by Slither (`incorrect-equality`).

**Recommended Mitigation:**

Document strict equality intentionality or use defensive comparison `amount <= 0`.

---

### [I-6] Erroneous Mathematical Explanation in NatSpec / Comments Misleads Developers

**Description:**

In `TSwapPool.sol` lines 132-143, inline comments claim $weth / poolTokens = k$. In Constant Product AMMs ($x \cdot y = k$), the invariant is multiplication, NOT division ($x / y = k$). The ratio of reserves represents instantaneous spot price, not the invariant $k$.

**Recommended Mitigation:**

Update comments to correctly describe the constant product invariant $x \cdot y = k$.

---

### [I-7] Redundant Wrapper Function `totalLiquidityTokenSupply()` Adds Bytecode Overhead

**Description:**

`TSwapPool.sol` defines a wrapper function `totalLiquidityTokenSupply()` that simply returns `totalSupply()`. Because `TSwapPool` inherits from OpenZeppelin's `ERC20`, `totalSupply()` is already public.

**Recommended Mitigation:**

Remove `totalLiquidityTokenSupply()` and call `totalSupply()` directly.

---

### [I-8] Unnamed Magic Numbers Obscure Business Logic and Contribute to Math Errors

**Description:**

Across `TSwapPool.sol`, numeric literals such as `997`, `1000`, `10000`, `1_000_000_000_000_000_000`, and `1e18` are hardcoded directly into arithmetic expressions without constant declarations, directly contributing to finding [H-2].

**Recommended Mitigation:**

Define named constants such as `FEE_DENOMINATOR = 1000;`, `FEE_NUMERATOR = 997;`, and `ONE_TOKEN = 1e18;`.

---

### [I-9] Private Function Declarations Preceding Public View Functions Violates Solidity Style Guide

**Description:**

In `TSwapPool.sol`, private functions `_swap()` and `_isUnknown()` are placed before public view functions, violating Solidity Style Guide layout conventions.

**Recommended Mitigation:**

Reorder functions according to standard visibility ordering (external, public, internal, private).

---

### [I-10] License Identifier Discrepancy Between Protocol (GPL-3.0) and Dependencies (MIT)

**Description:**

`PoolFactory.sol` and `TSwapPool.sol` specify `// SPDX-License-Identifier: GNU General Public License v3.0`, whereas imported OpenZeppelin contracts use `MIT`. GPL-3.0 has strong reciprocal copyleft terms that may impose licensing constraints on downstream integrators.

**Recommended Mitigation:**

Confirm that GPL-3.0 aligns with the protocol distribution roadmap.

---

### [I-11] Unused Function Parameter `deadline` in `deposit` Triggers Compiler Warning (5667)

**Description:**

In `TSwapPool.sol` line 117, `deposit()` accepts `uint64 deadline` as a parameter, but the parameter is never referenced or checked anywhere within the function body or modifier list, triggering Solc compiler warning `Warning (5667): Unused function parameter`.

*(Note: For the security impact of missing deadline enforcement against stale mempool transactions, see finding [M-2]).*

**Recommended Mitigation:**

Add the `revertIfDeadlinePassed(deadline)` modifier to enforce expiration (as described in [M-2]), or remove the parameter if deadline checking is not desired.

---

# Test Suite Quality & Mutation Testing Review

Following Phase 5.4 of The Tincho Method, an **Automated Mutation Testing Runner** (`scripts/mutation_runner.py`) was executed against the codebase to evaluate test sensitivity:

$$\text{Mutation Score} = \left( \frac{\text{Killed Mutants}}{\text{Total Mutants}} \right) \times 100\%$$

- **Total Tactical Mutants:** 16 (operator inversions, math alterations, fee bypasses, boundary deletions)
- **Original Client Test Suite Score:** **31.2%** (Only 5 of 16 mutants killed; **11 Mutants Survived!**)
- **Combined Suite with Audit PoCs Score:** **100.0%** (16 of 16 mutants killed)

Surviving mutants in the original test suite revealed that fee calculations, deadline checks, and deposit/withdrawal slippage boundaries were completely untested by the client test suite.

---

# General Recommendations

1. **Adopt FREI-PI and CEI Standards:** Complete all state balance updates before making external token transfers. Never introduce side-effect token giveaways inside core AMM swap paths.
2. **Decimal Standardization:** Ensure tokens with decimals other than 18 (e.g. USDC with 6 decimals) are handled with proper decimal scaling or validated upon pool creation.
3. **Incorporate ReentrancyGuard:** Guard all external entrypoints (`deposit`, `withdraw`, `swapExactInput`, `swapExactOutput`) with OpenZeppelin's `ReentrancyGuard` to prevent reentrancy via ERC777 tokens.
4. **Continuous Stateful Invariant Testing:** Maintain Foundry invariant fuzz suites testing constant product maintenance, solvency, and token ratios across thousands of randomized interaction sequences in CI/CD pipelines.
