import pandas as pd
import sqlite3
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
import os


class JobAnalyzer:
    def __init__(self, excel_path, db_path):
        self.excel_path = excel_path
        self.db_path = db_path

    def load_excel(self):
        """
        e-Statから取得したExcelを読み込む
        ※ 上2行が説明文の場合が多いため skiprows=2
        """
        df = pd.read_excel(self.excel_path, skiprows=2)
        return df

    def save_to_db(self, df, table_name):
        """
        DataFrameをSQLiteに保存
        """
        engine = create_engine(f"sqlite:///{self.db_path}")
        df.to_sql(table_name, engine, if_exists="replace", index=False)

    def load_from_db(self, table_name):
        """
        DBからデータを取得
        """
        conn = sqlite3.connect(self.db_path)
        query = f"SELECT * FROM {table_name}"
        df = pd.read_sql(query, conn)
        conn.close()
        return df

    def analyze_and_plot(self, df, time_col, value_col):
        """
        平均値を計算し、時系列グラフを描画
        """
        # NaN行を削除
        df_clean = df.dropna(subset=[time_col, value_col])
        
        # 数値型に変換
        df_clean[value_col] = pd.to_numeric(df_clean[value_col], errors='coerce')
        df_clean = df_clean.dropna(subset=[value_col])
        
        mean_value = df_clean[value_col].mean()
        print(f"{value_col} の平均値: {mean_value}")

        plt.figure()
        plt.plot(df_clean[time_col], df_clean[value_col])
        plt.xticks(rotation=45)
        plt.title(f"{value_col} の推移")
        plt.tight_layout()
        plt.show()


def main():
    # スクリプトのディレクトリパスを取得
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # ファイルパス
    excel_path = os.path.join(script_dir, "job_data.xlsx")
    db_path = os.path.join(script_dir, "job_data.db")
    table_name = "job_statistics"

    # 使用する列名（※Excelの列名に合わせて変更）
    time_column = "Unnamed: 0"  # 西暦が格納されている列
    value_column = "実数"  # 有効求人倍率の実数

    analyzer = JobAnalyzer(excel_path, db_path)

    # ① Excel読み込み
    df_excel = analyzer.load_excel()
    print("Excel読み込み完了")
    print(df_excel.head())

    # ② 必要な列のみ抽出
    df_use = df_excel[[time_column, value_column]]

    # ③ DBに保存
    analyzer.save_to_db(df_use, table_name)
    print("DB保存完了")

    # ④ DBから取得
    df_db = analyzer.load_from_db(table_name)
    print("DB読み込み完了")

    # ⑤ 分析・可視化
    analyzer.analyze_and_plot(df_db, time_column, value_column)


if __name__ == "__main__":
    main()
