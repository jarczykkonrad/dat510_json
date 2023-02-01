# encryptedcommunicator
Need to install to run the code:

pip install des
pip install shared-memory-dict
pip install localStoragePy
sudo pip3 install Werkzeug==0.16.0
pip install flask_cors
pip install flask-restful
python -m pip install requests

Content:

folder templates includes three html files: getmsg, getpub, home
communicator.py is a webserver communicator, using REST_API
TO RUN: first run REST_API file, as it works as db for communicator.py
please run Alice twice separately, select "1" on first terminal and "2" on the other one.
on your browser open http://localhost:5000/getpub as one side and http://localhost:80/getpub in another tab.
They should exchange public keys automatically and they will be able to communicate.
For received messages click on inbox.
