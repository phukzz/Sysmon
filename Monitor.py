import psutil
import time

_init = psutil.net_io_counters()
prev_recv = _init.bytes_recv
prev_sent = _init.bytes_sent

while True:
    a = psutil.cpu_percent(interval=None, percpu=False)
    b = psutil.virtual_memory()
    c = psutil.disk_usage("/")
    d = psutil.net_io_counters(nowrap=False)
    Time = time.strftime(" %d/%m/%Y %H:%M:%S")

    e = (d.bytes_recv - prev_recv)/1024/5
    f = (d.bytes_sent - prev_sent)/1024/5
    prev_recv = d.bytes_recv
    prev_sent = d.bytes_sent

    print(f"TIME: {(Time)} | CPU: {a}% | MEM: {round((b.used/(1024**3)),2)}/{round((b.total/(1024**3)),2)} GB, {b.percent}% | DISK: {c.percent}%, {round(c.used/(1024**3))}/{round(c.total/(1024**3))} GB | NETWORK: {e} KB/s, {f} KB/s")
    time.sleep(5)