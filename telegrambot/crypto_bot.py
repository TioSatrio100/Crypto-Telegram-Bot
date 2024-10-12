import os
import requests
import telebot
import matplotlib.pyplot as plt
from datetime import datetime

API_KEY = 'Secret Telegram APU Key'
bot = telebot.TeleBot(API_KEY)

# Function to take a cryptocurrency ID and return the price in USD
def get_crypto_price(crypto_id, currency='usd'):
    url = f'https://api.coingecko.com/api/v3/simple/price?ids={crypto_id}&vs_currencies={currency}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if crypto_id in data:
            return data[crypto_id][currency]
    return None

# Function to take a cryptocurrency ID and return the details
def get_crypto_details(crypto_id):
    url = f'https://api.coingecko.com/api/v3/coins/{crypto_id}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None
    
# Function to take a cryptocurrency ID and return the market chart for 7 days
def get_market_chart(crypto_id, vs_currency='usd', days='7'):
    url = f'https://api.coingecko.com/api/v3/coins/{crypto_id}/market_chart'
    params = {
        'vs_currency': vs_currency,
        'days': days
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return None
    
# Function to take a cryptocurrency ID and return the market chart for 30 days
def get_market_chart2(crypto_id, vs_currency='usd', days='30'):
    url = f'https://api.coingecko.com/api/v3/coins/{crypto_id}/market_chart'
    params = {
        'vs_currency': vs_currency,
        'days': days
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Function to take dates and prices and create a chart
def create_graph(dates, prices, filename='crypto_chart.png'):
    plt.figure(figsize=(10, 5))
    plt.plot(dates, prices, linestyle='-', color='b')
    plt.title('Chart of Price (USD)')
    plt.xlabel('Date')
    plt.ylabel('Price (USD)')
    plt.grid(True)
    plt.savefig(filename)
    plt.close()  

# Function to take dates and prices and create a chart
def create_graph2(dates, prices, filename='crypto_chart.png'):
    plt.figure(figsize=(15, 5))
    plt.plot(dates, prices,  linestyle='-', color='b')
    plt.title('Chart of Price (USD)')
    plt.xlabel('Date')
    plt.ylabel('Price (USD)')
    plt.grid(True)
    plt.savefig(filename)
    plt.close()  

# Handler for start command
@bot.message_handler(commands=["start"])
def start(message):
    bot.reply_to(message, "Hello, I am a crypto bot.\n Use /price <crypto_id> to get the current price.\n Use /details <crypto_id> to get the details.\n Use /chart7days <crypto_id> to get the chart for 7 days.\n Use /chart30days <crypto_id> to get the chart for 30 days.")

# Handler for price command
@bot.message_handler(commands=["price"])
def send_price(message):
    try:
    
        crypto_id = message.text.split()[1].lower()
        
        price = get_crypto_price(crypto_id)
        if price:
            bot.reply_to(message, f"The current price of {crypto_id.capitalize()} is ${price}")
        else:
            bot.reply_to(message, "Sorry, I couldn't find the price for that cryptocurrency.")
    except IndexError:
        bot.reply_to(message, "Please provide a cryptocurrency ID, e.g., /price bitcoin")
    except Exception as e:
        bot.reply_to(message, f"An error occurred: {e}")

# Handler for details command
@bot.message_handler(commands=["details"])
def send_crypto_details(message):
    try:
        
        crypto_id = message.text.split()[1].lower()
        
        
        details = get_crypto_details(crypto_id)
        
        if details:
            
            name = details['name']
            symbol = details['symbol']
            rank = details['market_cap_rank']
            price = details['market_data']['current_price']['usd']
            market_cap = details['market_data']['market_cap']['usd']
            volume = details['market_data']['total_volume']['usd']
            description = details['description']['en'][:1000] if details['description']['en'] else 'No description available.'

            
            message_text = (
                f"📈 *{name}* ({symbol.upper()})\n"
                f"🏅 Market Rank: {rank}\n"
                f"💰 Current Price (USD): ${price}\n"
                f"📊 Market Cap: ${market_cap}\n"
                f"🔄 24h Trading Volume: ${volume}\n\n"
                f"📋 *Description*: {description}\n"
            )
            
            bot.reply_to(message, message_text, parse_mode='Markdown')
        else:
            
            bot.reply_to(message, "Sorry, I couldn't find the details for that cryptocurrency.")
    except IndexError:
       
        bot.reply_to(message, "Please provide a cryptocurrency ID, e.g., /details bitcoin")
    except Exception as e:
       
        bot.reply_to(message, f"An error occurred: {e}")

# Handler for chart command 7 days
@bot.message_handler(commands=['chart7days'])
def send_graph(message):
    try:
        crypto_id = message.text.split()[1].lower()
        data = get_market_chart(crypto_id)

    
        if data:
        
            timestamps = [entry[0] for entry in data['prices']]
            prices = [entry[1] for entry in data['prices']]
            dates = [datetime.fromtimestamp(ts / 1000.0) for ts in timestamps]

        
            filename = 'crypto_chart.png'
            create_graph(dates, prices, filename)
        
        
            with open(filename, 'rb') as photo:
                bot.send_photo(message.chat.id, photo, caption="Price Chart of"  + crypto_id.capitalize() + " for the last 7 days")
        
        
            os.remove(filename)
        else:
            bot.reply_to(message, "Sorry, unable to retrieve data from CoinGecko API and error detected.")
    except IndexError:
        bot.reply_to(message, "Please provide a cryptocurrency ID, e.g., /chart bitcoin")
    except Exception as e:
        bot.reply_to(message, f"An error occurred: {e}")

# Handler for chart command 30 days
@bot.message_handler(commands=['chart30days'])
def send_graph(message):
    try:
        crypto_id = message.text.split()[1].lower()
        data = get_market_chart2(crypto_id)

    
        if data:
        
            timestamps = [entry[0] for entry in data['prices']]
            prices = [entry[1] for entry in data['prices']]
            dates = [datetime.fromtimestamp(ts / 1000.0) for ts in timestamps]

        
            filename = 'crypto_chart.png'
            create_graph2(dates, prices, filename)
        
        
            with open(filename, 'rb') as photo:
                bot.send_photo(message.chat.id, photo, caption="Price Chart of" + crypto_id.capitalize() + " for the last 30 days")
        
        
            os.remove(filename)
        else:
            bot.reply_to(message, "Sorry, unable to retrieve data from CoinGecko API and error detected.")
    except IndexError:
        bot.reply_to(message, "Please provide a cryptocurrency ID, e.g., /chart bitcoin")
    except Exception as e:
        bot.reply_to(message, f"An error occurred: {e}")

bot.polling()
