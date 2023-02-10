import flask
import Ass2_part1
from shared_memory_dict import SharedMemoryDict
from localStoragePy import localStoragePy
from flask import Flask, render_template, redirect, url_for, request
from requests import put, get
app= Flask(__name__)

localStorage = localStoragePy('Alice/Bob', 'json')

# shared message, for both Alice and Bob keeping only last message
messages = SharedMemoryDict(name='messages', size=1024)

# for image sending
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


@app.route('/getpub')
def getpub():

    # generating all keys

    if name == "Alice":
        if get('http://127.0.0.1:8000/db/public_keys/PUa').json() == None:
            if get('http://127.0.0.1:8000/db/variables/g').json() != None:
                PRa, PUa, g, prime_number_1, prime_number_2 = Ass2_part1.getpub_Alice(
                    int(get('http://127.0.0.1:8000/db/variables/g').json()), int(get('http://127.0.0.1:8000/db/variables/prime_number_1').json()),
                    int(get('http://127.0.0.1:8000/db/variables/prime_number_1').json()))
            else:
                PRa, PUa, g, prime_number_1, prime_number_2 = Ass2_part1.getpub_Alice()
                put('http://127.0.0.1:8000/db/variables/g', data={"g": g}).json()
                put('http://127.0.0.1:8000/db/variables/prime_number_1', data={"prime_number_1": prime_number_1}).json()
                put('http://127.0.0.1:8000/db/variables/prime_number_2', data={"prime_number_2": prime_number_2}).json()

            #sharing public key
            put('http://127.0.0.1:8000/db/public_keys/PUa', data={"PUa":PUa}).json()
            #saving private key in local storage
            localStorage.setItem('PRa', PRa)

            # if there are no other public keys in this shared variable, program will stop and wait for other public keys
            if get('http://127.0.0.1:8000/db/public_keys/PUb').json()==None:
                return render_template('getpub.html', name=name)

        Kab_Alice = Ass2_part1.computing_mod(int(get('http://127.0.0.1:8000/db/public_keys/PUb').json()),
                                       int(localStorage.getItem('PRa')), int(get('http://127.0.0.1:8000/db/variables/prime_number_1').json()))
        #localStorage.setItem('Kab_Alice', Kab_Alice)
        secret_key_Alice = Ass2_part1.bbs(Kab_Alice, (int(get('http://127.0.0.1:8000/db/variables/prime_number_1').json())*int(get('http://127.0.0.1:8000/db/variables/prime_number_2').json())))
        #for this assignment Kab key is stored for both ALice and Bob on the same variable in memory
        localStorage.setItem('secret_key_Alice', secret_key_Alice)


    elif name == "Bob":
        if get('http://127.0.0.1:8000/db/public_keys/PUb').json() == None:
            if get('http://127.0.0.1:8000/db/variables/g').json() != None:
                PRb, PUb, g, prime_number_1, prime_number_2 = Ass2_part1.getpub_Bob(
                    int(get('http://127.0.0.1:8000/db/variables/g').json()), int(get('http://127.0.0.1:8000/db/variables/prime_number_1').json()),
                    int(get('http://127.0.0.1:8000/db/variables/prime_number_1').json()))
            else:
                PRb, PUb, g, prime_number_1, prime_number_2 = Ass2_part1.getpub_Bob()
                put('http://127.0.0.1:8000/db/variables/g', data={"g": g}).json()
                put('http://127.0.0.1:8000/db/variables/prime_number_1', data={"prime_number_1": prime_number_1}).json()
                put('http://127.0.0.1:8000/db/variables/prime_number_2', data={"prime_number_2": prime_number_2}).json()

            put('http://127.0.0.1:8000/db/public_keys/PUb', data={"PUb":PUb}).json()
            localStorage.setItem('PRb', PRb)

            if get('http://127.0.0.1:8000/db/public_keys/PUa').json()==None:
                return render_template('getpub.html', name=name)

        Kab_Bob = Ass2_part1.computing_mod(int(get('http://127.0.0.1:8000/db/public_keys/PUa').json()),
                                       int(localStorage.getItem('PRb')), int(get('http://127.0.0.1:8000/db/variables/prime_number_1').json()))
        #localStorage.setItem('Kab_Bob', Kab_Bob)

        secret_key_Bob = Ass2_part1.bbs(Kab_Bob, (int(get('http://127.0.0.1:8000/db/variables/prime_number_1').json()) * int(get('http://127.0.0.1:8000/db/variables/prime_number_2').json())))
        localStorage.setItem('secret_key_Bob', secret_key_Bob)

    return redirect(url_for('main', name = name))


@app.route('/<name>', methods=['GET', 'POST'])
def main(name):
    if request.method == "POST":
        if request.form.get("plaintext"):
            if name=='Alice':
                cipher = Ass2_part1.encryption_DES(request.form.get('plaintext'), localStorage.getItem('secret_key_Alice'))
                messages["Alice"]=cipher
                #put('http://127.0.0.1:8000/db/messages/Alice', data={"Alice": str(cipher)}).json()
            else:
                cipher = Ass2_part1.encryption_DES(request.form.get('plaintext'), localStorage.getItem('secret_key_Bob'))
                messages["Bob"]=cipher
                #put('http://127.0.0.1:8000/db/messages/Bob', data={"Bob": str(cipher)}).json()

    return render_template('home.html', name=name)



@app.route('/<name>/getmsg')
def getmsg(name):
    if "Bob" in messages.keys():
        if name == 'Alice':
            return render_template('getmsg.html', name=name,
                                   plaintext=Ass2_part1.decryption_DES(messages["Bob"],
                                   localStorage.getItem('secret_key_Alice')).decode('utf-8'))
    if 'Alice' in messages.keys:
        if name == "Bob":
            return render_template('getmsg.html', name=name,
                                   plaintext=Ass2_part1.decryption_DES(messages["Alice"],
                                   localStorage.getItem('secret_key_Bob')).decode('utf-8'))

    return render_template('getmsg.html', name=name, plaintext="No messages")



if __name__ == '__main__':
    while True:
        who = int(input("Who are You? 1: Alice or 2: Bob, write the number: "))
        if who == 1:
            name = "Alice"
            app.run(host='localhost', port=80)
            break
        elif who==2:
            name = "Bob"
            app.run(host='localhost')
            break
