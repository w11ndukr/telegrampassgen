from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

import random
import string

# Функция для генерации пароля заданной длины со специальными символами и/или заглавными буквами
def generate_password(length: int, special_chars: bool = False, uppercase: bool = False) -> str:
    chars = string.ascii_lowercase
    if special_chars:
        chars += string.punctuation
    if uppercase:
        chars += string.ascii_uppercase
    return ''.join(random.choice(chars) for _ in range(length))

# Обработчик команды /start
def start(update: Update, _: CallbackContext) -> None:
    update.message.reply_text('Привет! Я бот-генератор паролей. Напиши /help, чтобы узнать, что я могу.')

# Обработчик команды /help
def help(update: Update, _: CallbackContext) -> None:
    update.message.reply_text('/password - сгенерировать новый пароль\n/save - сохранить пароль к определенному сервису')

# Обработчик команды /password
def password(update: Update, _: CallbackContext) -> None:
    # Запрашиваем у пользователя параметры пароля
    update.message.reply_text('Выбери длину пароля (от 4 до 28):')
    length = int(update.message.text)
    update.message.reply_text('Включить специальные символы (да/нет)?')
    special_chars = update.message.text.lower() == 'да'
    update.message.reply_text('Включить заглавные буквы (да/нет)?')
    uppercase = update.message.text.lower() == 'да'

    # Генерируем пароль
    password = generate_password(length, special_chars, uppercase)

    # Отправляем пароль пользователю
    update.message.reply_text(f'Твой новый пароль: {password}')

# Обработчик команды /save
def save(update: Update, _: CallbackContext) -> None:
    # Получаем название сервиса
    update.message.reply_text('Введи название сервиса:')
    service = update.message.text

    # Получаем мастер-пароль для доступа к сохраненным паролям
    update.message.reply_text('Введи мастер-пароль для доступа к сохраненным паролям:')
    master_password = update.message.text

    # Запрашиваем у пользователя параметры пароля
    update.message.reply_text('Выбери длину пароля (от 4 до 28):')
    length = int(update.message.text)
    update.message.reply_text('Включить специальные символы (да/нет)?')
    special_chars = update.message.text.lower() == 'да'
    update.message.reply_text('Включить заглавные буквы (да/нет)?')
    uppercase = update.message.text.lower() == 'да'

    # Генерируем пароль
    password = generate_password(length, special_chars, uppercase)

        # Сохраняем пароль в файл
    with open('passwords.txt', 'a') as f:
        f.write(f'{service}:{password}\n')

    # Отправляем подтверждение пользователю
    update.message.reply_text(f'Пароль для сервиса {service} успешно сохранен.')

# Точка входа
def main() -> None:
    # Создаем экземпляр бота и получаем его токен
    updater = Updater('5969795803:AAFwj401KLrSwX34s8QqUrjXpb9kl-cWF10')

    # Создаем диспетчер и добавляем обработчики команд
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('help', help))
    dispatcher.add_handler(CommandHandler('password', password))
    dispatcher.add_handler(CommandHandler('save', save))

    # Запускаем бота
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

