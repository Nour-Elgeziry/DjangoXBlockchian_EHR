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
contract_address = web3.toChecksumAddress("0xF9d78006A806c35cef9F32A508e97A4F271C826b") 
contract_abi = json.loads('[{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"Patients","outputs":[{"internalType":"string","name":"name","type":"string"},{"internalType":"string","name":"dob","type":"string"},{"internalType":"string","name":"postCode","type":"string"},{"internalType":"string","name":"bloodType","type":"string"},{"internalType":"string","name":"weight","type":"string"},{"internalType":"string","name":"height","type":"string"},{"internalType":"string","name":"insurance","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getAllergies","outputs":[{"internalType":"string[]","name":"","type":"string[]"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getInsurance","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getMedication","outputs":[{"internalType":"string[]","name":"","type":"string[]"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getPatientInfo","outputs":[{"internalType":"string","name":"","type":"string"},{"internalType":"string","name":"","type":"string"},{"internalType":"string","name":"","type":"string"},{"internalType":"string","name":"","type":"string"},{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"string","name":"_allergies","type":"string"}],"name":"setAllergies","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"string","name":"_insurance","type":"string"}],"name":"setInsurance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"string","name":"_medication","type":"string"}],"name":"setMedication","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"string","name":"_name","type":"string"},{"internalType":"string","name":"_dob","type":"string"},{"internalType":"string","name":"_postCode","type":"string"},{"internalType":"string","name":"_weight","type":"string"},{"internalType":"string","name":"_height","type":"string"}],"name":"setingPatientInfo","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"}]')
                            
contract = web3.eth.contract(address=contract_address, abi=contract_abi)

'''call register patient function'''
tx_hash = contract.functions.setingPatientInfo('Nour', '07.07.1999', 'CV14GJ', '80', '183').transact()
'''wait for transaction reciept'''
web3.eth.waitForTransactionReceipt(tx_hash)
''' get the username'''
print('returned user info', contract.functions.getPatientInfo().call())

''' set  patient medication'''
tx_hash = contract.functions.setMedication('panadol').transact()
'''wait for transaction reciept'''
web3.eth.waitForTransactionReceipt(tx_hash)
''' get the username'''
print('returned user medication', contract.functions.getMedication().call())



'''functions that carry different transactions'''
def index(request):
    return HttpResponse("Hello, world. You're at the Blockchain EHR website.")


