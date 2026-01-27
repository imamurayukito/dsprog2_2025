import pandas as pd
import sqlite3
import os

# スクリプトのディレクトリパスを取得
script_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(script_dir, "trade_prices.csv")
db_path = os.path.join(script_dir, "webland_properties.db")

# CSV読み込み
df = pd.read_csv(csv_path)

# DB作成・保存
conn = sqlite3.connect(db_path)
df.to_sql("trade_prices", conn, if_exists="replace", index=False)
conn.close()

print("CSVデータをDBに保存しました")
