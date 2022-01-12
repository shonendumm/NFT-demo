##  Doggie (DOG) NFT named Pug
NFT Doggie minted, available to view via OpenSea testnet
https://testnets.opensea.io/assets/0x9cEe94b1E4E62ae5F227Fd45cEBf380469f522d4/0 

### Deploy SimpleCollectible contract
brownie run scripts/deploy_and_create.py --network rinkeby


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

Total about 6.51 USD, but this is for rinkeby testnet when gas prices are free/low

### How to store image data in tokenURI on chain?

Refer to the etherOrcs files in /img.

The etherOrcs NFT has base64 encoded its JSON tokenURI
We can decode it using https://www.base64decode.org/ to get its tokenURI and attributes in json.

Then, to decode the image attribute at "image", 
take the base64 encoded part and decode it using
 https://www.base64decode.org again
then pass the <svg ... > code to
https://mybyways.com/blog/convert-svg-to-png-using-your-browser
it will generate the png.

Hence, to encode the tokenURI, we can do the reverse:
1. Convert your png to svg
2. Encode the svg to base64
3. put the encoded svg in the image attribute in the tokenURI json
4. Encode the json to base64
5. pass the encoded string as the tokenURI when minting