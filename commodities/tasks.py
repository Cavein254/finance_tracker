import logging
from datetime import datetime

import pandas as pd
from celery import shared_task

from .models import Commodity, CommodityPriceHistory
from .utils import fetch_yfinance_data

logger = logging.getLogger(__name__)


@shared_task
def fetch_commodity_history(symbol: str):
    """
    Fetch 5 year history for a commodity and save to database
    """
    data = fetch_yfinance_data(symbol, period="5y", interval="1d")
    if data.get("status") is False:
        logger.warning(f"No data found for symbol: {symbol}")
        return None

    records = data.get("data", [])
    if not records:
        logger.warning(f"No records to process for symbol: {symbol}")
        return None

    # Get last saved entry from DB
    try:
        logger.info(f"Processing data for symbol: {symbol}")
        # get commodity if available, else create it
        commodity, _ = Commodity.objects.get_or_create(
            symbol=symbol.upper(),
            defaults={
                "name": symbol,
                "description": f"Auto-created commodity for {symbol}",
                "unit": "unit",
                "commodity_type": "ALTERNATIVE",
                "price": 0,
            },
        )
        last_entry = (
            CommodityPriceHistory.objects.filter(commodity__symbol=symbol)
            .order_by("-date")
            .first()
        )

        # Convert list of dicts into DataFrame for filtering
        df = pd.DataFrame(records)

        if last_entry:
            last_date = last_entry.date
            # Filter data to only include new entries
            new_data = df[df["Date"] > pd.to_datetime(last_date)]
        else:
            new_data = df

        inserted_count = 0
        logger.info(f"New data to insert for {symbol}: {len(new_data)} entries")

        for _, row in new_data.iterrows():
            date_val = row["Date"]
            if isinstance(date_val, datetime):
                date_val = date_val.date()

            CommodityPriceHistory.objects.update_or_create(
                commodity_id=commodity.id,
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
