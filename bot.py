import telebot
import random

from telebot import types
from config import bot_token, eng, ru


bot = telebot.TeleBot(bot_token)


@bot.message_handler(commands=['start'])
def start_bot(message):
    if message.from_user.last_name == None:
        bot.send_message(message.chat.id, f'⭐️ Привет, {message.from_user.first_name}, добро пожаловать в игру Виселица!\n'
                                          f'\n🤖 Этот бот знаком со всеми нарицательными существительными русского языка и в каждой новой игре он случайным образом выбирает одно из ~51 тысячи существующих. '
                                          f'Слова, написанные через дефис, бот предлагать не будет.\n'
                                          f'\n✨ Чтобы начать новую игру, используй команду /play')
    else:
        bot.send_message(message.chat.id, f'⭐️ Привет, {message.from_user.first_name} {message.from_user.last_name}, добро пожаловать в игру Виселица!\n'
                         f'\n🤖 Этот бот знаком со всеми нарицательными существительными русского языка и в каждой новой игре он случайным образом выбирает одно из ~51 тысячи существующих. '
                         f'Слова, написанные через дефис, бот предлагать не будет.\n'
                         f'\n✨ Чтобы начать новую игру, используй команду /play')


@bot.message_handler(commands=['play'])
def play_game(message):
    bot.send_message(message.chat.id, '⚡️ Новая игра началась !\nВведите желаемое количество попыток (не более 20):')
    bot.register_next_step_handler(message, tries_num)


def replay_game(message):
    bot.send_message(message.chat.id, 'Вам нужно выбрать число от 1 до 20 !\nВведите желаемое количество попыток (не более 20):')
    bot.register_next_step_handler(message, tries_num)


@bot.message_handler()
def tries_num(message):

    word = list(random.choice(open('russian_nouns.txt', encoding='utf-8').read().split()))
    unknown_word_list = list('_' * len(word))
    unknown_word = '_ ' * len(word)
    symbols = len(word)
    symbols_guessed = 0
    choices = []

    try:
        if int(message.text) > 20:
            bot.send_message(message.chat.id, '⛔️ Вы ввели число, больше максимального !')
            replay_game(message)
            return
        elif int(message.text) <= 0:
            bot.send_message(message.chat.id, '⛔️️ Количество попыток не должно быть отрицательным или равным нулю !')
            replay_game(message)
            return
        else:
            tries = int(message.text)
            total_tries = int(message.text)
            bot.send_message(message.chat.id, f'✅ Отлично, количество ваших попыток равно {message.text} !')
            game_info(message, word, unknown_word_list, unknown_word, symbols, symbols_guessed, tries, choices, eng, ru, total_tries)
            return
    except:
        if message.text.startswith('/start'):
            start_bot(message)
            return
        elif message.text.startswith('/play'):
            play_game(message)
            return
        else:
            bot.send_message(message.chat.id, '⛔️ Количество попыток должно быть целым числом !')
            replay_game(message)
            return


def game_info(message, word, unknown_word_list, unknown_word, symbols, symbols_guessed, tries, choices, eng, ru, total_tries):

    bot.send_message(message.chat.id, f'🔒 Загаданное слово: {" ".join(unknown_word_list)}\n'
                                      f'🔎 Букв отгадано: {symbols_guessed} из {symbols}\n'
                                      f'📝 Осталось попыток: {tries}\n'
                                      f'☑️ Буквы, которые уже были использованы: {", ".join(choices)}')
    bot.send_message(message.chat.id, 'Введите букву:')
    bot.register_next_step_handler(message, game, word, unknown_word_list, unknown_word, symbols, symbols_guessed, tries, choices, eng, ru, total_tries)
    return


def same_letter(message, letter, word, unknown_word_list, unknown_word, symbols, symbols_guessed, tries, choices, eng, ru, total_tries):
    bot.send_message(message.chat.id, f'⛔️ Буква {letter.upper()} уже была использована ранее !')
    bot.send_message(message.chat.id, 'Введите букву:')
    bot.register_next_step_handler(message, game, word, unknown_word_list, unknown_word, symbols, symbols_guessed, tries, choices, eng, ru, total_tries)
    return


def wrong_letter(message, word, unknown_word_list, unknown_word, symbols, symbols_guessed, tries, choices, eng, ru, total_tries):
    bot.send_message(message.chat.id, f'🔒 Загаданное слово: {" ".join(unknown_word_list)}\n'
                                      f'🔎 Букв отгадано: {symbols_guessed} из {symbols}\n'
                                      f'📝 Осталось попыток: {tries}\n'
                                      f'☑️ Буквы, которые уже были использованы: {", ".join(choices)}')
    bot.send_message(message.chat.id, 'Введите букву:')
    bot.register_next_step_handler(message, game, word, unknown_word_list, unknown_word, symbols, symbols_guessed, tries, choices, eng, ru, total_tries)
    return


