import src.app as app
from waitress import serve
from config import Config

serve(app.create_app(), host=Config.host, port=Config.port)
