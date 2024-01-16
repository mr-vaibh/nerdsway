# context_processors.py
from config import BRAND_NAME, BRAND_LOGO

def brand_info(request):
    return {'brand_name': BRAND_NAME, 'brand_logo': BRAND_LOGO}