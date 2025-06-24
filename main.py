from flask import Flask, request
import requests

app = Flask(__name__)

DISCORD_WEBHOOK_URL = (
    "https://discord.com/api/webhooks/"
    "1380885679860613200/"
    "w5YxLn2_0pvjluhaiATLlkWGHemjKLjQCo96B6-gxIaHzISdx-xp7qyNLeQANjAHvhEJ"
)

SECRET_KEY = "7F2A9K3L5Q8X1Z0M"  # Substitua pela sua secret key de 16 chars

MESSAGES = {
    "SALE":   "💸 **VENDA CONFIRMADA!**",
    "UPSELL": "⬆️ **UPSELL / ORDER BUMP!**",
    "RFND":   "❌ **REEMBOLSO PROCESSADO!**",
    "BILL":   "🔁 **REBILL RECEBIDO!**",
    "CGBK":   "⚠️ **CHARGEBACK DETECTADO!**",
    "INSF":   "🚫 **FALHA DE PAGAMENTO (SALDO INSUFICIENTE)!**",
}

@app.route("/", methods=["GET"])
def home():
    return "✅ Bot do Xandão no ar! Pronto para receber notificações do ClickBank.", 200

@app.route("/webhook_clickbank", methods=["POST"])
def webhook_clickbank():
    # DEBUG: log completo do form
    print("🔍 Payload recebido:", dict(request.form))

    # Validação da secret key
    secret = request.form.get("secretKey", "")
    if secret != SECRET_KEY:
        print("❌ SecretKey inválida:", secret)
        return "", 403

    # Mapeamento de campos
    item     = request.form.get("item", "— Produto desconhecido —")
    amount   = request.form.get("amount", "0.00")
    tx_type  = request.form.get("transactionType", "UNKNOWN").upper()

    header = MESSAGES.get(tx_type, f"📦 **NOVA TRANSAÇÃO ({tx_type})**")
    mensagem = (
        f"{header}\n"
        f"🛍️ Produto: `{item}`\n"
        f"💵 Valor: `${amount}`\n"
        f"🔄 Tipo: `{tx_type}`"
    )

    resp = requests.post(DISCORD_WEBHOOK_URL, json={"content": mensagem})
    if resp.status_code == 204:
        print(f"✅ {tx_type} notificado com sucesso.")
    else:
        print(f"❌ Erro {resp.status_code}: {resp.text}")

    return "", 204

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
