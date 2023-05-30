from flask import Flask, request
from cryptography.fernet import Fernet
import os
import ipfshttpclient
#import logging
#logging.basicConfig(filename='error.log', level=logging.DEBUG)


app = Flask(__name__)

key = Fernet.generate_key()
cipher_suite = Fernet(key)

@app.route('/')
def home():
    return 'Hello World'

@app.route('/upload_endpoint', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No 'file' key in request.files",400

    file = request.files['file']
    filename = file.filename
    file_content = file.read()

    #ファイルの暗号化
    encrypted_file_content = cipher_suite.encrypt(file_content)

    #暗号化したファイルの保存
    with open(os.path.join('C:\\Users\\isiyu\\CryptreeFolder\\save', filename), 'wb') as f:
        f.write(encrypted_file_content)

    return 'File uploaded and encrypted successfully', 200

#ノードの追加
@app.route('/nodes', methods=['POST'])
def create_node():
    parent_node_id = request.form.get('parent_node_id')
    node_name = request.form.get('node_name')

    #IPFSに追加する
    client = ipfshttpclient.connect('/ip4/127.0.0.1/tcp/5001/http')
    res = client.add(node_name)
    node_id = res['Hash']

    return {"node_id": node_id}, 201

if __name__ == '__main__':
    app.run(port=5000)