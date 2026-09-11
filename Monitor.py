import psutil
import time
import Database as db

_init = psutil.net_io_counters()
prev_recv = _init.bytes_recv
prev_sent = _init.bytes_sent 
# Both prev_recv and prev_sent are initialized with the current network I/O counters to track the amount of data received and sent over time. The first iteration of the collect function will calculate the difference in bytes received and sent since this initialization, allowing for accurate measurement of network activity over the specified interval.

# Colect() is a function that collects various system metrics such as CPU usage, memory usage, disk usage, and network I/O statistics. It returns a dictionary containing these metrics along with a timestamp. Making a collect() function allows for easy retrieval of system performance data at regular intervals, which can be useful for monitoring and analysis purposes.
def collect():
    try:    
        global prev_recv, prev_sent # Colect() function uses the global variables prev_recv and prev_sent to keep track of the previous network I/O counters. This allows the function to calculate the amount of data received and sent since the last call to collect().
        a = psutil.cpu_percent(interval=None, percpu=False) #cpu_percent() with interval=None returns the current system-wide CPU utilization as a percentage without blocking. The percpu=False argument indicates that the function should return a single value representing the overall CPU usage rather than individual values for each CPU core.
        b = psutil.virtual_memory()
        c = psutil.disk_usage("/") # disk_usage("/") returns the disk usage statistics for the root directory ("/"). Using ("/") as the argument ensures that the function retrieves information about the primary storage device, which is typically where the operating system and most applications are installed.
        d = psutil.net_io_counters(nowrap=False) # net_io_counters() with nowrap=False means that the values will not reset to zero when they reach their maximum value, important for accurately tracking network activity over time.
        Time = int(time.time()) # getting timestamps as integer for SQLite then convert it into readable format.

        e = (d.bytes_recv - prev_recv)/1024/5
        f = (d.bytes_sent - prev_sent)/1024/5
        prev_recv = d.bytes_recv
        prev_sent = d.bytes_sent
        Data = {
            "TimeStamp": Time,
            "CPU_Percent": a,
            "MEM_Percent": b.percent,
            "MEM_Used": round((b.used/(1024**3)),2),
            "MEM_Total": round((b.total/(1024**3)),2),
            "DISK_Percent": c.percent,
            "DISK_Used": round(c.used/(1024**3),2),
            "DISK_Total": round(c.total/(1024**3),2),
            "NETWORK_Recv": round(e,2),
            "NETWORK_Sent": round(f,2)
        }
        return Data
    except Exception as e:
        print(f"Error collecting metrics: {e}")
        return None 

while True:
    data = collect()
    if data is None:
        print("Failed to collect metrics. Retrying in 5 seconds...")
        time.sleep(5)
    else:
        print(data)
        db.insert_metrics(data)
        time.sleep(5) # The while loop continuously calls the collect() function every 5 seconds.