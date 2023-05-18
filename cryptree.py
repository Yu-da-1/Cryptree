from cryptography.fernet import Fernet

class Encryption:
    #鍵生成
    def __init__(self):
        self.key = Fernet.generate_key()
        self.cipher_suite = Fernet(self.key)

    #引数として与えられた文字列データをバイト列にエンコードし、データを暗号化
    def encrypt(self, data: str) -> bytes:
        cipher_text = self.cipher_suite.encrypt(data.encode())
        return cipher_text
    
    #暗号化されたデータを引数としてうけとり復号化
    def decrypt(self, cipher_text: bytes) -> str:
        plain_text = self.cipher_suite.decrypt(cipher_text)
        return plain_text.decode()
    
#Cryptree構造のクラス作成
#一意の暗号化キーとCryptographic Linkを管理する
class CryptreeNode:
    def __init__(self, node_type: str, name: str):
        self.node_type = node_type
        self.name = name
        self.encryption = Encryption()
        self.parent = None
        self.children = {}

    #子ノードを追加した際の親ノード('self')を現在のノードに設定
    def add_child(self, child_node):
        self.children[child_node.name] = child_node
        child_node.parent = self
        self.data = None

    #ノードがファイルタイプであるか確認し、データをファイルノードに書き込む
    def write_data(self, data: str):
            if self.node_type =='file':
                self.data = self.encryption.encrypt(data) #暗号化して保存
            else:
                raise Exception("Cannot write data to a directory")
    #ノードがファイルタイプであるか確認し、ファイルを読み込む(ディレクトリから読み取れない)
    def read_data(self) -> str:
            if self.node_type == 'file':
                return self.encryption.decrypt(self.data) #復号化して返す
            else:
                raise Exception("Cannnot read data from a directory")

class Cryptree:
    #Cryptreeクラスのインスタンスの作成
    def __init__(self, root: CryptreeNode):
        self.root = root

    # パス文字列を引数に取り、該当するノードを返す
    def get_node(self, path: str) -> CryptreeNode:
        path = path.strip('/').split('/')
        if not path[0]:
            return self.root
        node = self.root
        for part in path:
            if part in node.children:
                node = node.children[part]
            else: 
                return None
        return node
    
    #データの追加、削除、移動などの基本的操作
    #新しいノードを作成し、指定された親ノードに追加する
    def create_node(self, path: str, node_type: str, name: str):
        parent = self.get_node(path) #親ノードを見つける
        if parent is not None:
            new_node = CryptreeNode(node_type, name)
            parent.add_child(new_node)
            return new_node
        else:
            raise Exception(f'NO such directory: {path}')
        
    #親ノードから削除する
    def delete_node(self, path: str):
        node = self.get_node(path)
        if node is not None:
            parent = node.parent
            if parent is not None:
                del parent.children[node.name]
            else:
                raise Exception("Cannot delete root node")
        else:
            raise Exception(f"No such file or directory: {path}")
        
    #ノードを移動させる
    def move_node(self, old_path: str, new_path: str):
        node = self.get_node(old_path) #指定されたノードを見つける
        if node is not None:
            new_parent = self.get_node(new_path) #親ノードに追加する
            if new_parent is not None: #古いノードの削除処理
                old_parent = node.parent
                del old_parent.children[node.name]
                new_parent.add_child(node)
            else:
                raise Exception(f"No such directory: {new_path}")
        else:
            raise Exception(f"No such file or directory: {old_path}")

#CryptreeNodeを作成してCryptreeを初期化
root = CryptreeNode('directory', 'root')
tree = Cryptree(root)

# 新しいディレクトリを作成
tree.create_node('/', 'directory', 'dir1')

# 新しいファイルを作成してデータを書き込む
file_node = tree.create_node('/dir1', 'file', 'file1')
file_node.write_data("Hello, Cryptree!")

# データを読み取る
print(file_node.read_data())

# ファイルを移動する
tree.move_node('/dir1/file1', '/')

# 以下、上記で定義した各クラスの後に追加する

if __name__ == "__main__":
    # ルートディレクトリノードを作成
    root = CryptreeNode('directory', 'root')

    # Cryptreeを作成
    tree = Cryptree(root)

    # 新しいディレクトリをルートに作成
    tree.create_node('/', 'directory', 'dir1')

    # 新しいファイルを作成し、データを書き込む
    file1 = tree.create_node('/dir1', 'file', 'file1')
    file1.write_data('Hello, Cryptree!')

    # データを読み取る
    print(file1.read_data())  # 出力: 'Hello, Cryptree!'
