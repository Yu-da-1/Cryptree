from flask import Flask, request
from cryptography.fernet import Fernet
import os
import ipfshttpclient
#import logging
#logging.basicConfig(filename='error.log', level=logging.DEBUG)


app = Flask(__name__)

node_files = {}  # 管理するノードのファイル {node_id: [file_id, ...], ...}
nodes = {}  # 管理するノードとその親ノード {node_id: parent_node_id, ...}
node_permissions = {}

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

#ノードの移動
@app.route('/nodes/<int:node_id>', methods=['PUT'])
def move_node(node_id):
    new_parent_node_id = request.form.get('new_parent_node_id')
    #node_idと新しい親node_idに基づいて移動させる
    if node_id not in nodes:
        return{"error": "No such node exists"}, 400
    
    nodes[node_id] = new_parent_node_id

    moved_node_info = {"node_id": node_id, "new_parent_node": new_parent_node_id}
    return moved_node_info, 200

#ノードの削除
@app.route('/nodes/<int:node_id>', methods=['DELETE'])
def delet_node(node_id):
    #node_idに基づいて削除処理
    if node_id not in nodes:
        return {"error": "No such node exists"}, 400
    del nodes[node_id]

    delete_success = {"node_id": node_id, "status": "delete"}
    return delete_success, 200

#ファイルの追加
@app.route('/nodes/<int:node_id>/files', methods=['POST'])
def upload_file_to_node(node_id):
    if 'file' not in request.files:
        return "No 'file' key in request.files",400

    file = request.files['file']
    file_content = file.read()

    # ファイルの暗号化
    encrypted_file_content = cipher_suite.encrypt(file_content)

    # IPFSにアップロード
    client = ipfshttpclient.connect('/ip4/127.0.0.1/tcp/5001/http')
    res = client.add_bytes(encrypted_file_content)
    file_id = res

    # ノードが持つファイルのリストに追加
    if node_id not in node_files:
        node_files[node_id] = []
    node_files[node_id].append(file_id)

    return {'file_id': file_id}, 200


@app.route('/nodes/<int:node_id>/files/<file_id>', methods=['GET'])
def download_file_from_node(node_id, file_id):
    #ノードがファイルを持っていることを確認
    if node_id not in node_files or file_id not in node_files[node_id]:
        return {"error": "File not found on this node"}, 404
    
    #IPFSからダウンロード
    client = ipfshttpclient.connect('/ip4/127.0.0.1/tcp/5001/http')
    encypted_file_content = client.cat(file_id)

    #ファイルの復号化
    file_content = cipher_suite.decrypt(encypted_file_content)
    return {'file_content': file_content.decode()}, 200

    file_data = {}
    return file_data

@app.route('/nodes/<int:node_id>/permissions', methods=['PUT'])
def change_node_permissions(node_id):
    user_id = request.form.get('user_id')
    permission = request.form.get('permission')

    if node_id not in node_permissions:
        node_permissions[node_id] = {'owner': [], 'reader': []}
    if permission not in ['owner', 'reader']:
        return {"error": "Invalid permisson type"}, 400
    
    if user_id not in node_permissions[node_id][permission]:
        node_permissions[node_id][permission].append(user_id)

    return {'node_id': node_id, 'user_id':user_id, 'permission':permission}, 200

if __name__ == '__main__':
    app.run(port=5000)