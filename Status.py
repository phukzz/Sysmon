import Database as db
import pandas as pd

def check_alerts():
    info = db.get_recent()
    df = pd.DataFrame(info)
    if len(df) == 0:
        return None
    else:
        latest = df["TimeStamp"].iloc[0]
        oldest = df["TimeStamp"].iloc[-1]
        x = latest - oldest
        if x < 295:
            return 2
        if x > 413:
            return 3
        if 295 <= x <= 413:
            checks = df["CPU_Percent"]
            if sum(checks >= 80) >= 48:
                return 1
            else:
                return 0