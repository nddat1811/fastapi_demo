
from .constants import PriceWaterBill

def calculate_price(volume):
    for price_level in PriceWaterBill:
        if volume >= price_level.value['range'][0] and volume <= price_level.value['range'][1]:
            return price_level.value['price']
    return None