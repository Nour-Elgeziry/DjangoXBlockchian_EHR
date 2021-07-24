import json
from django.shortcuts import render, redirect

'''forms'''
from .forms import *

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

    context ={
        'name': name,
        'dob': dob,
        'postCode': postCode,
        'height' : height,
        'weight' : weight,
        'insurance': user_insurance,
        'medication': user_medication,
        'alergies': user_allergies
    }
    return render(request, 'app/home.html', context)

def registerPatient(request):
    print('registering patient')
    if request.method == 'POST':
        form = PatientForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            name = form.cleaned_data['name']
            dob = form.cleaned_data['dob']
            postCode = form.cleaned_data['postCode']
            height = form.cleaned_data['height']
            weight = form.cleaned_data['weight']
            '''call smartcontract setingPatientInfo function'''
            tx_hash = contract.functions.setingPatientInfo(name, dob, postCode, height, weight).transact()
            '''wait for transaction reciept'''
            web3.eth.waitForTransactionReceipt(tx_hash)
            return redirect('/')
   
    form = PatientForm()
    return render(request, 'app/registerPatientPage.html', {'form':form})
    
    
    return redirect('/')

def registerInsurance(request):
    print('registering insurance')
    if request.method == 'POST':
        form = InsuranceForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            insuranceNumber = form.cleaned_data['insuranceNumber']
            '''call smartcontract setInsurance function'''
            tx_hash = contract.functions.setInsurance(insuranceNumber).transact()
            '''wait for transaction reciept'''
            web3.eth.waitForTransactionReceipt(tx_hash)
            return redirect('/')
    
    form = InsuranceForm()
    return render(request, 'app/registerInsurancePage.html', {'form':form})
    
def registerMedication(request):
    print('registering medication')
    if request.method == 'POST':
        form = MedicationForm(request.POST)
        if form.is_valid():
            medicine = form.cleaned_data['medicine']
            '''call smartcontract setMedication function'''
            tx_hash = contract.functions.setMedication(medicine).transact()
            '''wait for transaction reciept'''
            web3.eth.waitForTransactionReceipt(tx_hash)
            return redirect('/')
    form = MedicationForm()
    return render(request, 'app/registerMedicationPage.html', {'form':form})
    
    

def registerAlergies(request):
    print('registering allergies')
    if request.method == 'POST':
        form = AlergiesForm(request.POST)
        if form.is_valid():
            alergy = form.cleaned_data['alergy']
            '''call smartcontract setAllergies function'''
            tx_hash = contract.functions.setAllergies(alergy).transact()
            '''wait for transaction reciept'''
            web3.eth.waitForTransactionReceipt(tx_hash)
            return redirect('/')
    form = AlergiesForm()
    return render(request, 'app/registerAlergiesPage.html', {'form':form})


   
    

