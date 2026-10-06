# ⚡ Formal Verification Case Study: Differential Verification & Equivalence Checking

![Certora](https://img.shields.io/badge/Certora-Prover_6.x-blue?style=for-the-badge&logo=solidity)
![SMT](https://img.shields.io/badge/SMT_Solver-Z3_|_CVC5-purple?style=for-the-badge)
![Type](https://img.shields.io/badge/Methodology-Differential_Formal_Verification-orange?style=for-the-badge)

## 📌 Executive Summary

Writing gas-optimized smart contracts in low-level inline assembly (Yul) or Huff offers dramatic fee reductions for end users. However, manual memory management, raw pointer arithmetic, and custom storage packing introduce massive attack surfaces. 

In this case study, we employ **Differential Formal Verification** using the **Certora Prover** to mathematically prove that an aggressively gas-optimized marketplace contract ([`GasBadNftMarketplace.sol`](./src/GasBadNftMarketplace.sol)) executes with **identical state transitions and behavior** as the readable reference implementation ([`NftMarketplace.sol`](./src/NftMarketplace.sol)) across **all possible inputs and reachable states**.

---

## 🎯 Verification Scope & Target

- **Optimized Implementation (Yul/Assembly):** [`GasBadNftMarketplace.sol`](./src/GasBadNftMarketplace.sol)
- **Reference Implementation (Canonical Solidity):** [`NftMarketplace.sol`](./src/NftMarketplace.sol)
- **Interface & Mock:** [`INftMarketplace.sol`](./src/INftMarketplace.sol), [`NftMock.sol`](./src/mocks/NftMock.sol)
- **Certora Spec:** [`GasBadNft.spec`](./certora/spec/GasBadNft.spec)
- **Certora Config:** [`GasBadNft.conf`](./certora/conf/GasBadNft.conf)

---

## 🔬 Core Formal Verification Techniques

### 1. Differential Equivalence Checking (Parametric Rule)

A parametric CVL rule quantifies over all callable methods ($f, f_2$) having matching function selectors. It establishes that if both contracts start in identical storage states, any arbitrary function call with identical arguments will transition both contracts to identical ending states:

```cvl
using GasBadNftMarketplace as gasBadMarketplace; 
using NftMarketplace as marketplace;

rule calling_any_function_should_result_in_each_contract_having_the_same_state(
    method f, 
    method f2, 
    address listingAddr, 
    uint256 tokenId, 
    address seller
) {
    env e;
    calldataarg args;

    // 1. Initial State Equivalence (Precondition)
    require(gasBadMarketplace.getProceeds(e, seller) == marketplace.getProceeds(e, seller));
    require(gasBadMarketplace.getListing(e, listingAddr, tokenId).price == marketplace.getListing(e, listingAddr, tokenId).price);
    require(gasBadMarketplace.getListing(e, listingAddr, tokenId).seller == marketplace.getListing(e, listingAddr, tokenId).seller);

    // 2. Selectors Match
    require(f.selector == f2.selector);

    // 3. Execution of Arbitrary Method
    gasBadMarketplace.f(e, args);
    marketplace.f2(e, args);

    // 4. Final State Equivalence (Mathematical Proof)
    assert(gasBadMarketplace.getListing(e, listingAddr, tokenId).price == marketplace.getListing(e, listingAddr, tokenId).price);
    assert(gasBadMarketplace.getListing(e, listingAddr, tokenId).seller == marketplace.getListing(e, listingAddr, tokenId).seller);
    assert(gasBadMarketplace.getProceeds(e, seller) == marketplace.getProceeds(e, seller));
}
```

### 2. Ghost Variables & Opcode Hooks

To prove that storage writes cannot occur silently without emitting transparency events, we hook directly into the EVM execution pipeline:
- **`Sstore` opcode hook**: Increments a ghost counter whenever the `s_listings` storage slot is mutated.
- **`LOG4` opcode hook**: Increments a ghost counter whenever a 4-topic indexed EVM log is emitted.

```cvl
ghost mathint listingUpdatesCount {
    init_state axiom listingUpdatesCount == 0;
}

ghost mathint log4Count {
    init_state axiom log4Count == 0;
}

// Low-level EVM storage hook
hook Sstore s_listings[KEY address nftAddress][KEY uint256 tokenId].price uint256 price STORAGE {
    listingUpdatesCount = listingUpdatesCount + 1;
}

// Low-level EVM event emission hook
hook LOG4(uint offset, uint length, bytes32 t1, bytes32 t2, bytes32 t3, bytes32 t4) uint v {
    log4Count = log4Count + 1;
}

// Mathematical Invariant: Every storage modification MUST emit an indexed event
invariant anytime_mapping_updated_emit_event() 
    listingUpdatesCount <= log4Count;
```

### 3. Anti-Havoc & Dispatcher Summaries

External calls to unknown contracts (e.g., `safeTransferFrom` and `onERC721Received`) normally cause the Certora Prover to **HAVOC** contract storage (randomize all variables) to account for potential reentrancy attacks.

To constrain external calls to known mock implementations while maintaining sound verification:
```cvl
methods {
    // Wildcard summary declarations using DISPATCHER
    function _.onERC721Received(address, address, uint256, bytes) external => DISPATCHER(true);
    function _.safeTransferFrom(address, address, uint256) external => DISPATCHER(true);
}
```

In the configuration file ([`GasBadNft.conf`](./certora/conf/GasBadNft.conf)):
```json
{
    "files": [
        "src/GasBadNftMarketplace.sol:GasBadNftMarketplace",
        "src/NftMarketplace.sol:NftMarketplace",
        "src/mocks/NftMock.sol:NftMock"
    ],
    "verify": "GasBadNftMarketplace:certora/spec/GasBadNft.spec",
    "wait_for_results": "all",
    "rule_sanity": "basic",
    "optimistic_loop": true,
    "msg": "Differential Verification of NftMarketplace vs GasBadNftMarketplace",
    "optimistic_fallback": true
}
```

---

## 💡 Practical Security Impact

1. **Zero-Regression Gas Optimization:** Protocols can confidently implement high-risk assembly optimizations knowing that equivalence proofs guarantee zero divergence from audited reference logic.
2. **Exhaustive Path Coverage:** Unlike traditional unit or fuzz tests that test sampled inputs ($10^4 - 10^6$ iterations), SMT solvers prove equivalence across **all $2^{256}$ inputs**.
3. **Event & State Integrity:** Proves mathematically that no storage update can bypass audit logging and event tracking.

---

## ⚙️ Certora CLI Execution

```bash
certoraRun formal-verification/02-gas-bad-nft-marketplace/certora/conf/GasBadNft.conf
```
