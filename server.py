from waitress import serve
from config import Config
import app

serve(app.create_app(), host='0.0.0.0', port=Config.port)
