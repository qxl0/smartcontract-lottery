from brownie import ( accounts, network, config, MockV3Aggregator, Contract, 
  VRFCoordinatorMock, LinkToken)
from web3 import Web3

FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork", "mainnet-fork-dev"]
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]
DECIMALS = 8
STARTING_PRICE = 200000000000


def get_account(index=None, id=None):
    # accounts[0]
    # accounts.add("env")
    # accounts.load("id")
    if index:
      return accounts[index]
    
    if id:
      return accounts.load(id)

    if (
        network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS
        or network.show_active() in FORKED_LOCAL_ENVIRONMENTS
    ):
        return accounts[0]
      
    return accounts.add(config["wallets"]["from_key"])


# def deploy_mocks():
#     print(f"The actiev network is {network.show_active()}")
#     print("Deploying Mocks...")
#     if len(MockV3Aggregator) <= 0:
#         MockV3Aggregator.deploy(
#             DECIMALS, Web3.toWei(STARTING_PRICE, "ether"), {"from": get_account()}
#         )
contract_to_mock = {"eth_usd_price_feed": MockV3Aggregator,
"vrf_coordinator": VRFCoordinatorMock, "link_token": LinkToken}

def get_contract(contract_name):
  """This function will grab the contract address from the brownie config
  if defined, otherwise, 
  it will deploy a mock version of that contract, and return that mock contract.
    Args:
      contract_name(string)
    Returns:
      brownie.network.contract.ProjectContract: The most deployed
      version of this contract.
  """
  contract_type = contract_to_mock[contract_name]
  if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
    if len(contract_type) <= 0:
      deploy_mocks()
    contract = contract_type[-1]
  else:
    contract_address = config["networks"][network.show_active()][contract_name]
    contract = Contract.from_abi(contract_type._name, contract_address, contract_type.abi)
  return contract

DECIMALS = 8
STARTING_PRICE = 200000000000

def deploy_mocks(decimals=DECIMALS, initial_value=STARTING_PRICE):
  account = get_account()
  MockV3Aggregator.deploy(decimals, initial_value, {"from": account})
  link_token = LinkToken.deploy({"from": account})
  VRFCoordinatorMock.deploy(link_token, {"from": account})
  print("Deployed!")