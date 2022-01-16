##  Doggie (DOG) NFT named Pug
NFT Doggie minted, available to view via OpenSea testnet
https://testnets.opensea.io/assets/0x6E0C3760670875De758f15EEDdC8d311F274Cea6/0

### Deploy SimpleCollectible contract to testnet
brownie run scripts/deploy_and_create.py --network rinkeby

### Note
The code written here is only compatible with older versions of solidity and openzeppelin contracts.

The new openzeppelin contract's implementation of ERC721, i.e. its functions/ABI are different, and requires a newer version of solidity.

Hence, depending on which release of openzeppelin you're importing/inheriting for ERC721, we need to look at the documentation for the ABI/functions.

### How does opensea keep track of newly minted NFTs? (including testnets)

See https://ethereum.stackexchange.com/questions/106942/what-process-does-opensea-use-to-get-all-the-nfts-of-a-wallet/106949 

"OpenSea saves all the addresses of the ERC721 contract through EtherScan, then loads the contract to look up the NFT and adds a listen on the contract so it knows when someone is creating an NFT or moving an NFT!

While you're doing this, Opensea updates the NFT information to its own server, so when you're done, go to Opensea and you'll see your NFT.Sometimes it's slow, like when the metadata isn't showing, you can click sync." Or refresh webpage.

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

1. Upload an image to IPFS (or pinata) ourselves
2. Perhaps make the contract ownable (only the owner can mint), and verifiably scarce/ random. 