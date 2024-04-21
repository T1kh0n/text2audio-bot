from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext

import pyttsx3
import langid

import os


# personal token
TOKEN = '7048327417:AAF75w3dOtqyWe9_E2zanpSykADCbsdk_HQ'


# bot class initialization
class TelegramBot:
    def __init__(self, token):
        self.token = token

        self.path = os.getcwd()

    # start command initialization
    async def start_command(self, update: Update, context: CallbackContext) -> None:
        await context.bot.send_message(chat_id=update.effective_chat.id, text='Привет! Скидывай мне свой текст, а я его озвучу.')

    # speak initialization
    async def speak_command(self, update: Update, context: CallbackContext) -> None:
        # extracting text from message
        user_message = update.message.text.replace('/speak', '')[1::]
        print(user_message)

        print(len(user_message))
        if len(user_message) == 0:
            await context.bot.send_message(chat_id=update.effective_chat.id, text='Хм, ты забыл написать текст.')

        else:
            # pyttsx3 engine initialization
            engine = pyttsx3.init()

            # setting properties
            engine.setProperty('rate', 150)

            if langid.classify(user_message) != 'en':
                for voice in engine.getProperty('voices'):
                    if voice.name == 'russian':
                        print('RUSSIAN')
                        engine.setProperty('voice', voice.id)
                        engine.setProperty('rate', 110)
                        break

            # saving speech to a file
            engine.save_to_file(user_message, f'{self.path}/speech.mp3')
            engine.runAndWait()

            # sending the speech file
            with open(f'{self.path}/speech.mp3', 'rb') as audio_file:
                await context.bot.send_voice(chat_id=update.effective_chat.id, voice=audio_file, caption='А вот озвучка твоего текста')

    def run(self):
        application = Application.builder().token(self.token).build()

        # adding commands
        application.add_handler(CommandHandler('start', self.start_command))
        application.add_handler(CommandHandler('speak', self.speak_command))

        print('Bot started successfully')

        # running bot
        application.run_polling()



if __name__ == '__main__':
    print('Starting the bot...')

    bot = TelegramBot(TOKEN)
    bot.run()