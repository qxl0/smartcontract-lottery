# 0.019
# 190000000000000000
from brownie import Lottery, accounts, config , network
from web3 import Web3
from scripts.deploy_lottery import deploy_lottery 

def test_get_entrance_fee():
  lottery = deploy_lottery() 
  entrance_fee = lottery.getEntranceFee()
  expected_entrance_fee = Web3.toWei(0.025, "ether")
  assert expected_entrance_fee == entrance_fee