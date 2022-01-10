// SPDX-License-Identifier: MIT
pragma solidity 0.6.6;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@chainlink/contracts/src/v0.6/VRFConsumerBase.sol";

contract AdvancedCollectible is ERC721, VRFConsumerBase {

    uint256 public tokenCounter;
    bytes32 public keyhash;
    uint256 public fee;
    enum Breed{PUG, SHIBA_INU, ST_BERNARD}
    mapping(uint256 => Breed) public tokenIdToBreed;
    mapping(bytes32 => address) public requestIdToSender;
    // as a best practice, we emit an event whenever the mapping is updated:
    // indexed keyword makes it easier to search for this event
    event requestedCollectible(bytes32 indexed requestId, address requester);
    event breedAssigned(uint256 indexed tokenId, Breed breed);


    // refer to chainlink docs for VRFCoordinator's parameters
    constructor (address _vrfCoordinator, address _linkToken, bytes32 _keyhash, uint256 _fee) public VRFConsumerBase(_vrfCoordinator, _linkToken) ERC721 ("Dogie", "DOG") 
    {
        tokenCounter = 0;
        keyhash = _keyhash;
        fee = _fee;
    }

    // we can do away with tokenURI parameter here because we only know it when we got the random number. Breed is decided by random number.
    function createCollectible() public returns (bytes32){
        // we want the request id 
        bytes32 requestId = requestRandomness(keyhash, fee);
        requestIdToSender[requestId] = msg.sender;
        emit requestedCollectible(requestId, msg.sender);
    }

    // fulfillRandomness will be called by VRFCoordinator at Chainlink
    function fulfillRandomness(bytes32 requestId, uint256 randomNumber) internal override {
        Breed breed = Breed(randomNumber % 3);
        uint256 newTokenId = tokenCounter;
        tokenIdToBreed[newTokenId] = breed;
        emit breedAssigned(newTokenId, breed);

        address owner = requestIdToSender[requestId];
        _safeMint(owner, newTokenId);

        // we skip this _setTokenURI for now, for simplicity...
        // _setTokenURI(newTokenId, tokenURI);
        tokenCounter = tokenCounter + 1;
    }

    function setTokenURI(uint256 tokenId, string memory _tokenURI) public {
        // need 3 tokenURIs for the 3 breeds
        // we want to let only the owner of the tokenId mint set the tokenURI
        // checks that msgSender is the owner
        require(_isApprovedOrOwner(_msgSender(), tokenId), "ERC721: Caller is not owner nor approved.");
        _setTokenURI(tokenId, _tokenURI);

    }

}
