import logging
from flask import Flask, request, render_template
import datetime
import hashlib

# Configure logging to only print ERROR level logs
logging.basicConfig(level=logging.ERROR)

class Block:
    blockNo = 0
    data = None
    next = None
    nonce = 0
    previous_hash = 0
    timestamp = datetime.datetime.now()
    
    def __init__(self, data, patient_id, hospital_name, diagnosis, eth_address):
        self.data = data
        self.patientID = patient_id
        self.hospitalName = hospital_name
        self.diagnosis = diagnosis
        self.ethAddress = eth_address
        
    def hash(self):
        h = hashlib.sha256()
        h.update(
            str(self.nonce).encode('utf8') +
            str(self.data).encode('utf8') +
            str(self.previous_hash).encode('utf8') +
            str(self.timestamp).encode('utf8') +
            str(self.patientID).encode('utf8') +
            str(self.hospitalName).encode('utf8') +
            str(self.diagnosis).encode('utf8') +
            str(self.ethAddress).encode('utf8')
        )
        return h.hexdigest()
        
    def __str__(self):
        return (
            f"Block Hash: {self.hash()}\n"
            f"Patient ID: {self.patientID}\n"
            f"Hospital Name: {self.hospitalName}\n"
            f"Diagnosis: {self.diagnosis}\n"
            f"ETH Address: {self.ethAddress}\n"
            f"Block Data: {self.data}\n"
            f"Hashes: {self.nonce}\n"
            "--------------"
        )

class Blockchain:
    diff = 10
    maxNonce = 2**32
    target = 2**(256 - diff)
    
    block = Block("Genesis block", "Genesis", "Genesis", "Genesis", "Genesis")
    dummy = head = block
    
    def add(self, block):
        block.previous_hash = self.block.hash() 
        self.block.next = block
        self.block = self.block.next
    
    def mine(self, block):
        for n in range(self.maxNonce):
            if int(block.hash(), 16) <= self.target:
                self.add(block)
                return block.patientID, block.data, block.hospitalName, block.diagnosis, block.ethAddress
            else:
                block.nonce += 1

app = Flask(__name__)
blockchain = Blockchain()
patient_records = []

@app.route('/')
def my_form():
    return render_template('index.html', patient_list=patient_records)

@app.route('/', methods=['POST'])
def my_form_post():
    PatientID = request.form.get('PatientID')
    Details = request.form.get('Details')
    HospitalName = request.form.get('HospitalName')
    Diagnosis = request.form.get('Diagnosis')
    
    if PatientID and Details and HospitalName and Diagnosis:
        block = Block(Details, PatientID, HospitalName, Diagnosis, "")
        pid, details, hospital_name, diagnosis, _ = blockchain.mine(block)
        patient_records.append([pid, details, hospital_name, diagnosis])
        
        # Print the new patient record to the terminal
        print("\nNew Patient Record:")
        print(f"Patient ID: {pid}")
        print(f"Details: {details}")
        print(f"Hospital Name: {hospital_name}")
        print(f"Diagnosis: {diagnosis}")
        print(f"Block Number: {block.blockNo}")
        print(f"Block Hash: {block.hash()}")
        
    return render_template('index.html', patient_list=patient_records)

@app.route('/connect_metamask', methods=['GET'])
def connect_metamask():
    # You can handle MetaMask connection logic here
    return render_template('index.html', patient_list=patient_records)

if __name__ == "__main__":
    app.run(debug=True)
