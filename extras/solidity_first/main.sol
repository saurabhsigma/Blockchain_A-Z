// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract SimpleStorage {
    // State Variables
    uint256 public storedData;
    address public owner;
    // Events
    event DataUpdated(uint256 newData);
    // Modifiers
    modifier onlyOwner() {
        require(msg.sender == owner, "Caller is not the owner");
        _;
    }
    // Constructor
    constructor() {
        owner = msg.sender;
    }
    // Functions
    function set(uint256 x) public onlyOwner {
        storedData = x;
        emit DataUpdated(x);
    }
    function get() public view returns (uint256) {
        return storedData;
    }
}