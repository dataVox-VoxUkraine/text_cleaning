strip_patterns = {
#     parts to initially strip in all news 
    '': [
        (r"\*\[25 лютого\]: за юліанським календарем.*", re.S),
        (r"^[\w ]*фото:.*?\n", re.M | re.I),
        (r"Теги:.*", re.S),
        (r"Читайте також( статтю)?: ?\n?.*\n?", re.M | re.I),
        (r"Читайте більше:.*$", re.M),
        (r"Тако?же? читайте.*$", re.M),
        (r"Якщо (ви )?(побачили|виявили|помітили) помилку.*", re.S|re.I), 
        (r"Если Вы заметили орфографическую ошибку.*", re.S), 
        (r"Если вы нашли ошибку в тексте.*", re.S),
        (r"(^>.*\n)+", re.M), 
        (r"этот материал доступен на русском", re.I),
        (r"читать ((новость|этот материал) )?на русском", re.I),
        (r"Цей матеріал можна прочитати і російською мовою\n", re.I),
        (r"^Реклама$", re.M),
        (r"(ПУБЛИКАЦИИ|МАТЕРИАЛЫ) ПО ТЕМЕ.*", re.S),
        (r"^Твитнуть$", re.M),
        (r"\* {,4}\* Розсилка ?\nВІДПРАВИТИ\n?\n?\n?", re.S),
        (r"\n\n\nКопіювати код для вставки", re.S), 
        (r"^Цей матеріал також доступний українською$", re.M), 
        (r"^Нажмите на фото для увеличения изображения.*$", re.M),
        (r"https://[a-z\./0-9@:%_\+~#\?&=\-\(\)]+", re.I|re.M),
        (r"фото: instagram.com", re.M),
        (r"фото:? (ua\.)?depositphotos(\.com)?", re.M|re.I),
        (r"© president\.gov\.ua ?$", re.M),
        (r" ?\* ?Поділитися (на|у) (Facebook|Twitter|Telegram|ВКонтакте)$", re.M),
        (r"Share on .*$", re.M), 
        (r" ?\* ?Надіслати листом$", re.M),
        (r"^© ?REUTERS ?$", re.M),
        (r"^[\* ]*Кількість (переглядів|коментарів) \d* ?$", re.M),
        (r"^© фото president\.gov\.ua ?$", re.M),
        (r"Авторские права на изображение: TUT. BY", re.M),
        (r"^Коментувати Роздрукувати$", re.M),
        (r"Фото: ?Pixabay", re.I)

    ],
    
     # strip patterns by domains 
    
    'apostrophe.ua': [
        (r"### Новини.*?Всі новини", re.S),
        (r"Версія для друку.*", re.S),
        (r"\w+ новини тепер в Telegram.*", re.S),
        (r"^Читайте тако?же?.*$", re.M),
        (r"Підписуйтесь на канал.*", re.S),
        (r"^Поделиться$", re.M),
        (r"^1 \/ 1$", re.M)
    ],
    'https://www.rbc.ua': [
        (r"Читайте нас в Google News та підписуйтесь.*", re.S),
        (r"Надіслати новину другу\nКому\:\*\nВаш коментар\nНадіслати(\nДякуємо, Ваше повідомлення відправлено\!  \n  \nOk\n)?", re.M),
        (r"Дякуємо, Ваше повідомлення відправлено\!", re.M),
        (r"^Ok$", re.M)
    ],
    'https://www.unian.ua': [
        (r"Читайте останні новини України та світу.*", re.S),
        (r"Якщо ви знайшли помилку.*", re.S),
        (r"^Читайте тако?же?.*$", re.M)
    ],
    'https://censor.net.ua': [
        (r"^.*?Редактор Цензор\. НЕТ", re.S),
        (r"Мне нравится.*", re.S),
        (r"^Читайте (также ?)?(на \"?Цензор\. НЕТ\"?)?:.*?$", re.M),
#         (r"^Все про:.*?$", re.M),
        (r"Топ комментарии.*", re.S),
        (r"^Читайте:.*$", re.M),
        (r"\nИсточник:.*", re.S)
    ],
    'https://politeka.net/uk': [
        (r"Популярні новини зараз.*?Показати ще", re.S)
    ],
    'www.radiosvoboda.org': [
        (r"^ДИВІТЬСЯ ТАКОЖ: ?\n####.*?$", re.M),
        (r"### FACEBOO. КОМЕНТАРІ.*", re.S),
        (r"Отримати Adobe Flash Player.*\* \d+p | \d+(\,?\d+)?MB", re.S)
    ],
    'https://dt.ua/': [
        (r"(\^* #[\w ]+)+", re.M)
    ],
    'https://hromadske.ua/': [
        (r"Поділитись.*", re.S),
#         (r"Більше про:.*", re.S),
        (r"^Інформаційна гігієна не менш важлива за особисту.*?$", re.M),
        (r"### читайте також ?\n.*\n.*\n", re.M), ###???
        (r"### читайте також ?\n.*$", re.M)
    ],
    'https://www.obozrevatel.com': [
        (r"Тисни! Підписуйся!.*", re.S),
        (r"Ти ще не підписаний на наш Telegram.*", re.S),
        (r"Не набридаємо! Тільки найважливіше.*", re.S),
        (r"Підписуйся на наш Telegram.*", re.S),
        (r"^Читайте:.*?$", re.M | re.I)
    ],
    'https://www.segodnya.ua/ua': [
        (r"^Також дивіться.*?$", re.M),
        (r"Підпишись на наш telegram.*", re.S),
        (r"##### Ще кілька матеріалів по темі:.*", re.S),
        (r"^##### В тренді\n.*$", re.M)

    ],
    'focus.ua': [
        (r"^Читайте также.*$", re.M)
#         (r"Как ранее сообщал Фокус:.*", re.S)
    ],
    '112.ua':[
        (r"^#\w+.*?#\w+.*\n", re.M),
        (r"^Новини за темою:.*?$", re.M)
    ],
    'https://www.liga.net': [
        (r"^Читайте нас в Telegram:.*?$", re.M),
        (r"Еще по теме.*", re.S),
        (r"Ще по темі.*", re.S),
        (r"^Читайте также.*\n", re.M),
        (r"Присоединяйтесь к Instagram Liga.*", re.S)
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
        (r"^\* WhatsApp.*\* Відправити лист", re.S),
        (r"\* Відправити лист", re.S),
        (r"\* Повноекранний режим$", re.M),
#         (r"###### Читайте також: ?\n\w+.*?\n", False),
        (r"Приєднуйтесь також до tsn\.ua у Google News.*", re.S),
         (r"^ ?\* ?(Facebook|Twitter|Telegram|Messenger|Viber)$", re.M),
        (r"^ ?\* ?WhatsApp$", re.M),
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
        (r"^Читайте:.*?$", re.M)
    ],
    'https://www.epravda.com.ua': [
        (r"Читайте детальніше:.*", re.S)
#         (r"Нагадуємо:.*", re.S)
    ],
    'https://ukr.lb.ua': [
        (r"Читайте головні новини LB\.ua.*", re.S),
        (r"^(Facebook|Twitter)$", re.M),
        (r"^Темы:.*", re.S|re.M)
    ],
    'https://ukranews.com': [
        (r"Больше новостей о:.*", re.S),
        (r"Коментарии Facebook.*", re.S),
        (r"^\* \d+\n \* \d+\n", re.S),
        (r"^Українські Новини\nУкраїнські Новини\n.*\n\#.*\n.*\n", re.M),
        (r"^Українські Новини\n.*\n\#.*\n.*\n", re.M),
        (r"Читайте также:.*$", re.M)
    ],
   
    'zik.ua': [
        (r"^Новини за темою:.*?$", re.M)
    ],
    'https://ua.korrespondent.net/': [
        (r"Новини від Корреспондент\.net.*", re.S),
        (r"Підписуйтесь на наш канал.*", re.S)
       
    ],
    'vgolos.com.ua': [
        (r"###? Як писав \“Вголос\”:.*", re.S)
        
    ],
    'glavcom.ua': [
        (r"## Хроника событий.*", re.S),
        (r"Опитування$", re.M),
        (r"Читайте также:.*$", re.M),
        (r"Читайте також ?: ?\n?( \* .*\n?){1,}", re.M),
        (r"^на весь екран згорнути$", re.M)
    ],
    '24tv.ua': [
        (r"Читайте тако?же?:?.*$", re.M),
        (r"^Поділитися новиною ?$", re.M),
        (r"^ ?\* \* \* \* \* ?$", re.M)
    ], 
    'suspilne.media': [
        (r"## Що відомо.*", re.S),
        (r"## Читайте також.*", re.S),
        (r"(> )?Читайте також:.*", re.M)
    ],
    'babel.ua': [
        (r"(^ \* .*$){1,}$", re.M)
    ],
    # this shoud be the last part
    # patterns to finally strip in all news 
    # it is expected that every domain contains a dot
    '.': [
        (r"Читайте тако?же?:?\n?.*$", re.M | re.I),
        (r"^ ?\* ?$", re.M)
    ]

}


def remove_newlines(text):
    text = re.sub(r"\n \n", "\n", text)
    text = re.sub(r"\n{2,}", "\n", text)
    text = re.sub(r" {2,}", " ", text)
    text = text.strip()
    return text


def mystrip(df):
    for domain, patterns in strip_patterns.items():
        print(domain)
        domain_mask = df.domain.str.contains(domain)
        for part_to_strip in patterns:
            df.text.update(df[domain_mask].text.str.replace(part_to_strip[0], "", flags=part_to_strip[1]))
    df['text'] = df.text.apply(remove_newlines)


