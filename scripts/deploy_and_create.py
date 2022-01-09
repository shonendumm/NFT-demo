# Untill here: https://youtu.be/M576WGiDBdQ?t=36806
# Prepare to add tokenURI metadata when creating collectible
from scripts.helpful_scripts import get_account, SimpleCollectible


# upload image/json file to IPFS, but this is from Patrick's tutorial
sample_token_uri = 'https://ipfs.io/ipfs/Qmd9MCGtdVz2miNumBHDbvj8bigSgTwnr4SbyH6DNnpWdt?filename=0-PUG.json'

# {NFT_contract_address}/{tokenId}
opensea_url = "https://testnets.opensea.io/assets/{}/{}"



def main():
    account = get_account()
    simple_collectible = SimpleCollectible.deploy({"from": account})
    tx = simple_collectible.createCollectible(sample_token_uri, {"from": account})
    tx.wait(1)
    print(f"Congrats! You can view your NFT now at {opensea_url.format(simple_collectible.address, simple_collectible.tokenCounter() - 1)}")
    print("Please wait 20 minutes, and hit the refresh metadata button")