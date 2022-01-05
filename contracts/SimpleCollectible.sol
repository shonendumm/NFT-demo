// SPDX-License-Identifier: MIT

pragma solidity 0.6.6;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";

contract SimpleCollectible is ERC721 {

    uint256 public tokenCounter;

    constructor () public ERC721 ("Doggie", "DOG"){
        // initialize tokenCounter to 0
        tokenCounter = 0;
    }


    function createCollectible(string memory tokenURI) public returns (uint256) {
        // use tokenCounter as an id for each created token
        uint256 newTokenId = tokenCounter;
        // use _safeMint inherited from ERC721 contract to mint a token
        _safeMint(msg.sender, newTokenId);
        // add tokenURI to get token metadata from IPFS
        _setTokenURI(newTokenId, tokenURI);
        tokenCounter = tokenCounter + 1;
        return newTokenId;
    }

}