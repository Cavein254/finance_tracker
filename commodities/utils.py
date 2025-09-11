import pandas as pd
import yfinance as yf


def fetch_yfinance_data(symbol: str, period="1y", interval="1d"):
    try:
        data = yf.download(
            symbol,
            period=period,
            interval=interval,
            auto_adjust=True,
            group_by="ticker",
        )
        if data.empty:
            return {
                "status": False,
                "message": "No data found for the given symbol.",
            }
        else:
            if isinstance(data.columns, pd.MultiIndex):
                # data.columns = [
                #     "_".join([str(c) for c in col if c]) for col in data.columns
                # ]
                data.columns = data.columns.droplevel(0)
                # Reset index so Date becomes a column
                # If MultiIndex (happens when group_by="ticker"), drop the ticker level
                records = data.reset_index().to_dict(orient="records")
                return {"status": True, "data": records}
    except Exception as e:
        return {"status": False, "message": str(e)}
