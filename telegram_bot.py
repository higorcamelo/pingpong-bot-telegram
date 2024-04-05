import logging
import os
import time
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext, JobQueue, MessageHandler, filters
from dotenv import load_dotenv
from ping import pingURL

# Initialize logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO, filename= "log.txt")
logging.getLogger("httpx").setLevel(logging.INFO)

load_dotenv()

auth_token = os.getenv("TELEGRAM_KEY")

async def startMessage(update: Update, context: CallbackContext) -> None:
    message = """Já se perguntou quando um sistema caiu se foi só com você? Ou se foi com todo mundo? É para isso que estou aqui!
    Aqui estão os comandos que você pode usar:
    /ping (URL do site) - Testa a conexão com um site.
    /alert (URL do site) - Vou fazer verificações periodicas e te avisar quando o site voltar ao ar.
    """
    await context.bot.send_message(chat_id=update.effective_chat.id, text=message)
    
async def testConnection(update: Update, context: CallbackContext) -> None:
    url = context.args[0]
    if pingURL(url):
        message = f"O site {url} está online!"
    else:
        message = f"O site {url} está offline!"
    await context.bot.send_message(chat_id=update.effective_chat.id, text=message)
    
# Testar a cada 5 minutos se o site está offline e enviar mensagem se estiver online
async def alertSite(update: Update, context: CallbackContext) -> None:
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Certo, vou ficar de olho no site e te avisarei quando ele voltar!")
    
    
def main() -> None:
    app = Application.builder().token(auth_token).build()
    app.add_handler(CommandHandler("start", startMessage))
    app.add_handler(CommandHandler("ping", testConnection))
    app.add_handler(CommandHandler("alert", alertSite))
    
    app.run_polling(allowed_updates=Update.ALL_TYPES)

    
if __name__ == '__main__':
    main()