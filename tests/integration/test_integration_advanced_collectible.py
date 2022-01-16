from brownie import network
import pytest, time
from scripts.helpful_scripts import LOCAL_BLOCKCHAIN_ENVIRONMENTS, get_account, get_contract
from scripts.advancedCollectible.deploy_and_create import deploy_and_create

def test_can_create_advanced_collectible_integration():
    # deploy the contract
    # create an NFT
    # get a random breed back
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for rinkeby network testing")
    # Act
    advanced_collectible, creation_tx = deploy_and_create()
    # wait for the chainlink node to report back
    time.sleep(60)
    breed = advanced_collectible.events["breedAssigned"]["breed"]

    # assert
    assert advanced_collectible.tokenCounter() == 1
    assert advanced_collectible.tokenIdToBreed(0) == breed