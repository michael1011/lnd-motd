from os import path
from decimal import Decimal
from dataclasses import dataclass
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException

@dataclass
class BitcoinInfo:
    chain: str
    version: str

    blocks: int
    headers: int
    verification_progress: Decimal
    
    connections: int
    mempool_transactions: int

class BitcoinClient:
    rpc_connection: AuthServiceProxy = None

    def __init__(self, host: str, port: int, cookie_path: str):
        cookie = open(path.expanduser(cookie_path)).read().split(":")

        self.rpc_connection = AuthServiceProxy("http://{user}:{password}@{host}:{port}".format(
            port=port,
            host=host,
            user=cookie[0],
            password=cookie[1],
        ))

    def get_blockchain_info(self):
        return self.rpc_connection.getblockchaininfo()

    def get_network_info(self):
        return self.rpc_connection.getnetworkinfo()

    def get_mempool_info(self):
        return self.rpc_connection.getmempoolinfo()

    def get_connection_count(self):
        return self.rpc_connection.getconnectioncount();


def get_bitcoin_info(client: BitcoinClient) -> BitcoinInfo:
    mempool_info = client.get_mempool_info()
    network_info = client.get_network_info()
    blockchain_info = client.get_blockchain_info()
    connection_count = client.get_connection_count()

    version = network_info["subversion"].replace("Satoshi:", "", 1)
    version = version.replace("/", "", 2)

    return BitcoinInfo(
        version=version,

        chain=blockchain_info["chain"],

        blocks=blockchain_info["blocks"],
        headers=blockchain_info["headers"],
        verification_progress=blockchain_info['verificationprogress'],

        connections=connection_count,
        mempool_transactions=mempool_info["size"],
    )
