##  Doggie (DOG) NFT named Pug
NFT Doggie minted, available to view via OpenSea testnet
https://testnets.opensea.io/assets/0x6E0C3760670875De758f15EEDdC8d311F274Cea6/0

### Deploy SimpleCollectible contract to testnet
brownie run scripts/simpleCollectible/deploy_and_create.py --network rinkeby

### Note
The code written here is only compatible with older versions of solidity and openzeppelin contracts. The new openzeppelin contract's implementation of ERC721, i.e. its functions/ABI are different, and requires a newer version of solidity.

Hence, depending on which release of openzeppelin you're importing/inheriting for ERC721, we need to look at the documentation for the ABI/functions.

### How does opensea keep track of newly minted NFTs? (including testnets)
See https://ethereum.stackexchange.com/questions/106942/what-process-does-opensea-use-to-get-all-the-nfts-of-a-wallet/106949 

OpenSea looks up all addresses on Etherscan, notes down the ERC721 contracts, adds a listener on the contract so it knows when someone is creating an NFT or moving an NFT, and then records the wallet address of the person holding the NFT.

It stores these information in its own database. So when you connect your wallet to it, it retrieves your wallet address from its database, plus all the NFTs it had recorded as belonging to your wallet address.

Why?
Because your wallet (address) doesn't really store your NFTs.
It's the NFT contract that records your wallet address. Every NFT contract has a balanceOf(address) and ownerOf(tokenId) function which are essentially based on recording your wallet address to the number of coins it holds (i.e. balanceOf) and recording your wallet address to a particular token (i.e. ownerOf).


### What is the amount of ETH and gas fees to deploy the contract and mint the NFT on rinkeby?
View the example txn details at https://rinkeby.etherscan.io/address/0xf0Da5D362fF2031CdACeAd3fE1a55bFf7288d5Ec

Deploy contract: 
Transaction fee 0.001833897014671176 eth
Gas price 0.000000001000000008 eth

Mint pug:
Transaction fee 0.000253904002031232 eth
Gas price 0.000000001000000008 eth

Total about 6.51 USD, but this is for rinkeby testnet where gas prices are free/low

### How to store image data in tokenURI on chain?

Refer to NFTonChain repo

## AdvancedCollectible

1. Upload an image to IPFS (or pinata) via cli
2. Verifiably scarce/ random creation of NFT Dog breed via Chainlink VRFCoordinator
3. Add metadata to NFT token

### Deploy AdvancedCollectible contract to testnet

`brownie run scripts/AdvancedCollectible/deploy_and_create.py --network rinkeby`

This deploys the contract to rinkeby testnet and creates 1 NFT (random breed based on verified random number returned from Chainlink)

`brownie run scripts/AdvancedCollectible/createCollectible.py --network rinkeby`

This creates 1 NFT from the deployed contract (also of random breed)

`brownie run scripts/AdvancedCollectible/create_metadata.py --network rinkeby`

This retrieves number of NFTs minted and creates the metadata for them.
Note: On the testnet, it may be slower to mint the NFT as it takes time for Chainlink to return the random number, which our contract uses to assign the breed.

After confirming that the NFTs have been minted, e.g. reading tokenCounter on the verified contract on rinkeby.etherscan should return >0 , i.e. number of NFTs minted.

We can proceed to set the tokenURI for each NFT.

`brownie run scripts/AdvancedCollectible/set_tokenURI.py --network rinkeby`

This sets the tokenURI for each NFT to point to a json file hosted on IPFS. The JSON file contains the name, description, image_uri, and attributes information of the particular NFT.