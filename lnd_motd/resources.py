import json
import psutil
import subprocess
from dataclasses import dataclass

@dataclass
class ResourcesInfo:
    memory_free: int
    memory_total: int

    sd_free: int
    sd_total: int

    disk_free: int
    disk_total: int

    bandwidth_upload: int
    bandwidth_download: int

def get_resources_info(disk_mount: str) -> ResourcesInfo:
    sd_usage = psutil.disk_usage("/")
    memory_info = psutil.virtual_memory()

    disk_free = 0
    disk_total = 0

    if disk_mount != None:
        disk_usage = psutil.disk_usage(disk_mount)

        disk_free = disk_usage.free
        disk_total = disk_usage.total

    vnstat_result = subprocess.run(["vnstat", "--json"], stdout=subprocess.PIPE)
    vnstat_data = json.loads(vnstat_result.stdout.decode("utf-8"))
    total_traffic = vnstat_data['interfaces'][0]['traffic']['total']

    return ResourcesInfo(
        memory_free=memory_info.available,
        memory_total=memory_info.total,

        sd_free=sd_usage.free,
        sd_total=sd_usage.total,

        disk_free=disk_free,
        disk_total=disk_total,

        bandwidth_upload=total_traffic['tx'],
        bandwidth_download=total_traffic['rx'],
    )
