import telebot
import pprint
import time
from telebot import types

from _templates_constants import (
    first_words,
    price_list,
    empty_reciepe,
    reciepe,
    last_status,
    busket
    )

from sql_functions import (
    SQL_register_new_user,
    SQL_get_user_data,
    # SQL_put_user_phone
    )

from base_functions import (
    symbols,
    preparing_custom_buttons,
    writting_recipe2txt,
    calculate_cost,
    add_order_to_busket,
    writting_busket_info
    )

TOKEN = '5778281282:AAHAPOtzeP7_qofFxkkb0KxgSJzhMarWn-Y'  # Sergey_bot
telebot.apihelper.ENABLE_MIDDLEWARE = True
bot = telebot.TeleBot(TOKEN)
pp = pprint.PrettyPrinter(indent=3)


def draw_main_view():
    main_display = types.InlineKeyboardMarkup(row_width=2)
    btn_catalog = types.InlineKeyboardButton(f'{symbols[14]} Каталог', callback_data="Каталог")
    btn_custom = types.InlineKeyboardButton(f'{symbols[0]} Свой торт', callback_data="Свой торт")
    btn_profile = types.InlineKeyboardButton(f'{symbols[16]} Профиль', callback_data="Профиль")
    btn_busket = types.InlineKeyboardButton(f'{symbols[15]} Корзина', callback_data="Корзина")
    btn_support = types.InlineKeyboardButton(f'{symbols[18]} Поддержка', callback_data="Поддержка")
    btn_chat = types.InlineKeyboardButton(f'{symbols[17]} Чат', callback_data="Чат")
    main_display.add(btn_catalog, btn_custom, btn_profile,
                     btn_busket, btn_support, btn_chat)

    return main_display


def draw_custom_cake_view(add2busket=True):
    global busket

    buttons = preparing_custom_buttons(reciepe)
    custom_display = types.InlineKeyboardMarkup(row_width=2)
    c_btn11 = types.InlineKeyboardButton(buttons[0], callback_data='Levels')
    c_btn12 = types.InlineKeyboardButton(buttons[3], callback_data='Berries')
    c_btn21 = types.InlineKeyboardButton(buttons[1], callback_data='Form')
    c_btn22 = types.InlineKeyboardButton(buttons[4], callback_data='Decor')
    c_btn31 = types.InlineKeyboardButton(buttons[2], callback_data='Topping')
    c_btn32 = types.InlineKeyboardButton(buttons[5], callback_data='Label')

    if len(busket) >= 1:
        custom_display.row(types.InlineKeyboardButton(f'{symbols[15]} Перейти к корзине({len(busket)})', callback_data="Корзина"))

    if add2busket:
        if reciepe['Количество уровней'] and reciepe['Форма'] and reciepe['Топпинг']:
            custom_display.row(types.InlineKeyboardButton(f'{symbols[15]} Добавить в корзину', callback_data='Add2buscket'))
    custom_display.row(c_btn11, c_btn12)
    custom_display.row(c_btn21, c_btn22)
    custom_display.row(c_btn31, c_btn32)
    custom_display.row(types.InlineKeyboardButton('‹ Назад', callback_data='Main Page'))

    # custom_buttons = [types.InlineKeyboardButton(key1, callback_data=key2) for key1, key2 in buttons]
    # custom_buttons.append(types.InlineKeyboardButton('‹ Назад', callback_data='Main Page'))
    # custom_display.add(*custom_buttons)

    return custom_display


# ------------------------------------------ START

@bot.message_handler(commands=['start'])
def start_message(message):
    global first_words

    user_name = message.from_user.full_name
    user_login = message.from_user.username
    user_tg_id = message.from_user.id
    user = SQL_get_user_data(user_tg_id)
    if not user_name:
        user_name = user_login
    if not user:
        SQL_register_new_user(user_name, user_login, user_tg_id)

    main_display = draw_main_view()
    bot.send_message(
                chat_id=message.chat.id,
                text=first_words,
                parse_mode='html',
                disable_web_page_preview=True,
                reply_markup=main_display
                )


