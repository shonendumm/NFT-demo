from scripts.helpful_scripts import fund_with_link, get_account, OPENSEA_URL, get_contract
from brownie import AdvancedCollectible, config, network


# untill https://youtu.be/M576WGiDBdQ?t=39042

# upload image/json file to IPFS

def main():
    deploy_and_create()

def deploy_and_create():
    account = get_account()
    # AdvancedCollectible needs the following for constructor:
    # address _vrfCoordinator, address _linkToken, bytes32 _keyhash, uint256 _fee (rinkeby)
    advanced_collectible = AdvancedCollectible.deploy(
        get_contract("vrf_coordinator"),
        get_contract("link_token"),
        config["networks"][network.show_active()]["key_hash"],
        config["networks"][network.show_active()]["fee"],        
        {"from": account}, publish_source = config["networks"][network.show_active()].get("verify", False))
    
    # fund the contract with link tokens
    fund_with_link(advanced_collectible.address)
    # call createCollectible which will requestRandomness and pay fee (0.1) using funded link tokens
    tx = advanced_collectible.createCollectible({"from": account})
    tx.wait(1)
    # print(f"Congrats! You can view your NFT now at {OPENSEA_URL.format(advanced_collectible.address, advanced_collectible.tokenCounter() - 1)}")
    # tokenCounter() is the tokenID, but after every mint, it's already +1, so we need to -1 to get the actual minted tokenID
    print(f"AdvancedCollectible deployed at {advanced_collectible.address}")
    print("Please wait 20 minutes for VRFCoordinator to callback fulfillrandomness")
    return advanced_collectible, tx
