from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATABASE = str(BASE_DIR / 'store.db')
GOOD_TABLE = 'good'
CATEGORY_TABLE = 'category'
HOST = '0.0.0.0'
PORT = 5001
BASE_URL = f'http://127.0.0.1:{PORT}'
