from argparse import ArgumentParser

def setup_argument_parser():
    PARSER = ArgumentParser(description="Print basic information about a Bitcoin and LND node")

    PARSER.add_argument(
        "--disk-mount",
        help="Path to the mount point of the external disk",
        type=str,
    )

    # Bitcoin Core related arguments
    PARSER.add_argument(
        "--bitcoin-host",
        help="RPC host of the Bitcoin Core node",
        type=str,
        default="127.0.0.1",
    )
    PARSER.add_argument(
        "--bitcoin-port",
        help="RPC Port of the Bitcoin Core node",
        type=int,
        default=8332,
    )
    PARSER.add_argument(
        "--bitcoin-cookie",
        help="Path to the cookie file of the Bitcoin Core node",
        type=str,
    )

    # LND related arguments
    PARSER.add_argument(
        "--lnd-host",
        help="REST API host of the LND node",
        type=str,
        default="127.0.0.1",
    )
    PARSER.add_argument(
        "--lnd-port",
        help="REST API port of the LND node",
        type=int,
        default=8080,
    )
    PARSER.add_argument(
        "--lnd-cert",
        help="Path to the SSL certificate of the REST API of LND",
        type=str,
        default="~/.lnd/tls.cert",
    )
    PARSER.add_argument(
        "--lnd-macaroon",
        help="Path to the readonly macaroon of the LND node",
        type=str,
        default="~/.lnd/data/chain/bitcoin/mainnet/readonly.macaroon",
    )

    return PARSER.parse_args()
