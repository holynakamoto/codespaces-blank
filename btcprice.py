import yfinance as yf
from gtts import gTTS
import feedparser
import os
import threading

def get_bitcoin_price_text():
    try:
        btc_data = yf.download('BTC-USD', start='2023-01-01', end='2023-12-31')
        price = btc_data['Close'].iloc[-1]
        return f"Latest Bitcoin Price: ${price:.2f}"
    except Exception as e:
        print(f"Error fetching Bitcoin price: {e}")
        return "Failed to fetch Bitcoin price."

def fetch_news(source, bitcoin_news):
    feed = feedparser.parse(source)
    for entry in feed.entries:
        title = entry.title
        bitcoin_news.append(title)

def get_bitcoin_news():
    bitcoin_news = []
    sources = [
        "https://news.google.com/rss/search?q=Bitcoin",
        "https://www.bing.com/news/search?q=Bitcoin",
        "https://www.wsj.com/news/business/markets",
        "https://www.marketwatch.com/search?q=Bitcoin",
        "https://www.zerohedge.com/search?query=Bitcoin"
    ]

    threads = []
    for source in sources:
        thread = threading.Thread(target=fetch_news, args=(source, bitcoin_news))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    return bitcoin_news[:5]

def convert_text_to_speech(text):
    try:
        tts = gTTS(text=text, lang='en')
        tts.save("output.mp3")
        os.system("afplay output.mp3")
    except Exception as e:
        print(f"Error converting text to speech: {e}")

def main():
    bitcoin_price_text = get_bitcoin_price_text()
    if bitcoin_price_text:
        print(bitcoin_price_text)
        convert_text_to_speech(bitcoin_price_text)
    else:
        print("Failed to fetch Bitcoin price.")

    bitcoin_news = get_bitcoin_news()
    if bitcoin_news:
        print("\nBitcoin News Headlines:")
        for idx, headline in enumerate(bitcoin_news, start=1):
            print(f"{idx}. {headline}")
        news_text = '\n'.join(bitcoin_news)
        convert_text_to_speech(news_text)
    else:
        print("\nFailed to fetch Bitcoin news.")

if __name__ == "__main__":
    main()
