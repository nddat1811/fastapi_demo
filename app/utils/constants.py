from enum import Enum


class Role(str, Enum):
    USER = 'user'
    ADMIN = 'admin'
    STAFF = 'staff'

class PriceWaterBill(Enum):
    LEVEL_1 = {'range': (0, 50), 'price': 1000}
    LEVEL_2 = {'range': (51, 100), 'price': 2000}
    LEVEL_3 = {'range': (101, float('inf')), 'price': 3000}


class PermissionEnum(Enum):
    EDIT = 'EDIT'
    DELETE = 'DELETE'
    CREATE = 'CREATE'
    EXPORT_EXCEL = 'EXPORT_EXCEL'
    VIEW = 'VIEW'


URL_PATH = {
    '/auth/login': False,
    '/hiu': False,
}