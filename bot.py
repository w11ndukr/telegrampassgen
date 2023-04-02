import random
import string
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

def generate_password(length: int, special_chars: bool = False, uppercase: bool = False) -> str:
    chars = string.ascii_lowercase
    if special_chars:
        chars += string.punctuation
    if uppercase:
        chars += string.ascii_uppercase
    return ''.join(random.choice(chars) for _ in range(length))

def start(update: Update, context: CallbackContext) -> None:
    context.bot.send_message(chat_id=update.effective_chat.id, text='Привет! Я бот-генератор паролей. Напиши /help, чтобы узнать, что я могу.')

def help(update: Update, context: CallbackContext) -> None:
    context.bot.send_message(chat_id=update.effective_chat.id, text='/password - сгенерировать новый пароль\n/save - сохранить пароль к определенному сервису')

def password(update: Update, context: CallbackContext) -> None:
    context.bot.send_message(chat_id=update.effective_chat.id, text='Выбери длину пароля (от 4 до 28):')
    context.user_data['password_length'] = True

def save(update: Update, context: CallbackContext) -> None:
    context.bot.send_message(chat_id=update.effective_chat.id, text='Введи название сервиса:')
    context.user_data['service'] = True

def validate_password_length(update: Update, context: CallbackContext) -> None:
    try:
        length = int(update.message.text)
        if length < 4 or length > 28:
            raise ValueError('Длина пароля должна быть от 4 до 28 символов.')
        context.user_data['password_length'] = length
        context.bot.send_message(chat_id=update.effective_chat.id, text='Включить специальные символы (да/нет)?')
        context.user_data['special_chars'] = True
    except ValueError as e:
        context.bot.send_message(chat_id=update.effective_chat.id, text=str(e))

def validate_special_chars(update: Update, context: CallbackContext) -> None:
    try:
        special_chars = update.message.text.lower() == 'да'
        context.user_data['special_chars'] = special_chars
        context.bot.send_message(chat_id=update.effective_chat.id, text='Включить заглавные буквы (да/нет)?')
        context.user_data['uppercase'] = True
    except ValueError as e:
        context.bot.send_message(chat_id=update.effective_chat.id, text=str(e))

def validate_uppercase(update: Update, context: CallbackContext) -> None:
    try:
        uppercase = update.message.text.lower() == 'да'
        context.user_data['uppercase'] = uppercase
        password = generate_password(context.user_data['password_length'], context.user_data['special_chars'], context.user_data['uppercase'])
        context.bot.send_message(chat_id=        update.effective_chat.id, text=f'Ваш пароль: {password}')
        context.user_data.clear()
    except ValueError as e:
        context.bot.send_message(chat_id=update.effective_chat.id, text=str(e))

def save_password(update: Update, context: CallbackContext) -> None:
    try:
        service = update.message.text
        password = generate_password(context.user_data['password_length'], context.user_data['special_chars'], context.user_data['uppercase'])
        context.bot.send_message(chat_id=update.effective_chat.id, text=f'Пароль для сервиса {service}: {password}')
        context.user_data.clear()
    except KeyError:
        context.bot.send_message(chat_id=update.effective_chat.id, text='Начните генерацию пароля с команды /password')

def main() -> None:
    updater = Updater(token=TOKEN, context=Context(command=Command))
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('help', help))
    dispatcher.add_handler(CommandHandler('password', password))
    dispatcher.add_handler(CommandHandler('save', save))

    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command & ~Filters.regex('^/'), 
                                           validate_password_length))
    dispatcher.add_handler(MessageHandler(Filters.regex('^(да|нет)$') & Filters.update.message & 
                                           Filters.user(user_id=update.effective_user.id),
                                           validate_special_chars))
    dispatcher.add_handler(MessageHandler(Filters.regex('^(да|нет)$') & Filters.update.message & 
                                           Filters.user(user_id=update.effective_user.id),
                                           validate_uppercase))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command & ~Filters.regex('^/'),
                                           save_password))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

