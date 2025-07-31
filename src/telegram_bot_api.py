from flask import request
from .gemini import Gemini
from md2tgmd import escape
from telegram.ext import ApplicationBuilder
from telegram import Update
from os import getenv
from io import BytesIO
from PIL import Image
from .enums import TelegramBotCommands
from .flask_app import app, db, ChatMessage, ChatSession


@app.get('/')
def hello_world():
    return 'Hello, World!'


@app.post('/webhook/<secret>')
async def webhook(secret):
    chat_id = None

    # Validate webhook secret from URL
    expected_secret = getenv('TELEGRAM_WEBHOOK_SECRET', 'SONU_SECRET_KEY')
    if secret != expected_secret:
        return "Unauthorized: Secret mismatch", 403

    telegram_app = ApplicationBuilder().token(getenv('TELEGRAM_BOT_TOKEN')).build()
    gemini = Gemini()

    try:
        body = request.get_json()
        if not body:
            return 'Invalid JSON body', 400

        update = Update.de_json(body, telegram_app.bot)
        if not update.message:
            return 'No message object in update', 200

        chat_id = update.message.chat_id

        # Session management
        session = db.session.query(ChatSession).filter_by(
            chat_id=chat_id).first()
        if not session:
            session = ChatSession(chat_id=chat_id, messages=[])
            db.session.add(session)
            db.session.commit()

        # Edited message? Ignore.
        if update.edited_message:
            return 'OK'

        # /start command
        if update.message.text == TelegramBotCommands.START:
            await telegram_app.bot.send_message(
                chat_id=chat_id,
                text="Welcome to Cyber Shaty. I can help you with any cyber related queries relevent to Nepal."
            )
            return 'OK'

        # /newchat command
        if update.message.text == TelegramBotCommands.NEW_CHAT:
            db.session.query(ChatMessage).filter_by(
                chat_id=session.id).delete()
            db.session.commit()
            await telegram_app.bot.send_message(chat_id=chat_id, text="New chat started.")
            return 'OK'

        # Processing message
        message = await telegram_app.bot.send_message(chat_id=chat_id, text="Processing your request...")
        message_id = message.message_id

        # Image handling
        if update.message.photo:
            app.logger.info("Image received")
            file_id = update.message.photo[-1].file_id
            app.logger.info("Image file id: " + str(file_id))

            file = await telegram_app.bot.get_file(file_id)
            bytes_array = await file.download_as_bytearray()
            image = Image.open(BytesIO(bytes_array))
            app.logger.info("Image loaded")

            prompt = update.message.caption if update.message.caption else 'Describe the image'
            print("Prompt is:", prompt)

            text = gemini.send_image(prompt, image)

            session.messages.append(ChatMessage(
                chat_id=chat_id, text=prompt, date=update.message.date, role="user"))
            session.messages.append(ChatMessage(
                chat_id=chat_id, text=text, date=update.message.date, role="model"))
            db.session.commit()

        # Text message
        else:
            history = [
                {
                    "role": message.role,
                    "parts": [{"text": message.text}]
                } for message in session.messages
            ]

            print("History:", history)
            chat = gemini.get_model().start_chat(history=history)
            text = gemini.send_message(update.message.text, chat)

            session.messages.append(ChatMessage(
                chat_id=chat_id, text=update.message.text, date=update.message.date, role="user"))
            session.messages.append(ChatMessage(
                chat_id=chat_id, text=text, date=update.message.date, role="model"))
            db.session.commit()

            print('Response:', text)

        await telegram_app.bot.edit_message_text(
            chat_id=chat_id,
            text=escape(text),
            message_id=message_id,
            parse_mode="MarkdownV2"
        )

        return 'OK'

    except Exception as error:
        print(f"Error Occurred: {error}")
        return {
            "method": "sendMessage",
            "chat_id": chat_id,
            "text": 'Sorry, I am not able to generate content for you right now. Please try again later.'
        }
