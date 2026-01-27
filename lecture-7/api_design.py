# api_design.py
# 実在する国土交通省 不動産取引価格情報APIの設計コード

import requests

url = "http://www.land.mlit.go.jp/webland/api/TradeListSearch"
params = {
    "from": "20231",   # 2023年第1四半期
    "to": "20232",     # 2023年第2四半期
    "area": "13"       # 東京都
}

response = requests.get(url, params=params)
data = response.json()

print(data)
