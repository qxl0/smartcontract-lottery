# 0.019
# 190000000000000000
from brownie import Lottery, accounts, config , network, exceptions
from scripts.helpful_scripts import LOCAL_BLOCKCHAIN_ENVIRONMENTS
from web3 import Web3
from scripts.deploy_lottery import deploy_lottery 
from scripts.helpful_scripts import get_account
import pytest

def test_get_entrance_fee():
  if (network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS):
    pytest.skip()
  lottery = deploy_lottery() 
  entrance_fee = lottery.getEntranceFee()
  expected_entrance_fee = Web3.toWei(0.025, "ether")
  assert expected_entrance_fee == entrance_fee


def test_cant_enter_unless_started():
  if (network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS):
    pytest.skip()
  lottery = deploy_lottery() 
  with pytest.raises(exceptions.VirtualMachineError):
    lottery.enter({"from": get_account(), "value": lottery.getEntranceFee()})

