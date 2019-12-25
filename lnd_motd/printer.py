import re
import subprocess
from typing import List
from .lnd_client import LndInfo
from .resources import ResourcesInfo
from .bitcoin_client import BitcoinInfo

WARNING_THRESHOLD = 0.9

MEGABYTE = 2**20
GIGABYTE = 2**30
TERABYTE = 2**40

RESET = "\033[0m"
RED = "\u001b[31m"
GREEN = "\u001b[32m"
YELLOW = "\u001b[33m"

ANSI_ESCAPE = re.compile(r'(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]')

class Column:
    def __init__(self, entries: List[str]):
        self.entries = entries
        self.longesEntry = max(len(ANSI_ESCAPE.sub('', x)) for x in entries)    


def hex_to_rgb(hex):
    hex = hex.lstrip('#')
    hlen = len(hex)
    
    return tuple(int(hex[i:i + hlen // 3], 16) for i in range(0, hlen, hlen // 3))

def get_color_escape(hex, background=False):
    r, g, b = hex_to_rgb(hex)
    
    return "\033[{};2;{};{};{}m".format(48 if background else 38, r, g, b)


def prepare_columns(resource_info: ResourcesInfo, bitcoin_info: BitcoinInfo, lnd_info: LndInfo):
    columns = []

    # Resources column
    resources_entries = []

    resources_entries.append("{yellow}Resources".format(yellow=YELLOW))  
    resources_entries.append("Memory    {color}{free}M / {total}M{reset}".format(
        color=GREEN if resource_info.memory_free / resource_info.memory_total < WARNING_THRESHOLD else RED,
        free=resource_info.memory_free // MEGABYTE,
        total=resource_info.memory_total // MEGABYTE,
        reset=RESET,
    ))
    resources_entries.append("SD        {color}{free}G ({percentage:.0%}){reset}".format(
        color=GREEN if resource_info.sd_free / resource_info.sd_total < WARNING_THRESHOLD else RED,
        free=resource_info.sd_free // GIGABYTE,
        percentage=resource_info.sd_free / resource_info.sd_total,
        reset=RESET
    ))

    if resource_info.disk_total != 0:
        resources_entries.append("SSD       {color}{free}G ({percentage:.0%}){reset}".format(
            color=GREEN if resource_info.disk_free / resource_info.disk_total < WARNING_THRESHOLD else RED,
            free=resource_info.disk_free // GIGABYTE,
            percentage=resource_info.disk_free / resource_info.disk_total,
            reset=RESET
        ))

    resources_entries.append("Bandwidth ▲ {:.2f}T".format(resource_info.bandwidth_upload / GIGABYTE))
    resources_entries.append("          ▼ {:.2f}T".format(resource_info.bandwidth_download / GIGABYTE))
    
    # Bitcoin column
    bitcoin_entries = []

    bitcoin_entries.append("₿itcoin ({network})".format(network=bitcoin_info.chain))

    bitcoin_sync = ""

    if bitcoin_info.blocks < bitcoin_info.headers:
        bitcoin_sync = "{}{} ({:.0%}){}".format(
            RED,
            bitcoin_info.blocks,
            bitcoin_info.verification_progress,
            RESET,
        )
    else:
        bitcoin_sync = "{}{}{}".format(
            GREEN,
            bitcoin_info.blocks,
            RESET,
        )

    bitcoin_entries.append("Sync    {}".format(bitcoin_sync))
    bitcoin_entries.append("Peers   {}".format(bitcoin_info.connections))
    bitcoin_entries.append("Mempool {} txs".format(bitcoin_info.mempool_transactions))

    # Lightning column
    lightning_entries = []

    lightning_entries.append("Lightning{reset}".format(reset=RESET))
    lightning_entries.append("{}{}{}".format(
        get_color_escape(lnd_info.color),
        lnd_info.alias,
        RESET,
    ))

    pending_channels = ""

    if lnd_info.pending_channels > 0:
        pending_channels = " ({} pending)".format(lnd_info.pending_channels)

    lightning_entries.append("Channels {}/{}{}".format(
        lnd_info.active_channels,
        lnd_info.active_channels + lnd_info.inactive_channels,
        pending_channels,
    ))
    lightning_entries.append("Balance  {} sats".format(lnd_info.channel_balance))
    lightning_entries.append("Wallet   {} sats".format(lnd_info.wallet_balance))

    columns.append(Column(resources_entries))
    columns.append(Column(bitcoin_entries))
    columns.append(Column(lightning_entries))

    return columns

def print_info(resource_info: ResourcesInfo, bitcoin_info: BitcoinInfo, lnd_info: LndInfo):
    columns = prepare_columns(resource_info, bitcoin_info, lnd_info)

    divider_len = (len(columns) - 1) * 5
    longest_column = 0

    for column in columns:
        divider_len += column.longesEntry

        for i in range(0, len(column.entries)):            
            if i > longest_column:
                longest_column = i
            
            escaped_entry = ANSI_ESCAPE.sub('', column.entries[i])
            escaped_entry_len = len(escaped_entry)

            if escaped_entry_len < column.longesEntry:
                column.entries[i] += " " * (column.longesEntry - escaped_entry_len)


    print("{yellow}ThunDroid{reset}: Bitcoin Core {bitcoin_version} & LND {lnd_version}".format(
        yellow=YELLOW,
        reset=RESET,
        bitcoin_version=bitcoin_info.version,
        lnd_version=lnd_info.version,
    ))

    print("{yellow}{divider}{reset}".format(
        yellow=YELLOW,
        divider="-" * divider_len,
        reset=RESET,
    ))
    result = subprocess.run(["uptime"], stdout=subprocess.PIPE)
    print(result.stdout.decode("utf-8").replace(" ", "", 1))

    for i in range(0, longest_column + 1):
        row = ""
        
        for column in columns:
            if row != "":
                row += "     "

            try:
                row += column.entries[i]
            except:
                row += " " * column.longesEntry

        print(row)
    
    print()
