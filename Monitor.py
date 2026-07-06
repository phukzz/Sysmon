import psutil
import time
from prettytable import PrettyTable

table = PrettyTable()
table.field_names = ['ID','System Information','Percentage','Capacity','Recv','Sent']

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
        "MEM_Total": round((b.used/(1024**3)),2)/round((b.total/(1024**3)),2),
        "DISK_Percent": c.percent,
        "DISK_Total": round(c.used/(1024**3))/round(c.total/(1024**3)),
        "NETWORK_Recv": round(e,2),
        "NETWORK_Sent": round(f,2)
    }
    return Data

while True:
    print(collect())
    # table.clear_rows()
    # table.add_row(['1','CPU',f"{a}%","N/A","N/A","N/A"])
    # table.add_row(['2','MEMORY',f"{b.percent}%" ,f"{round((b.used/(1024**3)),2)}/{round((b.total/(1024**3)),2)} GB","N/A","N/A"])
    # table.add_row(['3','DISK',f"{c.percent}%",f"{round(c.used/(1024**3))}/{round(c.total/(1024**3))} GB","N/A","N/A"])
    # table.add_row(['4','NETWORK',"N/A","N/A",f"{e} KB/s",f"{f} KB/s"])
    # print(f"TIME: {(Time)}")
    # print(table)
    time.sleep(5)