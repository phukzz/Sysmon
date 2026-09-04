import sqlite3

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
    conn.commit()
    conn.close()

