// SPDX-License-Identifier: SEE LICENSE IN LICENSE
pragma solidity ^0.8.20;

import {MathMasters} from "./MathMasters.sol";

contract CompactCodeBase {
    function mulWadUp(uint256 x, uint256 y) external returns (uint256) {
        return MathMasters.mulWadUp(x, y);
    }
}
