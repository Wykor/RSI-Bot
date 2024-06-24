import os
from dotenv import load_dotenv

from pybit.unified_trading import HTTP

from db_helpers import create_rsi, get_latest_rsi


load_dotenv()
api_key = os.getenv('BYBIT_API_KEY')
api_secret = os.getenv('BYBIT_API_SECRET')

class RSICalculator:

    def __init__(self, db_session):
        self.db_session = db_session
        self.api_session = HTTP(
            api_key=api_key,
            api_secret=api_secret,
        )


    def calculate_avg_gain_lose(self, close_prices):
        gains = []
        losses = []
        for i in range(1, len(close_prices)):
            diff = close_prices[i] - close_prices[i - 1]
            if diff > 0:
                gains.append(diff)
                losses.append(0)
            else:
                gains.append(0)
                losses.append(abs(diff))

        average_gain = sum(gains) / len(gains)
        average_loss = sum(losses) / len(losses)
        return average_gain, average_loss

    def calculate_rsi(self, average_gain, average_loss):
        if average_loss == 0:
            return 100
        rs = average_gain / average_loss
        rsi = 100 - (100 / (1 + rs))
        return rsi

    def calculate_rsi_from_kline(self, kline):
        close_prices = [float(bar['close']) for bar in reversed(kline['result']['list'])]
        
        average_gain, average_loss = self.calculate_avg_gain_lose(close_prices)

        rsi = self.calculate_rsi(average_gain, average_loss)
        return rsi


    def get_rsi(self, symbol, timeframe=60, periods=14):
        rsi = get_latest_rsi(self.db_session, symbol)
        kline = self.api_session.get_kline(symbol=symbol, interval=timeframe, limit=periods)
        latest_bar_close_at = kline['result']['list'][-1][0]
        if rsi is None or rsi.latest_bar_close_at != latest_bar_close_at:
            new_rsi = self.calculate_rsi_from_kline(kline)
            rsi = create_rsi(self.db_session, symbol, new_rsi, latest_bar_close_at)
            return rsi.rsi