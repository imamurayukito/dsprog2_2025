import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import os

# ======================
# DBからデータ取得
# ======================
script_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(script_dir, "webland_properties.db")

conn = sqlite3.connect(db_path)
df = pd.read_sql("SELECT * FROM trade_prices", conn)
conn.close()

print(df)

# ======================
# 仮説検証①：可視化
# ======================
plt.scatter(df.index, df["trade_price"])
plt.xlabel("Property ID")
plt.ylabel("Trade Price (yen)")
plt.title("Distribution of Trade Prices")
plt.show()

# ======================
# 仮説検証②：数値分析
# ======================
average_price = df["trade_price"].mean()
print(f"全体の平均取引価格: {average_price:.0f} 円")

# ======================
# 関数化（動的処理）
# ======================
def average_price_by_city(city):
    return df[df["municipality"] == city]["trade_price"].mean()

print("新宿区の平均価格:", average_price_by_city("新宿区"))
print("渋谷区の平均価格:", average_price_by_city("渋谷区"))
