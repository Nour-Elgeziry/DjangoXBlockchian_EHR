import json
from django.shortcuts import render, redirect

'''forms'''
from .forms import *

''' Create your views here. '''
from django.http import HttpResponse
from web3 import Web3
from eth_account.messages import encode_defunct
from django.contrib import messages
import time

'''ganache address'''
ganache_url = "hTTP://127.0.0.1:7545"

'''setting up web3 to use ganache url'''
web3 = Web3(Web3.HTTPProvider(ganache_url))

'''setting the contract'''
contract_address = web3.toChecksumAddress("0x1dD4989338241041beE8922F9aaF2714461E3747") 
contract_abi = json.loads('[{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"Patients","outputs":[{"internalType":"string","name":"name","type":"string"},{"internalType":"string","name":"dob","type":"string"},{"internalType":"string","name":"postCode","type":"string"},{"internalType":"string","name":"bloodType","type":"string"},{"internalType":"string","name":"weight","type":"string"},{"internalType":"string","name":"height","type":"string"},{"internalType":"string","name":"insurance","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"deleteMedication","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"getAllergies","outputs":[{"internalType":"string[]","name":"","type":"string[]"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getInsurance","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getMedication","outputs":[{"internalType":"string[]","name":"","type":"string[]"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getPatientInfo","outputs":[{"internalType":"string","name":"","type":"string"},{"internalType":"string","name":"","type":"string"},{"internalType":"string","name":"","type":"string"},{"internalType":"string","name":"","type":"string"},{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"string","name":"_allergies","type":"string"}],"name":"setAllergies","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"string","name":"_insurance","type":"string"}],"name":"setInsurance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"string","name":"_medication","type":"string"}],"name":"setMedication","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"string","name":"_name","type":"string"},{"internalType":"string","name":"_dob","type":"string"},{"internalType":"string","name":"_postCode","type":"string"},{"internalType":"string","name":"_weight","type":"string"},{"internalType":"string","name":"_height","type":"string"}],"name":"setingPatientInfo","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"}]')
contract = web3.eth.contract(address=contract_address, abi=contract_abi)

isAuthuorized = False

def login(request):
    print('Veryfying User Info')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            '''getting user info '''
            account_address  = form.cleaned_data['address']
            account_private_key = form.cleaned_data['privateKey']
            print('address and pk', account_address, account_private_key)

            msg = 'A message to be hashed'
            message = encode_defunct(text=msg)
            signed_message = web3.eth.account.sign_message(message, private_key=account_private_key)
            print('returned signature', signed_message)
            '''recover function returns address of message sender'''
            account_sent_from = web3.eth.account.recover_message(message, signature=signed_message.signature)
            print('returned actuall address', account_sent_from)
            '''validate sender == current user'''
            if account_address == account_sent_from:
                web3.eth.defaultAccount = account_address
                global isAuthuorized
                isAuthuorized  = True
                return redirect('/home')              
            else:
                messages.error(request,'Account wrong try again')
                
                         
    form = LoginForm()
    return render(request, 'app/login.html',{'form':form})

def home(request):
    if isAuthuorized != True:
        return redirect('/')
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
    if isAuthuorized != True:
        return redirect('/')
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
            return redirect('/home')
   
    form = PatientForm()
    return render(request, 'app/registerPatientPage.html', {'form':form})
    
    
    return redirect('/')

def registerInsurance(request):
    if isAuthuorized != True:
        return redirect('/')
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
            return redirect('/home')
    
    form = InsuranceForm()
    return render(request, 'app/registerInsurancePage.html', {'form':form})
    
def registerMedication(request):
    if isAuthuorized != True:
        return redirect('/')
    print('registering medication')
    if request.method == 'POST':
        form = MedicationForm(request.POST)
        if form.is_valid():
            medicine = form.cleaned_data['medicine']
            '''call smartcontract setMedication function'''
            tx_hash = contract.functions.setMedication(medicine).transact()
            '''wait for transaction reciept'''
            web3.eth.waitForTransactionReceipt(tx_hash)
            return redirect('/home')
    form = MedicationForm()
    return render(request, 'app/registerMedicationPage.html', {'form':form})
    
    

def registerAlergies(request):
    if isAuthuorized != True:
        return redirect('/')
    print('registering allergies')
    if request.method == 'POST':
        form = AlergiesForm(request.POST)
        if form.is_valid():
            alergy = form.cleaned_data['alergy']
            '''call smartcontract setAllergies function'''
            tx_hash = contract.functions.setAllergies(alergy).transact()
            '''wait for transaction reciept'''
            web3.eth.waitForTransactionReceipt(tx_hash)
            return redirect('/home')
    form = AlergiesForm()
    return render(request, 'app/registerAlergiesPage.html', {'form':form})


   
    

