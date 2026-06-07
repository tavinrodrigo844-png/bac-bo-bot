import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Token do bot
BOT_TOKEN = os.getenv("8698797816:AAHANQTdKwZ5pGL-1fpZKIVmldgUg6vhBo0", "")

# Armazenar resultados
resultados = []

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /start"""
    await update.message.reply_text(
        "🎰 Bem-vindo ao Bot de Baccarat!\n\n"
        "Comandos disponíveis:\n"
        "/add_result [B/P/T] - Adicionar resultado (B=Banco, P=Jogador, T=Empate)\n"
        "/stats - Ver estatísticas\n"
        "/clear - Limpar histórico\n"
        "/help - Ajuda"
    )

async def add_result(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /add_result"""
    if not context.args:
        await update.message.reply_text("❌ Use: /add_result [B/P/T]")
        return
    
    resultado = context.args[0].upper()
    if resultado not in ['B', 'P', 'T']:
        await update.message.reply_text("❌ Resultado inválido! Use B (Banco), P (Jogador) ou T (Empate)")
        return
    
    resultados.append(resultado)
    nomes = {'B': '🏦 Banco', 'P': '👤 Jogador', 'T': '🤝 Empate'}
    await update.message.reply_text(f"✅ {nomes[resultado]} adicionado!\nTotal de resultados: {len(resultados)}")

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /stats"""
    if not resultados:
        await update.message.reply_text("📊 Nenhum resultado registrado ainda!")
        return
    
    banco = resultados.count('B')
    jogador = resultados.count('P')
    empate = resultados.count('T')
    total = len(resultados)
    
    mensagem = (
        f"📊 ESTATÍSTICAS\n"
        f"━━━━━━━━━━━━━━━━\n"
        f"🏦 Banco: {banco} ({banco/total*100:.1f}%)\n"
        f"👤 Jogador: {jogador} ({jogador/total*100:.1f}%)\n"
        f"🤝 Empate: {empate} ({empate/total*100:.1f}%)\n"
        f"━━━━━━━━━━━━━━━━\n"
        f"📈 Total: {total}"
    )
    await update.message.reply_text(mensagem)

async def clear(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /clear"""
    global resultados
    resultados = []
    await update.message.reply_text("🗑️ Histórico limpo!")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /help"""
    await update.message.reply_text(
        "🎰 AJUDA - Bot de Baccarat\n\n"
        "/add_result [B/P/T]\n"
        "Adiciona um resultado. Exemplos:\n"
        "• /add_result B (Banco venceu)\n"
        "• /add_result P (Jogador venceu)\n"
        "• /add_result T (Empate)\n\n"
        "/stats - Mostra estatísticas\n"
        "/clear - Limpa o histórico\n"
        "/start - Menu inicial"
    )

def main():
    """Inicia o bot"""
    if not BOT_TOKEN:
        print("8698797816:AAHANQTdKwZ5pGL-1fpZKIVmldgUg6vhBo0")
        return
    
    app = Application.builder().token(BOT_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("add_result", add_result))
    app.add_handler(CommandHandler("stats", stats))
    app.add_handler(CommandHandler("clear", clear))
    app.add_handler(CommandHandler("help", help_command))
    
    print("🤖 Bot iniciado! Pressione Ctrl+C para parar.")
    app.run_polling()

if __name__ == "__main__":
    main()
