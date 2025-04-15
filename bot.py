from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os
import requests
from dotenv import load_dotenv

load_dotenv()

# 地址绑定存储（内存）
USER_DATA = {}

# /energy
async def energy_status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    threshold = os.getenv("ENERGY_THRESHOLD", "20000")
    cost = os.getenv("RENT_COST_TRX", "3")
    duration = os.getenv("RENT_DURATION_HOURS", "1")
    wallet = os.getenv("TRX_WALLET_ADDRESS", "未设置地址")
    await update.message.reply_text(
        f"钱包地址：{wallet}\n当前能量状态模拟：低于 {threshold}\n"
        f"将自动租赁 {cost} TRX，时长 {duration} 小时"
    )

# /weather
async def weather(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("请输入城市名，例如：/weather 北京")
        return
    city = " ".join(context.args)
    api_key = os.getenv("OPENWEATHER_API_KEY")
    geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={api_key}"
    geo_data = requests.get(geo_url).json()
    if not geo_data:
        await update.message.reply_text(f"无法定位城市：{city}")
        return
    lat = geo_data[0]["lat"]
    lon = geo_data[0]["lon"]
    cname = geo_data[0]["name"]
    weather_url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric&lang=zh_cn"
    w_data = requests.get(weather_url).json()
    desc = w_data["weather"][0]["description"]
    temp = w_data["main"]["temp"]
    await update.message.reply_text(f"{cname} 当前天气：{desc}，温度：{temp}°C")

# /price
async def price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    coin = "tron"
    if context.args:
        arg = context.args[0].lower()
        if arg in ["btc", "bitcoin"]:
            coin = "bitcoin"
        elif arg in ["eth", "ethereum"]:
            coin = "ethereum"
        elif arg in ["trx", "tron"]:
            coin = "tron"
        else:
            await update.message.reply_text("支持查询的币种：trx, btc, eth")
            return
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin}&vs_currencies=usd"
    try:
        data = requests.get(url).json()
        price = data[coin]["usd"]
        await update.message.reply_text(f"{coin.upper()} 当前价格：${price}")
    except:
        await update.message.reply_text("价格获取失败")

# /bind
async def bind(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not context.args:
        await update.message.reply_text("用法：/bind Txxxxxxx（你的TRX地址）")
        return
    address = context.args[0]
    USER_DATA[user_id] = address
    await update.message.reply_text(f"绑定成功！你的地址是：{address}")

# /myaddress
async def myaddress(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    address = USER_DATA.get(user_id)
    if address:
        await update.message.reply_text(f"你绑定的地址是：{address}")
    else:
        await update.message.reply_text("你还没有绑定地址，使用 /bind Txxx 来绑定")

# main
def main():
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        print("未设置 TELEGRAM_BOT_TOKEN")
        return
    app = ApplicationBuilder().token(token).build()
    app.add_handler(CommandHandler("energy", energy_status))
    app.add_handler(CommandHandler("weather", weather))
    app.add_handler(CommandHandler("price", price))
    app.add_handler(CommandHandler("bind", bind))
    app.add_handler(CommandHandler("myaddress", myaddress))
    print("Bot 正在运行...")
    app.run_polling()

if __name__ == "__main__":
    main()
