import json
from django.shortcuts import render, redirect

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
contract_address = web3.toChecksumAddress("0x1dD4989338241041beE8922F9aaF2714461E3747") 
contract_abi = json.loads('[{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"Patients","outputs":[{"internalType":"string","name":"name","type":"string"},{"internalType":"string","name":"dob","type":"string"},{"internalType":"string","name":"postCode","type":"string"},{"internalType":"string","name":"bloodType","type":"string"},{"internalType":"string","name":"weight","type":"string"},{"internalType":"string","name":"height","type":"string"},{"internalType":"string","name":"insurance","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"deleteMedication","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"getAllergies","outputs":[{"internalType":"string[]","name":"","type":"string[]"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getInsurance","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getMedication","outputs":[{"internalType":"string[]","name":"","type":"string[]"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getPatientInfo","outputs":[{"internalType":"string","name":"","type":"string"},{"internalType":"string","name":"","type":"string"},{"internalType":"string","name":"","type":"string"},{"internalType":"string","name":"","type":"string"},{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"string","name":"_allergies","type":"string"}],"name":"setAllergies","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"string","name":"_insurance","type":"string"}],"name":"setInsurance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"string","name":"_medication","type":"string"}],"name":"setMedication","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"string","name":"_name","type":"string"},{"internalType":"string","name":"_dob","type":"string"},{"internalType":"string","name":"_postCode","type":"string"},{"internalType":"string","name":"_weight","type":"string"},{"internalType":"string","name":"_height","type":"string"}],"name":"setingPatientInfo","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"}]')
                        
contract = web3.eth.contract(address=contract_address, abi=contract_abi)


def home(request):
    print('Inside home')
    user_info = contract.functions.getPatientInfo().call()
    name = user_info[0]
    dob =  user_info[1]
    postCode = user_info[2]
    height = user_info[3]
    weight = user_info[4]

    user_insurance = contract.functions.getInsurance().call()
    user_medication = contract.functions.getMedication().call()
    user_allergies = contract.functions.getAllergies().call()

    print('user medication', user_medication)

    context ={
        'name': name,
        'dob': dob,
        'postCode': postCode,
        'height' : height,
        'weight' : weight,
        'insurance': user_insurance,
        'medication': user_medication,
        'allergies': user_allergies
    }
    return render(request, 'app/home.html', context)

def registerPatientPage(request):
    return render(request, 'app/registerPatientPage.html')

def registerInsurancePage(request):
    return render(request, 'app/registerInsurancePage.html')

def registerMedicationPage(request):
    return render(request, 'app/registerMedicationPage.html')

def registerAlergiesPage(request):
    return render(request, 'app/registerAlergiesPage.html')

def registerPatient(request):
    print('registering patient')
    #tx_hash = contract.functions.setingPatientInfo('Nour', '07.07.1999', 'CV14GJ', '80', '183').transact()
    '''wait for transaction reciept'''
    #web3.eth.waitForTransactionReceipt(tx_hash)
    return redirect('/')

def registerInsurance(request):
    print('registering insurance')
    #tx_hash = contract.functions.setInsurance(str(insurance_no)).transact()
    '''wait for transaction reciept'''
    #web3.eth.waitForTransactionReceipt(tx_hash)
    return redirect('/')

def registerMedication(request):
    print('registering medication')
    #tx_hash = contract.functions.setMedication('medication').transact()
    '''wait for transaction reciept'''
    #web3.eth.waitForTransactionReceipt(tx_hash)
    return redirect('/')

def registerAllergies(request):
    print('registering allergies')
    #tx_hash = contract.functions.setAllergies('allergy').transact()
    '''wait for transaction reciept'''
    #web3.eth.waitForTransactionReceipt(tx_hash)
    return redirect('/')

