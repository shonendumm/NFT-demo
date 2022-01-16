from brownie import network
import pytest
from scripts.helpful_scripts import LOCAL_BLOCKCHAIN_ENVIRONMENTS, get_account, get_contract
from scripts.advancedCollectible.deploy_and_create import deploy_and_create

def test_can_create_advanced_collectible():
    # deploy the contract
    # create an NFT
    # get a random breed back
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing")
    # Act
    advanced_collectible, creation_tx = deploy_and_create()
    requestId = creation_tx.events["requestedCollectible"]["requestId"]
    # Since we're testing locally, we need to mock the vrf_coordinator call back
    random_number = 777
    get_contract("vrf_coordinator").callBackWithRandomness(
        requestId, random_number, advanced_collectible, {"from": get_account()}
        )
    # assert
    assert advanced_collectible.tokenCounter() == 1
    assert advanced_collectible.tokenIdToBreed(0) == random_number % 3