def win(message, word, tries, choices, total_tries):
    bot.send_message(message.chat.id, '🎉 Поздравляю, вы выиграли !')
    bot.send_sticker(message.chat.id, sticker='CAACAgIAAxkBAAEMo4VmuhFPt1O5IlyGD0XtVwhA9on8SAACcCIAAq7-4Er8II1NUPOSrTUE')
    bot.send_message(message.chat.id, f'🔑 Слово, которое вы угадали: {"".join(word).upper()}\n'
                                      f'🪄 Попыток было использовано: {total_tries - tries} из {total_tries}\n'
                                      f'✏️ Использованные буквы: {", ".join(choices)}')
    if_win(message, word)
    return


def if_win(message, word):
    buttons = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton(f'Узнать значение слова "{"".join(word)}"', url=f'https://ru.wiktionary.org/wiki/{"".join(word).lower()}')
    buttons.row(button1)
    bot.send_message(message.chat.id, '🔥 Игра окончена !\nЧтобы начать новую, используйте команду /play\nЧтобы перезапустить бота, используйте команду /start', reply_markup=buttons)
    return


def lose(message, word, tries, choices, total_tries):
    bot.send_message(message.chat.id, '💀 К сожалению, вы проиграли.')
    bot.send_sticker(message.chat.id, sticker='CAACAgIAAxkBAAEMo41muhay0Fe1yYPs_047FFORpNO_7QACUSgAAts3qEr5ao1UtSI6YjUE')
    bot.send_message(message.chat.id, f'🔑 Слово, которое вы не угадали: {"".join(word).upper()}\n'
                                      f'🪄 Попыток было использовано: {total_tries - tries} из {total_tries}\n'
                                      f'✏️ Использованные буквы: {", ".join(choices)}')
    if_lose(message, word)
    return


def if_lose(message, word):
    buttons = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton(f'Узнать значение слова "{"".join(word)}"', url=f'https://ru.wiktionary.org/wiki/{"".join(word).lower()}')
    buttons.row(button1)
    bot.send_message(message.chat.id, '🌧 Игра окончена !\nЧтобы начать новую, используйте команду /play\nЧтобы перезапустить бота, используйте команду /start', reply_markup=buttons)
    return


@bot.message_handler()
def game(message, word, unknown_word_list, unknown_word, symbols, symbols_guessed, tries, choices, eng, ru, total_tries):

    letter = message.text.lower()

    if tries >= 1:
        found = False
        for i in range(len(word)):
            if letter == word[i]:
                unknown_word_list.pop(i)
                unknown_word_list.insert(i, letter.upper())
                found = True

        if message.text.startswith('/start'):
            start_bot(message)
            return
        elif message.text.startswith('/play'):
            play_game(message)
            return

        elif letter.lower() in ru:
            if found:
                if letter.lower() not in choices:
                    symbols_guessed = len(word) - unknown_word_list.count('_')
                    choices.extend(letter)
                    bot.send_message(message.chat.id, f'✅ Верно !')
                    if symbols_guessed != symbols:
                        game_info(message, word, unknown_word_list, unknown_word, symbols, symbols_guessed, tries, choices, eng, ru, total_tries)
                        return
                    else:
                        win(message, word, tries, choices, total_tries)
                        return
                else:
                    same_letter(message, letter, word, unknown_word_list, unknown_word, symbols, symbols_guessed, tries, choices, eng, ru, total_tries)
                    return
            else:
                if letter.lower() not in choices:
                    if tries > 1:
                        choices.extend(letter)
                        tries -= 1
                        bot.send_message(message.chat.id, f'❌️ Буква выбрана неверно, попробуйте еще раз !')
                        wrong_letter(message, word, unknown_word_list, unknown_word, symbols, symbols_guessed, tries, choices, eng, ru, total_tries)
                        return
                    elif tries == 1:
                        choices.extend(letter)
                        tries -= 1
                        bot.send_message(message.chat.id, f'❌️ Буква выбрана неверно !')
                        lose(message, word, tries, choices, total_tries)
                        return
                else:
                    same_letter(message, letter, word, unknown_word_list, unknown_word, symbols, symbols_guessed, tries, choices, eng, ru, total_tries)
                    return
        else:
            if len(letter) > 1:
                bot.send_message(message.chat.id, f'⛔ Вам нужно ввести не более одного символа !')
                wrong_letter(message, word, unknown_word_list, unknown_word, symbols, symbols_guessed, tries, choices, eng, ru, total_tries)
                return
            elif letter.lower() in eng:
                bot.send_message(message.chat.id, f'⛔️ Введите букву кириллического алфавита !')
                wrong_letter(message, word, unknown_word_list, unknown_word, symbols, symbols_guessed, tries, choices, eng, ru, total_tries)
                return
            else:
                bot.send_message(message.chat.id, f'⛔️ Вам нужно ввести букву !\nВы же, все-таки, слово угадываете :)')
                wrong_letter(message, word, unknown_word_list, unknown_word, symbols, symbols_guessed, tries, choices, eng, ru, total_tries)
                return


bot.infinity_polling()
