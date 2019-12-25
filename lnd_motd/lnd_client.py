from os import path
from dataclasses import dataclass
import base64, codecs, json, requests

@dataclass
class LndInfo:
    alias: str
    color: str
    version: str

    active_channels: int
    inactive_channels: int
    pending_channels: int

    wallet_balance: int
    channel_balance: int

class LndClient:
    url: str = None

    headers = None
    cert_path = None

    def __init__(self, host: str, port: int, cert_path: str, macaroon_path: str):
        self.url = "https://{host}:{port}/v1".format(
            host=host,
            port=port,
        )

        self.cert_path = path.expanduser(cert_path)

        macaroon = codecs.encode(
            open(path.expanduser(macaroon_path), "rb").read(),
            "hex"
        )
        self.headers = {"Grpc-Metadata-macaroon": macaroon}

    def get_info(self):
        return self.__send_request("getinfo")

    def get_wallet_balance(self):
        return self.__send_request("balance/blockchain")

    def get_channel_balance(self):
        return self.__send_request("balance/channels")

    def __send_request(self, endpoint: str):
        response = requests.get(
            "{url}/{endpoint}".format(url=self.url, endpoint=endpoint),
            headers=self.headers,
            verify=self.cert_path,
        )

        return response.json()


def get_lnd_info(client: LndClient) -> LndInfo:
    info = client.get_info()
    wallet_balance = client.get_wallet_balance()
    channel_balance = client.get_channel_balance()

    version = info["version"].split(" ")[0]

    return LndInfo(
        version=version,

        alias=info["alias"],
        color=info["color"],

        active_channels=info.get("num_active_channels", 0),
        pending_channels=info.get("num_pending_channels", 0),
        inactive_channels=info.get("num_inactive_channels", 0),

        channel_balance=channel_balance.get("balance", 0),
        wallet_balance=wallet_balance.get("total_balance", 0),
    )
