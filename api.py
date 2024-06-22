import os
from dotenv import load_dotenv

from pybit.unified_trading import HTTP

load_dotenv()
api_key = os.getenv('BYBIT_API_KEY')
api_secret = os.getenv('BYBIT_API_SECRET')

session = HTTP(
    api_key=api_key,
    api_secret=api_secret,
)

print(session.get_kline(symbol='SOLUSDT', interval=60))