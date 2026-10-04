import os
import logging
from datetime import datetime
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN não foi definido. Crie um arquivo .env com BOT_TOKEN=SEU_TOKEN")

# Dados por chat/grupo
resultados_por_chat = {}


def get_chat_data(chat_id: int):
    if chat_id not in resultados_por_chat:
        resultados_por_chat[chat_id] = []
    return resultados_por_chat[chat_id]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /start"""
    chat_id = update.effective_chat.id
    get_chat_data(chat_id)
    await update.message.reply_text(
        "🎰 Bem-vindo ao Bot de Baccarat!\n\n"
        "Comandos disponíveis:\n"
        "/add_result [B/P/T] - Adicionar resultado\n"
        "/stats - Ver estatísticas\n"
        "/clear - Limpar histórico do grupo\n"
        "/help - Ajuda\n"
        "/reset - Resetar tudo do grupo"
    )


async def add_result(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Adiciona B, P ou T para o grupo atual"""
    if not context.args:
        await update.message.reply_text("❌ Use: /add_result [B/P/T]")
        return

    resultado = context.args[0].upper()
    if resultado not in {"B", "P", "T"}:
        await update.message.reply_text("❌ Resultado inválido! Use B, P ou T.")
        return

    chat_id = update.effective_chat.id
    dados = get_chat_data(chat_id)
    dados.append({
        "resultado": resultado,
        "usuario": update.effective_user.first_name,
        "timestamp": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
    })

    nomes = {"B": "🏦 Banco", "P": "👤 Jogador", "T": "🤝 Empate"}
    total = len(dados)
    await update.message.reply_text(
        f"✅ {nomes[resultado]} adicionado!\n"
        f"Total de resultados: {total}"
    )


async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Mostra estatísticas do grupo"""
    chat_id = update.effective_chat.id
    resultados = get_chat_data(chat_id)

    if not resultados:
        await update.message.reply_text("📊 Nenhum resultado registrado ainda!")
        return

    total = len(resultados)
    banco = sum(1 for r in resultados if r["resultado"] == "B")
    jogador = sum(1 for r in resultados if r["resultado"] == "P")
    empate = sum(1 for r in resultados if r["resultado"] == "T")

    mensagem = (
        "📊 ESTATÍSTICAS\n"
        "━━━━━━━━━━━━━━━━\n"
        f"🏦 Banco: {banco} ({(banco/total)*100:.1f}%)\n"
        f"👤 Jogador: {jogador} ({(jogador/total)*100:.1f}%)\n"
        f"🤝 Empate: {empate} ({(empate/total)*100:.1f}%)\n"
        "━━━━━━━━━━━━━━━━\n"
        f"📈 Total: {total}"
    )
    await update.message.reply_text(mensagem)


async def clear(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Limpa o histórico do grupo"""
    chat_id = update.effective_chat.id
    dados = get_chat_data(chat_id)
    if not dados:
        await update.message.reply_text("📊 Nenhum resultado para limpar!")
        return

    dados.clear()
    await update.message.reply_text("🗑️ Histórico limpo!")


async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Reseta tudo do grupo"""
    chat_id = update.effective_chat.id
    if chat_id in resultados_por_chat:
        resultados_por_chat.pop(chat_id)
        await update.message.reply_text("🔄 Grupo resetado com sucesso!")
    else:
        await update.message.reply_text("📊 Este grupo ainda não possui histórico.")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /help"""
    await update.message.reply_text(
        "🎰 AJUDA - Bot de Baccarat\n\n"
        "/add_result [B/P/T] - Adicionar resultado\n"
        "Exemplos:\n"
        "• /add_result B\n"
        "• /add_result P\n"
        "• /add_result T\n\n"
        "/stats - Estatísticas do grupo\n"
        "/clear - Limpa o histórico\n"
        "/reset - Reseta tudo do grupo\n"
        "/start - Menu inicial"
    )


def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("add_result", add_result))
    app.add_handler(CommandHandler("stats", stats))
    app.add_handler(CommandHandler("clear", clear))
    app.add_handler(CommandHandler("reset", reset))
    app.add_handler(CommandHandler("help", help_command))

    logger.info("🤖 Bot iniciado! Pressione Ctrl+C para parar.")
    app.run_polling()


if __name__ == "__main__":
    main()
