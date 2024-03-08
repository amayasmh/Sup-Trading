import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from DatabaseFunctions import Connect, Execute, CreateAllTables

# Symbole du CAC 40
cac40_symbol = "VIV.PA"

# Déterminer les dates de début et de fin
end_date = datetime.now()
start_date = end_date - timedelta(days=6*30)  # 6 mois

# Récupérer les données du CAC 40
cac40_data = yf.download(cac40_symbol, start=start_date, end=end_date)
cac40_data["price"] = cac40_data["Close"]

# Sauvegarder les données dans un fichier CSV
cac40_data.to_csv("cac40_historical_data.csv")
print(cac40_data.columns)

dates = cac40_data.index

cac40_data["Date"] = dates

print(cac40_data)

def InsertDataCac40(Conn, Cur, Data):
    if Conn is None or Cur is None:
        Conn, Cur = Connect()
    for index, row in Data.iterrows():
        Sql = "INSERT INTO COMPANIES (company, sector, price, variation, open, high, low, downward_limit, upward_limit, last_dividend, last_dividend_date, volume, valuation, capital, estimated_yield_2024, trade_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        Values = ("VIVENDI", "Audiovisuel et divertissements", row["price"], None, row["Open"], row["High"], row["Low"], None, None, None, None, row["Volume"], None, None, None, row["Date"])
        Execute(Conn, Cur, Sql, Values)
    Conn.commit()
    Cur.close()
    Conn.close()

# CreateAllTables(None, None)
# InsertDataCac40(None, None, cac40_data)
