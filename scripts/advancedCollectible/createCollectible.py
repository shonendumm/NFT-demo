from scripts.helpful_scripts import fund_with_link, get_account, OPENSEA_URL, get_contract
from brownie import AdvancedCollectible, config, network

# untill: https://youtu.be/M576WGiDBdQ?t=39753
# untill https://youtu.be/M576WGiDBdQ?t=39042

# upload image/json file to IPFS

def main():
    account = get_account()
    advanced_collectible = AdvancedCollectible[-1]
    fund_with_link(advanced_collectible.address)
    tx = advanced_collectible.createCollectible({"from": account})
    tx.wait(1)
    print("Collectible created!")
