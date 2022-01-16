from brownie import accounts, network, config, MockV3Aggregator, Contract, VRFCoordinatorMock, LinkToken
from web3 import Web3

LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["hardhat", "development", "ganache"]
FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork", "mainnet-fork-dev"] 

DECIMALS = 8
STARTING_PRICE = 200000000000 # 2000 * 10**8 , 1 eth = 2000 usd

OPENSEA_URL = "https://testnets.opensea.io/assets/{}/{}"

def get_account(index=None, id=None):
    if index:
        return accounts[index]
    if id:
        return accounts[id]
    if (
        network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS 
        or network.show_active() in FORKED_LOCAL_ENVIRONMENTS
    ):
        return accounts[0]
    # using metamask wallet
    return accounts.add(config["wallets"]["from_key"])

contract_to_mock = {
    "eth_usd_price_feed": MockV3Aggregator,
    "vrf_coordinator": VRFCoordinatorMock,
    "link_token": LinkToken
}

def get_contract(contract_name):
    """ This function will grab the contract addresses from 
    brownie config if defined, otherwise, it will deploy
    a mock version of that contract and return that contract.
    """
    contract_type = contract_to_mock[contract_name]
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        if len(contract_type) <= 0:
            deploy_mocks()
        contract = contract_type[-1]
    # Else not on local, but on forked mainnet or rinkeby
    else:
        contract_address = config["networks"][network.show_active()][contract_name] 
        # we use the address and ABI in order to get the contract
        # import Contract from brownie which has a from_abi function
        contract = Contract.from_abi(contract_type._name, contract_address, contract_type.abi)
        # MockV3Aggregator.abi , MockV3Aggregator._name
    return contract



def deploy_mocks(decimals=DECIMALS, starting_price=STARTING_PRICE):
    account = get_account()
    print(f"The active network is {network.show_active()}")
    print("Deploying Mocks...")
    MockV3Aggregator.deploy(decimals, starting_price, {"from": account})
    # print(f"Mock price feed deployed at {mock_price_feed.address}!")
    # linkToken, no constructor
    link_token = LinkToken.deploy({"from": account})   
    # constuctor needs address linkAddress
    VRFCoordinatorMock.deploy(link_token.address, {"from": account})
    print("Mocks deployed!")

def fund_with_link(contract_address, account=None, link_token=None, amount=Web3.toWei(1, "ether")):
    account = account if account else get_account()
    link_token = link_token if link_token else get_contract("link_token")
    # we are going to transfer link token to the contract_address
    tx = link_token.transfer(contract_address, amount, {"from": account})

    # The above works but sometimes some contracts don't have the function (e.g. to transfer) but we can interact with them as interfaces. Here:
    #  Example LinkToken interface: https://github.com/smartcontractkit/chainlink-mix/blob/master/interfaces/LinkTokenInterface.sol
    # see above on Contract.from_abi which is another way to get the contract
    #  this method works with interface if the contract is not available
    # link_token_contract = interface.LinkTokenInterface(link_token.address)
    # tx = link_token_contract.transfer(contract_address, amount, {"from": account})
    tx.wait(1)
    print("Fund contract with Link token!")
    return tx