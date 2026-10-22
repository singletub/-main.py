import os
import time
import requests
import pandas as pd
import yfinance as yf

# Telegram Bot Credentials
TELEGRAM_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
CHAT_ID = "YOUR_TELEGRAM_CHAT_ID"

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print(f"Error sending message: {e}")

def check_signals():
    # USD/JPY data ghenyasathi
    data = yf.download("USDJPY=X", period="1d", interval="15m")
    if data.empty:
        return
    
    # Technical Indicators (SMA)
    data['SMA_short'] = data['Close'].rolling(window=5).mean()
    data['SMA_long'] = data['Close'].rolling(window=20).mean()
    
    last_short = data['SMA_short'].iloc[-1]
    last_long = data['SMA_long'].iloc[-1]
    prev_short = data['SMA_short'].iloc[-2]
    prev_long = data['SMA_long'].iloc[-2]
    
    # Crossover Logic
    if prev_short <= prev_long and last_short > last_long:
        send_telegram_message("🟢 BUY Signal for USD/JPY!")
    elif prev_short >= prev_long and last_short < last_long:
        send_telegram_message("🔴 SELL Signal for USD/JPY!")

if __name__ == "__main__":
    send_telegram_message("🚀 Bot started running 24/7 on Render!")
    while True:
        try:
            check_signals()
        except Exception as e:
            print(f"Error: {e}")
        time.sleep(900)  # Call every 15 minutes
