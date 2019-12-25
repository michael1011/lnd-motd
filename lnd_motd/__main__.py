from argparse import ArgumentParser
from .printer import print_info
from .cli import setup_argument_parser
from .resources import get_resources_info
from .lnd_client import LndClient, get_lnd_info
from .bitcoin_client import BitcoinClient, get_bitcoin_info

# TODO: error handling
def main():
    ARGS = setup_argument_parser()

    BITCOIN_CLIENT = BitcoinClient(ARGS.bitcoin_host, ARGS.bitcoin_port, ARGS.bitcoin_cookie)
    BITCOIN_INFO = get_bitcoin_info(BITCOIN_CLIENT)

    LND_CLIENT = LndClient(ARGS.lnd_host, ARGS.lnd_port, ARGS.lnd_cert, ARGS.lnd_macaroon)
    LND_INFO = get_lnd_info(LND_CLIENT)

    RESOURCES_INFO = get_resources_info(ARGS.disk_mount)

    print_info(RESOURCES_INFO, BITCOIN_INFO, LND_INFO)

if __name__ == "__main__":
    main()
