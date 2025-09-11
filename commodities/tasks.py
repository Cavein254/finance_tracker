import logging
from datetime import datetime

import yfinance as yf
from celery import shared_task

from .models import CommodityPriceHistory

logger = logging.getLogger(__name__)


@shared_task
def fetch_commodity_history(symbol: str):
    """
    Fetch 5 year history for a commodity and save to database
    """
    data = yf.download(
        tickers=symbol,
        period="5y",
        interval="1d",
        group_by="ticker",
        auto_adjust=True,
    )
    if data.empty:
        logger.warning(f"No data found for symbol: {symbol}")
        return None

    # Reset index
    data = data.reset_index().dropna()

    # Get last saved entry from DB
    try:
        last_entry = (
            CommodityPriceHistory.objects.filter(commodity__symbol=symbol)
            .order_by("-date")
            .first()
        )

        if last_entry:
            last_date = last_entry.date
            # Filter data to only include new entries
            new_data = data[data["Date"] > last_date]
        else:
            new_data = data

        inserted_count = 0
        for _, row in new_data.iterrows():
            date_val = row["Date"]
            if isinstance(date_val, datetime):
                date_val = date_val.date()

            CommodityPriceHistory.objects.update_or_create(
                commodity_id=symbol,
                date=date_val,
                defaults={
                    "open": row["Open"],
                    "high": row["High"],
                    "low": row["Low"],
                    "close": row["Close"],
                    "volume": row["Volume"],
                },
            )
            inserted_count += 1

        logger.info(f"Inserted/Updated {inserted_count} entries for symbol: {symbol}")
        return inserted_count
    except Exception as e:
        logger.error(f"Error fetching history for symbol {symbol}: {e}")
        return None
