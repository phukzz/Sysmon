import sqlite3
import time

def init_db():
    conn = sqlite3.connect('system_metrics.db')
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS metrics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            TimeStamp INTEGER,
            CPU_Percent REAL,
            MEM_Percent REAL,
            MEM_Used REAL,
            MEM_Total REAL,
            DISK_Percent REAL,
            DISK_Used REAL,
            DISK_Total REAL,
            NETWORK_Recv REAL,
            NETWORK_Sent REAL
        )
    ''')
    conn.commit()
    return conn, cur

init_db()

def insert_metrics(Data):
    try: # Wrap insert_metrics() function in a try-except block. If an error occurs during the insertion of metrics into the database, it continue without crashing the program.
        conn, cur = init_db()
        cur.execute('''
            INSERT INTO metrics (
                TimeStamp, 
                CPU_Percent, 
                MEM_Percent, 
                MEM_Used, 
                MEM_Total, 
                DISK_Percent, 
                DISK_Used, 
                DISK_Total, 
                NETWORK_Recv, 
                NETWORK_Sent
            ) VALUES (
                :TimeStamp, 
                :CPU_Percent, 
                :MEM_Percent, 
                :MEM_Used, 
                :MEM_Total, 
                :DISK_Percent, 
                :DISK_Used, 
                :DISK_Total, 
                :NETWORK_Recv, 
                :NETWORK_Sent) 
            ''', Data)
    except Exception as e: # What happens if an error occurs during the execution of the insert_metrics() function, print out the error message and continue without crashing the program.
        print(f"Error inserting metrics: {e}")
    finally: # Finally block ensures that if there is an error or not, the function will always commit the changes to the database and close the connection to prevent resource leaks and ensure that the database remains in a consistent state.
        conn.commit()
        conn.close()

def get_recent():
    conn, cur = init_db()

    cur.execute('SELECT * FROM metrics ORDER BY TimeStamp DESC LIMIT 60')
    res = cur.fetchall()

    desc = cur.description
    columns = [col[0] for col in desc]
    result = [dict(zip(columns, row)) for row in res]
    conn.close()
    return result

def get_stats(minutes=60):
    conn, cur = init_db()

    cutoff = int(time.time()) - (minutes * 60)

    cur.execute(f'''SELECT
                MIN(CPU_Percent) AS min_cpu,
                MAX(CPU_Percent) AS max_cpu,
                AVG(CPU_Percent) AS avg_cpu,
                MIN(MEM_Percent) AS min_mem,
                MAX(MEM_Percent) AS max_mem,  
                AVG(MEM_Percent) AS avg_mem,
                MIN(DISK_Percent) AS min_disk,
                MAX(DISK_Percent) AS max_disk,
                AVG(DISK_Percent) AS avg_disk,
                MIN(NETWORK_Recv) AS min_recv,
                MAX(NETWORK_Recv) AS max_recv,
                AVG(NETWORK_Recv) AS avg_recv,
                MIN(NETWORK_Sent) AS min_sent,
                MAX(NETWORK_Sent) AS max_sent,
                AVG(NETWORK_Sent) AS avg_sent
                FROM metrics WHERE TimeStamp >= ?''', (cutoff,))
    stats = cur.fetchone()

    desc = cur.description
    columns = [col[0] for col in desc]
    result = dict(zip(columns, stats))
    conn.close()    
    return result
