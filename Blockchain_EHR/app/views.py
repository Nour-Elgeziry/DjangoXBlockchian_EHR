import json
from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from web3 import Web3

#ganache address
ganache_url = "hTTP://127.0.0.1:7545"

#setting up web3 to use ganache url
web3 = Web3(Web3.HTTPProvider(ganache_url))
#print(web3.eth.blockNumber)

#set deafault account
web3.eth.defaultAccount = web3.eth.accounts[0]

#deployes contract address and abi
contract_address = web3.toChecksumAddress("0x86134c6bBeA25Db0d89852E645a14b2a13FdC336") 
contract_abi = json.loads('[{"inputs":[],"name":"retrieve","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"setValue","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"num","type":"uint256"}],"name":"store","outputs":[],"stateMutability":"nonpayable","type":"function"}]')
#setting the contract
contract = web3.eth.contract(address=contract_address, abi=contract_abi)

#call store function from contract
tx_hash = contract.functions.store(7).transact()
#wait for transaction reciept
web3.eth.waitForTransactionReceipt(tx_hash)
#retrieve the stored number
print(contract.functions.retrieve().call())


#functions that carry different transactions
def index(request):
    return HttpResponse("Hello, world. You're at the Blockchain EHR website.")