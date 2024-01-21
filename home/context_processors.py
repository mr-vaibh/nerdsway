# context_processors.py
from config import BRAND_NAME, BRAND_NAME_CASE, BRAND_LOGO

def brand_info(request):
    return {
        'brand_name': BRAND_NAME,
        'brand_name_case': BRAND_NAME_CASE,
        'brand_logo': BRAND_LOGO
    }