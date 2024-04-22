from enum import Enum


class Role(str, Enum):
    USER = 'user'
    ADMIN = 'admin'
    STAFF = 'staff'

class PriceWaterBill(Enum):
    LEVEL_1 = {'range': (0, 50), 'price': 1000}
    LEVEL_2 = {'range': (51, 100), 'price': 2000}
    LEVEL_3 = {'range': (101, float('inf')), 'price': 3000}