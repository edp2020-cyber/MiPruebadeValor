import os
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce
import telebot

# --- CONFIGURACIÓN ---
ALPACA_KEY = "TU_PAPER_KEY"
ALPACA_SECRET = "TU_PAPER_SECRET"
TELEGRAM_TOKEN = "TU_BOT_TOKEN"
MI_CHAT_ID = "TU_CHAT_ID"

# Inicializar Clientes
trading_client = TradingClient(ALPACA_KEY, ALPACA_SECRET, paper=True)
bot = telebot.TeleBot(TELEGRAM_TOKEN)

@bot.message_handler(commands=['start', 'balance'])
def enviar_balance(message):
    account = trading_client.get_account()
    msg = f"💰 Balance actual: ${account.cash}\nStatus: {account.status}"
    bot.reply_to(message, msg)

@bot.message_handler(commands=['comprar'])
def comprar_prueba(message):
    # Ejemplo rápido: Compra 1 acción de Apple (AAPL)
    try:
        req = MarketOrderRequest(
            symbol="AAPL",
            qty=1,
            side=OrderSide.BUY,
            time_in_force=TimeInForce.GTC
        )
        trading_client.submit_order(req)
        bot.reply_to(message, "✅ Orden de compra AAPL enviada (Paper Trading)")
    except Exception as e:
        bot.reply_to(message, f"❌ Error: {e}")

print("Bot corriendo...")
bot.infinity_polling()
