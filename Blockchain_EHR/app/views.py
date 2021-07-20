import json
from django.shortcuts import render

''' Create your views here. '''
from django.http import HttpResponse
from web3 import Web3

'''ganache address'''
ganache_url = "hTTP://127.0.0.1:7545"

'''setting up web3 to use ganache url'''
web3 = Web3(Web3.HTTPProvider(ganache_url))
#print(web3.eth.blockNumber)

'''set deafault account'''
web3.eth.defaultAccount = web3.eth.accounts[0]
print('user account', web3.eth.defaultAccount)

'''setting the contract'''
contract_address = web3.toChecksumAddress("0xA6830C68ae385F22Ac29385e0818a66B6a23cE03") 
contract_abi = json.loads('[{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"Patients","outputs":[{"internalType":"string","name":"userName","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getPatientUsername","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"string","name":"_userName","type":"string"}],"name":"registeringPatientUsername","outputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"string","name":"","type":"string"}],"stateMutability":"nonpayable","type":"function"}]')
contract = web3.eth.contract(address=contract_address, abi=contract_abi)

'''call register patient function'''
tx_hash = contract.functions.registeringPatientUsername('Nour').transact()
'''wait for transaction reciept'''
web3.eth.waitForTransactionReceipt(tx_hash)
''' get the username'''
print(contract.functions.getPatientUsername().call())





'''functions that carry different transactions'''
def index(request):
    return HttpResponse("Hello, world. You're at the Blockchain EHR website.")


