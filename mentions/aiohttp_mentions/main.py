from aiohttp import web
import aiohttp_jinja2
import jinja2
from routes import setup_routes
from settings import config, BASE_DIR
from db import pg_context

app = web.Application()
app['config'] = config
aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader(
    str(BASE_DIR / 'aiohttp_mentions' / 'templates')))
setup_routes(app)
app.cleanup_ctx.append(pg_context)

web.run_app(app, host='localhost', port=5000)