# ------------------------------------------ CALL BACK

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):

    global reciepe
    global empty_reciepe
    global first_words
    global price_list
    global symbols
    global last_status
    global busket

    if call.message:

        if call.data == 'Main Page':
            main_display = draw_main_view()
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=first_words,
                parse_mode='html',
                disable_web_page_preview=True,
                reply_markup=main_display
                )

        if call.data == 'Свой торт':
            custom_display = draw_custom_cake_view()
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=writting_recipe2txt(reciepe),
                reply_markup=custom_display
                )

        if call.data.split('^')[0] == 'Change':
            getting_data = call.data.split('^')
            getting_data.remove(getting_data[0])
            if getting_data[0] == 'Levels':
                reciepe['Количество уровней'] = getting_data[1]
                reciepe['Стоимость'] = calculate_cost(reciepe, price_list)
            if getting_data[0] == 'Form':
                reciepe['Форма'] = getting_data[1]
                reciepe['Стоимость'] = calculate_cost(reciepe, price_list)
            if getting_data[0] == 'Topping':
                reciepe['Топпинг'] = getting_data[1]
                reciepe['Стоимость'] = calculate_cost(reciepe, price_list)
            if getting_data[0] == 'Berries':
                reciepe['Ягоды'] = getting_data[1]
                if getting_data[1] == 'Cancel':
                    reciepe['Ягоды'] = False
                reciepe['Стоимость'] = calculate_cost(reciepe, price_list)
            if getting_data[0] == 'Decor':
                reciepe['Декор'] = getting_data[1]
                if getting_data[1] == 'Cancel':
                    reciepe['Декор'] = False
                reciepe['Стоимость'] = calculate_cost(reciepe, price_list)
            if getting_data[0] == 'Label':
                reciepe['Надпись'] = getting_data[1]
                if getting_data[1] == 'Cancel':
                    reciepe['Надпись'] = False
                reciepe['Стоимость'] = calculate_cost(reciepe, price_list)

            custom_display = draw_custom_cake_view()
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=writting_recipe2txt(reciepe),
                reply_markup=custom_display
                )

        if call.data == "Levels":
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            buttons = [types.InlineKeyboardButton(f'{key} ({value} р.)', callback_data=f'Change^Levels^{key}') for key, value in price_list['Количество уровней'].items()]
            buttons.append(types.InlineKeyboardButton('‹ Назад', callback_data="Свой торт"))
            keyboard.add(*buttons)
            text_message = call.message.text
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=text_message,
                reply_markup=keyboard
                )

        if call.data == "Form":
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            buttons = [types.InlineKeyboardButton(f'{key} ({value} р.)', callback_data=f'Change^Form^{key}') for key, value in price_list['Форма'].items()]
            buttons.append(types.InlineKeyboardButton('‹ Назад', callback_data="Свой торт"))
            keyboard.add(*buttons)
            text_message = call.message.text
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=text_message,
                reply_markup=keyboard
                )

        if call.data == "Topping":
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            buttons = [types.InlineKeyboardButton(f'{key} ({value} р.)', callback_data=f'Change^Topping^{key}') for key, value in price_list['Топпинг'].items()]
            buttons.append(types.InlineKeyboardButton('‹ Назад', callback_data="Свой торт"))
            keyboard.add(*buttons)
            text_message = call.message.text
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=text_message,
                reply_markup=keyboard
                )

        if call.data == "Berries":
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            buttons = [types.InlineKeyboardButton(f'{key} ({value} р.)', callback_data=f'Change^Berries^{key}') for key, value in price_list['Ягоды'].items()]
            if reciepe['Ягоды']:
                buttons.append(types.InlineKeyboardButton(f'{symbols[13]} Без ягод {symbols[13]}', callback_data=f'Change^Berries^Cancel'))
            buttons.append(types.InlineKeyboardButton('‹ Назад', callback_data="Свой торт"))
            keyboard.add(*buttons)
            text_message = call.message.text
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=text_message,
                reply_markup=keyboard
                )

        if call.data == "Decor":
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            buttons = [types.InlineKeyboardButton(f'{key} ({value} р.)', callback_data=f'Change^Decor^{key}') for key, value in price_list['Декор'].items()]
            if reciepe['Декор']:
                buttons.append(types.InlineKeyboardButton(f'{symbols[13]} Без декора {symbols[13]}', callback_data=f'Change^Decor^Cancel'))
            buttons.append(types.InlineKeyboardButton('‹ Назад', callback_data="Свой торт"))
            keyboard.add(*buttons)
            text_message = call.message.text
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=text_message,
                reply_markup=keyboard
                )

        if call.data == "Label":
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            buttons = []
            last_status = 'ADD TEXT'
            if reciepe['Надпись']:
                buttons.append(types.InlineKeyboardButton(f'{symbols[13]} Без надписи {symbols[13]}', callback_data=f'Change^Label^Cancel'))
            buttons.append(types.InlineKeyboardButton('‹ Назад', callback_data="Свой торт"))
            keyboard.add(*buttons)
            text_message = writting_recipe2txt(reciepe) + '\n*отправьте текст надписи\nсообщением в чат'
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=text_message,
                reply_markup=keyboard
                )

        if call.data == "Add2buscket":
            del_msg = bot.send_message(call.message.chat.id, f'{symbols[3]} Торт добавлен в корзину.').message_id
            add_order_to_busket(busket, reciepe, reciepe['Стоимость'])
            for item in reciepe:
                reciepe[item] = False
            custom_display = draw_custom_cake_view(add2busket=False)
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=writting_recipe2txt(reciepe),
                parse_mode='html',
                disable_web_page_preview=True,
                reply_markup=custom_display
                )
            time.sleep(2)
            bot.delete_message(call.message.chat.id, del_msg)

        if call.data == "Корзина":
            busket_display = types.InlineKeyboardMarkup(row_width=1)
            for item in busket:
                busket_display.add(types.InlineKeyboardButton(f'#{item}: Посмотреть/Удалить', callback_data=f'Busket^Item^{item}'))
            busket_display.row(types.InlineKeyboardButton('‹ Назад', callback_data='Main Page'))
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=writting_busket_info(busket),
                reply_markup=busket_display
                )

# ------------------------------------------ ECHO
@bot.message_handler(content_types=['text'])
def echo_message(message):
    global last_status
    global reciepe

    if last_status == 'ADD TEXT':
        bot.send_message(message.chat.id, f'{symbols[3]} Надпись успешно добавлена.')
        reciepe['Надпись'] = message.text
        reciepe['Стоимость'] = calculate_cost(reciepe, price_list)
        custom_display = draw_custom_cake_view()
        bot.send_message(
            chat_id=message.chat.id,
            text=writting_recipe2txt(reciepe),
            reply_markup=custom_display
            )

    # bot.send_message(message.chat.id, message.text.encode())
    # print(message.text.encode())


if __name__ == '__main__':

    bot.infinity_polling()
