import re
import pandas

strip_patterns = {
    '': [
        (r"\*\[25 лютого\]: за юліанським календарем.*", re.S),
        (r"^[\w ]*фото:.*?\n", re.M | re.I),
        (r"Теги:.*", re.S),
        (r"Читайте також: ?\n?\w+.*\n?", re.M),
        (r"Якщо побачили помилку.*", re.S), 
        (r"(^>.*\n)+", re.M), 
        (r"этот материал доступен на русском", re.I),
        (r"читать (новость )?на русском", re.I),
        (r"Цей матеріал можна прочитати і російською мовою\n", re.I),
        (r"^Реклама\n", re.M),
        (r"^Твитнуть\n", re.M)
    ],
    'apostrophe.ua': [
        (r"### Новини.*?Всі новини", re.S),
        (r"Версія для друку.*", re.S)
    ],
    'https://www.rbc.ua': [
        (r"Читайте нас в Google News та підписуйтесь.*", re.S),
        (r"Надіслати новину другу\nКому\:\*\nВаш коментар\nНадіслати(\nДякуємо, Ваше повідомлення відправлено\!  \n  \nOk\n)?", re.M)
    ],
    'https://www.unian.ua': [
        (r"Читайте останні новини України та світу.*", re.S),
        (r"Якщо ви знайшли помилку.*", re.S),
        (r"^Читайте також.*?\n", re.M)
    ],
    'https://censor.net.ua': [
        (r"^.*?Редактор Цензор\. НЕТ", re.S),
        (r"Мне нравится.*", re.S),
        (r"^Читайте (также )?на \"Цензор\. НЕТ\":.*?\n", re.M),
        (r"^Все про:.*?\n", re.M),
        (r"Топ комментарии.*", re.S)
    ],
    'https://politeka.net/uk': [
        (r"Популярні новини зараз.*?Показати ще", re.S)
    ],
    'www.radiosvoboda.org': [
        (r"^ДИВІТЬСЯ ТАКОЖ: ?\n####.*?\n", re.M),
        (r"### FACEBOOК КОМЕНТАРІ.*", re.S),
        (r"Отримати Adobe Flash Player.*\* \d+p | \d+(\,?\d+)?MB", re.S)
    ],
    'https://dt.ua/': [
        (r"(\^* #[\w ]+)+", re.M)
    ],
    'https://hromadske.ua/': [
        (r"Поділитись.*", re.S),
        (r"Більше про:.*", re.S),
        (r"^Інформаційна гігієна не менш важлива за особисту.*?\n", re.M),
        (r"### читайте також ?\n.*\n.*\n", re.M) ###???
    ],
    'https://www.obozrevatel.com': [
        (r"Тисни! Підписуйся!.*", re.S),
        (r"Ти ще не підписаний на наш Telegram.*", re.S),
        (r"Не набридаємо! Тільки найважливіше.*", re.S),
        (r"Підписуйся на наш Telegram.*", re.S),
        (r"^Читайте:.*?\n", re.M | re.I)
    ],
    'https://www.segodnya.ua/ua': [
        (r"^Також дивіться.*?\n", re.M),
        (r"Підпишись на наш telegram.*", re.S),
        (r"##### Ще кілька матеріалів по темі:.*", re.S)
    ],
    'focus.ua': [
        (r"^Читайте также.*\n", re.M),
#         (r"Как ранее сообщал Фокус:.*", re.S)
    ],
    '112.ua':[
        (r"^#\w+.*?#\w+.*\n", re.M),
        (r"^Новини за темою:.*?\n", re.M)
    ],
    'https://www.liga.net': [
        (r"^Читайте нас в Telegram:.*?\n", re.M),
        (r"Еще по теме.*", re.S),
        (r"Ще по темі.*", re.S),
        (r"^Читайте также.*\n", re.M)
    ],
    'espreso.tv':[
        (r"Слідкуйте за подіями в Україні та світі.*", re.S),
        (r"Все по темі.*", re.S),
        (r"Підписуйтесь на Telegram.*", re.S)
        # can't detect this parts in all domain, so leaving them for now
#         (r" \* Нагадаємо")
    ],
    'strana.ua': [
        (r"^Читайте также ?\n( ?\*.*?\n)+", re.M),
        (r"Подпишитесь на телеграм-канал.*", re.S),
        (r"Читайте Страну в Google News.*", re.S)
    ],
    'tsn.ua': [
        (r"^\* Facebook.*\* Відправити лист", re.S),
#         (r"###### Читайте також: ?\n\w+.*?\n", False),
        (r"Приєднуйтесь також до tsn\.ua у Google News.*", re.S),
         (r"^ ?\* ?(Facebook|Twitter|Telegram|Messenger|Viber)\n", re.M)
    ],
    'https://hromadske.radio': [
        (r"Підписуйтесь на Telegram-канал.*", re.S)
    ],
    'znaj.ua': [
        (r"Обов'язково підпишись.*", re.S),
        (r"Популярні новини зараз.*Показати ще", re.S),
        (r"Популярні новини.*", re.S)
    ],
    'fakty.com.ua': [
        (r"^Читайте:.*?\n", re.M)
    ],
    'https://www.epravda.com.ua': [
        (r"Читайте детальніше:.*", re.S)
#         (r"Нагадуємо:.*", re.S)
    ],
    'https://ukr.lb.ua': [
        (r"Читайте головні новини LB\.ua.*", re.S),
        (r"^(Facebook|Twitter)\n", re.M),
        (r"^Темы:.*", re.S|re.M)
    ],
    'https://ukranews.com': [
        (r"Больше новостей о:.*", re.S),
        (r"Коментарии Facebook.*", re.S),
        (r"^\* \d+\n \* \d+\n", re.S),
        (r"^Українські Новини\nУкраїнські Новини\n.*\n\#.*\n.*\n", re.M),
        (r"^Українські Новини\n.*\n\#.*\n.*\n", re.M)
    ],
   
    'zik.ua': [
        (r"^Новини за темою:.*?\n", re.M)
    ]
    
}


def mystip(df):
    for domain, patterns in strip_patterns.items():
        domain_mask = df.domain.str.contains(domain)
        for part_to_strip in patterns:
            df.text.update(df[domain_mask].text.str.replace(part_to_strip[0], "", flags=part_to_strip[1]))
        


