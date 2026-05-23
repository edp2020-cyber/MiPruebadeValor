import http.server
import socketserver
import threading
import os
import telebot
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce

# 1. SERVIDOR FALSO PARA RENDER (Evita el error de puerto y el cierre del bot)
def start_dummy_server():
    handler = http.server.SimpleHTTPRequestHandler
    try:
        # Render exige que el servicio escuche en el puerto 10000
        with socketserver.TCPServer(("", 10000), handler) as httpd:
            httpd.serve_forever()
    except Exception:
        pass 

threading.Thread(target=start_dummy_server, daemon=True).start()

# 2. CONFIGURACIÓN (Lee las variables del panel de Render)
# NO pongas tus llaves aquí. Ponlas en la pestaña 'Environment' de Render.
ALPACA_KEY = os.getenv("ALPACA_API_KEY")
ALPACA_SECRET = os.getenv("ALPACA_SECRET_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

# 3. INICIALIZAR CLIENTES
# paper=True indica que usaremos la cuenta de prueba
trading_client = TradingClient(ALPACA_KEY, ALPACA_SECRET, paper=True)
bot = telebot.TeleBot(TELEGRAM_TOKEN)

@bot.message_handler(commands=['start', 'balance'])
def enviar_balance(message):
    try:
        account = trading_client.get_account()
        msg = f"💰 Balance actual: ${account.cash}\nStatus: {account.status}"
        bot.reply_to(message, msg)
    except Exception as e:
        bot.reply_to(message, f"❌ Error al consultar balance: {e}")

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
        bot.reply_to(message, f"❌ Error en la compra: {e}")

print("🚀 Bot encendido y esperando comandos en Telegram...")
bot.infinity_polling()
