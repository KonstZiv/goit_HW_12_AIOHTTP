from sqlalchemy import create_engine, MetaData

from aiohttp_mentions.settings import config
from aiohttp_mentions.db import resource, word_scope, mention


DSN = "postgresql://{user}:{password}@{host}:{port}/{database}"


def create_tables(engine):
    meta = MetaData()
    meta.create_all(bind=engine, tables=[resource, word_scope, mention])


def sample_data(engine):
    conn = engine.connect()
    conn.execute(resource.insert(), [
        {'name': 'Glavcom, front page',
         'url': 'https://glavcom.ua/'},
        {'name': 'Хвиля, front page',
         'url': 'https://hvylya.net/'},
        {'name': 'OBOZREVATEL',
         'url': 'https://www.obozrevatel.com/'},
        {'name': 'UKR.NET',
         'url': 'https://www.ukr.net/'},
        {'name': 'BBC NEWS | Україна',
         'url': 'https://www.bbc.com/ukrainian'},
        {'name': 'Інтерфакс-Україна',
         'url': 'https://interfax.com.ua/'},
        {'name': 'УКРАИНСКАЯ ПРАВДА',
         'url': 'https://www.pravda.com.ua/rus/news/'},
        {'name': 'ЛІГА.НОВИНИ',
         'url': 'https://news.liga.net/'},
        {'name': 'UNN: украинские национальные новости',
         'url': 'https://www.unn.com.ua/ru/'},
        {'name': 'СЕГОДНЯ| Украина',
         'url': 'https://ukraine.segodnya.ua/'},
        {'name': 'КорреспонденТ.net',
         'url': 'https://korrespondent.net/'},
        {'name': 'ЦЕНЗОР.НЕТ',
         'url': 'https://censor.net/'},
        {'name': 'УНІАН',
         'url': 'https://www.unian.net/'},
        {'name': 'Gazeta.UA',
         'url': 'https://gazeta.ua/news'}

    ])
    conn.execute(word_scope.insert(), [
        {'name': 'Меркель', 'scope': 'Меркель Бундестаг '},
        {'name': 'Тарифы', 'scope': 'тарифы Тарифы отопление тарифи Тарифи опалення коммуналка коммуналку'},
        {'name': 'Донбас', 'scope': 'Донбас ДНР ТКГ Донецьк Луганськ Луганск'},
        {'name': 'Зеленский', 'scope': 'Зеленский Зеленський президент'}
    ])
    conn.close()


if __name__ == '__main__':
    db_url = DSN.format(**config['postgres'])
    print(db_url)
    engine = create_engine(db_url)

    create_tables(engine)
    sample_data(engine)
