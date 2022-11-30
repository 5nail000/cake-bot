import pandas
import pprint
from pathlib import Path

# from sql_functions import ( SQL_register_new_order )


pp = pprint.PrettyPrinter(indent=3)

symbols = [
    b'\xf0\x9f\x8d\xb0'.decode('utf-8'),  # 0 Кусок торта с вишенкой
    b'\xf0\x9f\x8e\x82'.decode('utf-8'),  # 1 Торт со свечами
    b'\xf0\x9f\x8d\xa5'.decode('utf-8'),  # 2 Спираль в кружеве
    b'\xe2\x9c\x85'.decode('utf-8'),      # 3 Галочка 'Сделано'
    b'\xf0\x9f\x94\x8d'.decode('utf-8'),  # 4 Лупа
    b'\xf0\x9f\x92\xb0'.decode('utf-8'),  # 5 Мешок денег
    b'\xf0\x9f\x8d\xa9'.decode('utf-8'),  # 6: Топпинг
    b'\xf0\x9f\xa5\x9e'.decode('utf-8'),  # 7: Слои
    b'\xf0\x9f\x8d\x93'.decode('utf-8'),  # 8: Ягоды
    b'\xf0\x9f\xa4\x8e'.decode('utf-8'),  # 9: Форма (сердце)
    b'\xf0\x9f\xa5\xa8'.decode('utf-8'),  # 10: Декор
    b'\xe2\x9e\x95'.decode('utf-8'),      # 11: +++
    b'\xe2\x93\x82\xef\xb8\x8f'.decode('utf-8'),  # 12 Надпись
    b'\xe2\x9c\x96\xef\xb8\x8f'.decode('utf-8'),  # 13 X
    b'\xf0\x9f\xa5\xae'.decode('utf-8'),  # 14 MOON_CAKE
    b'\xf0\x9f\x9b\x92'.decode('utf-8'),  # 15 SHOPPING
    b'\xf0\x9f\x91\xa4'.decode('utf-8'),  # 16 SILHOUETTE
    b'\xf0\x9f\x92\xac'.decode('utf-8'),  # 17 CHAT
    b'\xf0\x9f\x9a\xb8'.decode('utf-8'),  # 18 SUPPORT
    ]


def read_excel_column(excelfile, col):
    column = pandas.read_excel(
        excelfile,
        index_col=None,
        usecols=col,
        na_filter=False
        )
    category = column.columns[0]
    column = column.to_dict('tight')['data']

    product_price = {}
    for item in column:
        if len(item[0]) < 1:
            continue
        product_price.update({item[0]: item[1]})
    return {category: product_price}


def read_pricelist_custom():

    file_loc = Path.cwd().joinpath('data').joinpath('prices_custom.xlsx')

    price_list_custom = {}
    price_list_custom.update(read_excel_column(file_loc, "B:C"))  # Кол-во уров
    price_list_custom.update(read_excel_column(file_loc, "E:F"))  # Форма
    price_list_custom.update(read_excel_column(file_loc, "H:I"))  # Топпинг
    price_list_custom.update(read_excel_column(file_loc, "K:L"))  # Ягоды
    price_list_custom.update(read_excel_column(file_loc, "N:O"))  # Декор

    text_label = pandas.read_excel(
        file_loc,
        index_col=None,
        usecols='Q:Q',
        na_filter=False).to_dict('split')['data'][0][0]

    price_list_custom.update({'Надпись': text_label})  # Надпись

    return price_list_custom


def preparing_custom_buttons(reciepe):
    buttons = []
    if reciepe['Количество уровней']:
        buttons.append(f'{symbols[7]} Количество уровней')
    else:
        buttons.append(f'Количество уровней {symbols[11]}')

    if reciepe['Форма']:
        buttons.append(f'{symbols[9]} Форма')
    else:
        buttons.append(f'{symbols[9]} Форма {symbols[11]}')

    if reciepe['Топпинг']:
        buttons.append(f'{symbols[6]} Топпинг')
    else:
        buttons.append(f'{symbols[6]} Топпинг {symbols[11]}')

    if reciepe['Ягоды']:
        buttons.append(f'{symbols[8]} Ягоды')
    else:
        buttons.append(f'{symbols[8]} Ягоды')

    if reciepe['Декор']:
        buttons.append(f'{symbols[10]} Декор')
    else:
        buttons.append(f'{symbols[10]} Декор')

    if reciepe['Надпись']:
        buttons.append(f'{symbols[12]} Изменить надпись')
    else:
        buttons.append(f'{symbols[12]} Добавить надпись')

    return buttons


