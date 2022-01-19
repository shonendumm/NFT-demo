from brownie import network, AdvancedCollectible
from scripts.helpful_scripts import OPENSEA_URL, getBreed, get_account

dog_metadata_dic = {
    "PUG": "https://ipfs.io/ipfs/QmRdJZrUfCRo4jzeMmexq1h4hex25wg5PNcqmUhVo9Ytsa?filename=1-PUG.json",
    "SHIBA_INU": "https://ipfs.io/ipfs/QmdryoExpgEQQQgJPoruwGJyZmz6SqV4FRTX1i73CT3iXn?filename=1-SHIBA_INU.json",
    "ST_BERNARD": "https://ipfs.io/ipfs/QmSgxDaBSzacDQpL66vQQxPLNAXbb5xwjWHFoum5Co3wJN?filename=0-ST_BERNARD.json",
}

def main():
    print(f"Working on {network.show_active()}")
    advanced_collectible = AdvancedCollectible[-1]
    number_of_collectibles = advanced_collectible.tokenCounter()
    print(f"You have {number_of_collectibles} tokenIds!")

    for token_id in range(number_of_collectibles):
        breed = getBreed(advanced_collectible.tokenIdToBreed(token_id))
        # check that the token_id's URI is not empty
        if not advanced_collectible.tokenURI(token_id).startswith("https://"):
            print(f"Setting tokenURI of {token_id}")
            set_tokenURI(token_id, advanced_collectible, dog_metadata_dic[breed])

def set_tokenURI(token_id, nft_contract, tokenURI):
    account = get_account()
    tx = nft_contract.setTokenURI(token_id, tokenURI, {"from": account})
    tx.wait(1)
    print(f"You can view your NFT at {OPENSEA_URL.format(nft_contract.address, token_id)}")
    print("Please wait up to 20 minutes, and hit the refresh metadata button")