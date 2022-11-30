from base_functions import (
    symbols,
    read_pricelist_custom
    )

busket = {}
last_status = ''
first_words = f"{symbols[0]} Добро пожаловать {symbols[0]}\n\nЭто магазин {symbols[1]} тортов {symbols[1]}. Здесь вы можете выбрать как популярные рецепты, так и придумать свои {symbols[2]}\n\n<a href='https://dvmn.org/'>{symbols[3]} Подписывайтесь на наш канал, </a> что бы следить {symbols[4]} за актуальными новостями и акциями - получайте скидки {symbols[5]}"
price_list = read_pricelist_custom()
empty_reciepe = {
    'Количество уровней': False,
    'Форма': False,
    'Топпинг': False,
    'Ягоды': False,
    'Декор': False,
    'Надпись': False,
    'Стоимость': False
    }
reciepe = empty_reciepe
