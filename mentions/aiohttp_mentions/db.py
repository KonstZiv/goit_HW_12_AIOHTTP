from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import (
    MetaData, Table, Column, ForeignKey, Integer, String, Text
)
from sqlalchemy.dialects.postgresql import TIMESTAMP

__all__ = ['resource', 'word_scope', 'mention']
meta = MetaData()
# описывает ресурс в интернете, где нужно отслеживать количество ссылок по какой-то тематике
resource = Table(
    'resource', meta,
    Column('id', Integer, primary_key=True),
    Column('name', String(50), nullable=False, unique=True),
    Column('url', String(200), nullable=False)
)
# описывает набор слов в поле scope разделенных пробелами, которые объединяются какой-то темой
# (название темы в поле name)
word_scope = Table(
    'word_scope', meta,
    Column('id', Integer, primary_key=True),
    Column('name', String(50), nullable=False, unique=True),
    Column('scope', Text, nullable=False)
)
# отражает количество упоминаний (поле result) по теме (связь с word_scope)
# через колонку scope_id на ресурсе (resource_id) в момент времени datetime
mention = Table(
    'mention', meta,
    Column('id', Integer, primary_key=True),
    Column('datetime', TIMESTAMP, nullable=False),
    Column('scope_name', String(50), ForeignKey(
        'word_scope.name', ondelete='CASCADE', onupdate='CASCADE')),
    Column('resource_name', String(50), ForeignKey(
        'resource.name', ondelete='CASCADE', onupdate='CASCADE')),
    Column('result', Integer)

)


async def pg_context(app):
    conf = app['config']['postgres']
    conn_str = f"postgresql+asyncpg://{conf['user']}:{conf['password']}@{conf['host']}/{conf['database']}"
    app['db'] = create_async_engine(conn_str, echo=True)

    yield

    # app['db'].close()
    await app['db'].wait_closed()
