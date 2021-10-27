import logging
import aiohttp
import asyncio
import re
from datetime import datetime

import db
from db import mention


async def get_resources(app):
    # возвращает из БД список словарей [{'id': XX, 'name': 'Glavrom', 'url': 'https://gla.....'}]
    async with app['db'].begin() as conn:
        cursor = await conn.execute(db.resource.select())
        records = cursor.fetchall()
        return [dict(s) for s in records]


async def get_scpoes(app):
    # возвращает из БД сок словарей [{'id_scope': XX, 'name': 'Меркель', 'scope': ['Меркель', 'Бундестаг' ,.....'], ...}]
    async with app['db'].begin() as conn:
        cursor = await conn.execute(db.word_scope.select())
        records = cursor.fetchall()
        scopes = [dict(s) for s in records]
        print('scopes = ', scopes)
        return [{'id': scope['id'], 'name': scope['name'], 'scope': scope['scope'].split()} for scope in scopes]


async def put_data_to_db(app, data):
    # полученные данные data записывает в БД, соединение к которой хранится в app['db']
    async with app['db'].begin() as conn:
        await conn.execute(mention.insert(), data)


def get_table_data(data):
    # конвертирует данные data формата get_data() в формат
    # --> {resource_name_1: {scope_1: res 1,
    #                       scope_2: res_2,
    #                       .............},
    #      resource_name_2: {scope_1: res 1,
    #                       scope_2: res_2,
    #                       .............},
    #     ...............................}
    table_data = {}
    for result in data:
        if not result['resource_name'] in table_data:
            table_data[result['resource_name']] = {}
        table_data[result['resource_name']
                   ][result['scope_name']] = result['result']
    return table_data


async def get_data(resources, scopes):
    # асинхнхронно делает запросы к ресурсам из resources и считает число повторений каждого элемента
    # темы scope['id'] по словам списка scope['scope'] и возвращает список словарей:
    # results = [{'datetime': XXX, 'scope_name': ZZZ, 'resource_name': YYY, 'result': FFF},
    #           {...}, ...]
    async with aiohttp.ClientSession() as session:
        results = []
        for resource in resources:
            try:
                async with session.get(resource['url']) as resp:
                    if resp.status == 200:
                        html = await resp.text()
                        for scope in scopes:
                            res = sum([len(re.findall(word, html))
                                       for word in scope['scope']])
                            results.append(
                                {
                                    'datetime': datetime.now().replace(microsecond=0),
                                    'scope_name': scope['name'],
                                    'resource_name': resource['name'],
                                    'result': res
                                })
                    else:
                        for scope in scopes:
                            results.append(
                                {
                                    'datetime': datetime.now().replace(microsecond=0),
                                    'scope_id': scope['id_scope'],
                                    'resource_id': resource['id'],
                                    'result': None
                                })
            except Exception as ex:
                print(f'ошибка в функции get_data(): {ex}')
        return results


async def main():
    a = await get_resources()
    print(a)


if __name__ == '__main__':

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
