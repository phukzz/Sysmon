import psutil
import time

_init = psutil.net_io_counters()
prev_recv = _init.bytes_recv
prev_sent = _init.bytes_sent

def collect():
    global prev_recv, prev_sent
    a = psutil.cpu_percent(interval=None, percpu=False)
    b = psutil.virtual_memory()
    c = psutil.disk_usage("/")
    d = psutil.net_io_counters(nowrap=False)
    Time = time.strftime(" %d/%m/%Y %H:%M:%S")
    e = (d.bytes_recv - prev_recv)/1024/5
    f = (d.bytes_sent - prev_sent)/1024/5
    prev_recv = d.bytes_recv
    prev_sent = d.bytes_sent
    Data = {
        "TimeStamp": Time,
        "CPU_Percent": a,
        "MEM_Percent": b.percent,
        "MEM_USED": round((b.used/(1024**3)),2),
        "MEM_Total": round((b.total/(1024**3)),2),
        "DISK_Percent": c.percent,
        "DISK_USED": round(c.used/(1024**3),2),
        "DISK_Total": round(c.total/(1024**3),2),
        "NETWORK_Recv": round(e,2),
        "NETWORK_Sent": round(f,2)
    }
    return Data

while True:
    print(collect())
    time.sleep(5)