def writting_recipe2txt(reciepe: dict):
    global symbols
    text = ''

    if reciepe['Количество уровней']:
        text = f"Количество уровней: {reciepe['Количество уровней']} \n"
    if reciepe['Форма']:
        text += f"Форма: {reciepe['Форма']} \n"
    if reciepe['Топпинг']:
        text += f"Топпинг: {reciepe['Топпинг']} \n"
    if reciepe['Ягоды']:
        text += f"Ягоды: {reciepe['Ягоды']} \n"
    if reciepe['Декор']:
        text += f"Декор: {reciepe['Декор']} \n"
    if reciepe['Надпись']:
        text += f"Надпись: {reciepe['Надпись']} \n"

    header = f' {symbols[0]} Ваш новый рецепт {symbols[0]}' + '\n'
    header += '------------------------------------------------' + '\n\n'

    footer = '\n'
    footer += '------------------------------------------------' + '\n'
    if reciepe['Стоимость'] != 0:
        footer += f"Стоимость: {reciepe['Стоимость']}"
    if len(text) < 1:
        text = '(ещё ничего не выбрано)' + '\n'

    text = header + text + footer
    return text


def calculate_cost(reciepe, price_list):
    cost = 0
    if reciepe['Количество уровней']:
        cost += price_list['Количество уровней'][reciepe['Количество уровней']]
    if reciepe['Форма']:
        cost += price_list['Форма'][reciepe['Форма']]
    if reciepe['Топпинг']:
        cost += price_list['Топпинг'][reciepe['Топпинг']]
    if reciepe['Ягоды']:
        cost += price_list['Ягоды'][reciepe['Ягоды']]
    if reciepe['Декор']:
        cost += price_list['Декор'][reciepe['Декор']]
    if reciepe['Надпись']:
        cost += price_list['Надпись']

    if cost == 0:
        cost = False
    return cost


def add_order_to_busket(busket, recipe, price):
    busket.update({
        len(busket) + 1: {
            'recipe': recipe,
            'price': price
            }
        })
    return busket

def writting_busket_info(busket):
    text = ''
    num = 0
    for item in busket:
        num += 1
        text += f"Выбор #{num}: {busket[item]['price']} рублей"
    if len(text) < 1:
        text = '(Выбранных заказов нет)'

    return text


'''
def delete_from_busket(busket, id):
    busket.pop(id)
    new_busket = {}
    num = 1
    for item in busket:
        new_busket.update({num: busket[item]})
        num += 1

    return new_busket


def confirm_busket2order(user_id, busket, all_addreses):

    num = 0
    total_price = 0
    order_info_txt = '===== ЗАКАЗ =====' + '\n'
    order_info_txt += '=================' + '\n'
    order_info_txt += '' + '\n'
    for item in busket:
        num += 1
        order_info_txt += 'Торт #{num}:' + '\n'
        order_info_txt += '' + '\n'
        order_info_txt += formatting_recipe2txt(busket[item]['recipe'])
        order_info_txt += f"Cтоимость: {busket[item]['price']}" + '\n'
        order_info_txt += '' + '\n'
        total_price += busket[item]['price']
    order_info_txt += '=================' + '\n'
    order_info_txt += f"ИТОГО: {total_price}" + '\n'
    order_info_txt += '' + '\n'
    order_info_txt += 'Адрес доставки:' + '\n'
    if not all_addreses:
        order_info_txt += 'не указан' + '\n'
    else:
        order_info_txt += all_addreses[0] + '\n'
    order_info_txt += '' + '\n'

    # print(order_info_txt)

    if not all_addreses:
        pass
        # Код для отображения кнопки и функционала "указать адрес"
    else:
        pass
        # Код для отображения кнопки и функционала "изменить адрес"
        #  - Указать новый
        #  - Выбрать из истории

    order_address = ""

    # --- Код для добавления/изменения коментария
    order_comment = ""

    # --- Код для указания даты и времени заказа.
    order_date = ""
    order_time = ""

    # --- Кнопка. Отправить заказ в обработку
    SQL_register_new_order(user_id,  # TG_id
                           recipe=order_info_txt,
                           price=total_price,
                           address=order_address,
                           delivery_date=order_date,
                           delivery_time=order_time,
                           comment=order_comment
                           )


# pp.pprint(read_pricelist_custom())
'''
