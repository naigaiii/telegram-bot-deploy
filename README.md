# Telegram Bot：TRX能量 + 天气 + 币价 + 用户绑定

一个功能齐全的 Telegram Bot，支持以下指令：

## 指令说明

- `/energy`：查看能量模拟状态
- `/weather 城市`：实时天气（中文城市）
- `/price` 或 `/price btc/eth/trx`：获取币价
- `/bind TRX地址`：绑定钱包地址
- `/myaddress`：查看你绑定的钱包地址

---

## 本地启动方式：

```bash
pip install -r requirements.txt
cp .env.example .env  # 修改为你的密钥
python bot.py
```

---

## Railway 部署方法

1. 登录 https://railway.app
2. 点击 “New Project” → 选择 “Deploy from GitHub”
3. 上传该项目或通过 GitHub 链接
4. 添加环境变量（Variables）：

| 名称 | 示例值 |
|------|---------|
| TELEGRAM_BOT_TOKEN | 你的 Bot Token |
| OPENWEATHER_API_KEY | 你的天气 API |
| TRX_WALLET_ADDRESS | TRX钱包地址 |
| ENERGY_THRESHOLD | 20000 |
| RENT_COST_TRX | 3 |
| RENT_DURATION_HOURS | 1 |

5. Railway 会自动构建并启动你的机器人！

---

由 ChatGPT 自动生成部署包。
