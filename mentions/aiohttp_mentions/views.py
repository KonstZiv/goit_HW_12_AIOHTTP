from importlib import resources
from aiohttp import web
import aiohttp_jinja2
import db
from func import get_resources, get_scpoes, get_data, put_data_to_db, get_table_data


@aiohttp_jinja2.template('table.html')
async def index(request):
    resources = await get_resources(request.app)
    print('-' * 80)
    print(resources)
    print('-' * 80)
    scopes = await get_scpoes(request.app)
    print('-' * 80)
    print(scopes)
    print('-' * 80)
    data = await get_data(resources, scopes)
    print('-' * 80)
    print(data)
    print('-' * 80)
    await put_data_to_db(request.app, data)
    table_data = get_table_data(data)
    return {"table_data": table_data}


@aiohttp_jinja2.template('detail.html')
async def mention(request):
    async with request.app['db'].begin() as conn:
        question_id = request.match_info['question_id']
        try:
            question, choices = await db.get_question(conn,
                                                      question_id)
        except db.RecordNotFound as e:
            raise web.HTTPNotFound(text=str(e))
        return {
            'question': question,
            'choices': choices
        }
