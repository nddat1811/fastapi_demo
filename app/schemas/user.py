from datetime import date, datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr
from app.utils.constants import Role

class UserBase(BaseModel):
    username : str
    email : EmailStr
    dob : date

class User2Base(BaseModel):
    username: str
    email: str
    code: Optional[str] = None
    expiry: datetime
    refresh_token: Optional[str] = None
    created_at: datetime
    deleted_at: Optional[datetime] = None
    role: str
    id: int
    hashed_password: Optional[str] = None
    dob: datetime
    last_login: Optional[datetime] = None
    updated_at: datetime

{
    "total_items": 11,
    "total_pages": 2,
    "items": [ {
        "id": 1,
        "invoice_no": 329,
        "denominator": 1,
        "symbol": "C24TTP",
        "currency_unit": "VND",
        "seller_tax_code": "0313639411",
        "seller_address": "1128/4 Trường Sa, Phường 13, Quận Phú Nhuận, Thành Phố Hồ Chí Minh, Việt Nam",
        "seller_name": "CÔNG TY TNHH MÁY VĂN PHÒNG TIẾN PHÁT",
        "seller_bank_name": "Ngân Hàng TMCP Á Châu (ACB)",
        "seller_bank_number": "211752729",
        "buyer_tax_code": "0305260309",
        "buyer_address": "194/11M Bạch Đằng, Phường 24, Quận Bình Thạnh, TP Hồ Chí Minh, Việt Nam",
        "buyer_name": "Công Ty TNHH Thương Mại Dịch Vụ Viễn Thông Minh Phát",
        "buyer_bank_name": null,
        "buyer_bank_number": null,
        "buyer_phone":null,
        "payment_method": "Tiền mặt/Chuyển khoản",
        "invoice_code": "002C8753EA5FAC4CCB8569CF4F413C5494",
        "invoice_type_name": "HÓA ĐƠN GIÁ TRỊ GIA TĂNG",
        "total_amount_without_VAT": 863636.0,
        "total_VAT_amount": 69091.0,
        "total_payment_in_word": "Chín trăm ba mươi hai nghìn bảy trăm hai mươi bảy đồng",
        "total_payment_in_number": 932727.0,
        "statement_number": null,
        "statement_date": null, 
        "non_taxable_deduction_amount": null,
        "total_fee": null,
        "total_trade_discount": null,
        "total_other_deduction": null,
        "tax_authority_id": null, 
        "sync_datetime": null,
        "invoice_form": 1,
        "invoice_creation_date": "2024-04-24T17:00:00Z",
        "invoice_basic_id": "2c11c62a-0741-4e6a-ae4d-515b79843d76"
    }
    ]
}


{
    "id": 11,
    "invoice_no": 329,
    "denominator": 1,
    "symbol": "C24TTP",
    "currency_unit": "VND",
    "seller_tax_code": "0313639411",
    "seller_address": "1128/4 Trường Sa, Phường 13, Quận Phú Nhuận, Thành Phố Hồ Chí Minh, Việt Nam",
    "seller_name": "CÔNG TY TNHH MÁY VĂN PHÒNG TIẾN PHÁT",
    "seller_bank_name": "Ngân Hàng TMCP Á Châu (ACB)",
    "seller_bank_number": "211752729",
    "buyer_tax_code": "0305260309",
    "buyer_address": "194/11M Bạch Đằng, Phường 24, Quận Bình Thạnh, TP Hồ Chí Minh, Việt Nam",
    "buyer_name": "Công Ty TNHH Thương Mại Dịch Vụ Viễn Thông Minh Phát",
    "buyer_bank_name": null,
    "buyer_bank_number": null,
    "buyer_phone": null,
    "payment_method": "Tiền mặt/Chuyển khoản",
    "invoice_code": "002C8753EA5FAC4CCB8569CF4F413C5494",
    "invoice_type_name": "HÓA ĐƠN GIÁ TRỊ GIA TĂNG",
    "total_amount_without_VAT": 863636.0,
    "total_VAT_amount": 69091.0,
    "total_payment_in_word": "Chín trăm ba mươi hai nghìn bảy trăm hai mươi bảy đồng",
    "total_payment_in_number": 932727.0,
    "statement_number": null,
    "statement_date": null,
    "non_taxable_deduction_amount": null,
    "total_fee": null,
    "total_trade_discount": null,
    "total_other_deduction": null,
    "tax_authority_id": null,
    "sync_datetime": null,
    "invoice_form": 1,
    "invoice_creation_date": "2024-04-24T17:00:00Z",
    "invoice_basic_id": "2c11c62a-0741-4e6a-ae4d-515b79843d76",
    "invoice_detail": {
        "unit_price":863636.111111,
        "unit": "Cái",
        "interest_rate": "8%",
        "quantity":1,
        "item_name": "Sim mobi",
        "discount":null,
        "items": [{
            "item_name":"Sim",
            "ref_item_name":"Sim Mobi",
            "created_by": {
                "full_name":"Đạt",
            }
        }]
    }
}



{
    "total_items": 12,
    "total_pages": 2,
    "items": [ {
        "id": 1,
        "name": "User View",
        "description": "Vai trò xem danh sách user",
        "status": 0,
        "created_at": "2024-04-23T01:39:12.824747",
        "updated_at": "2024-04-23T01:39:12.824747",
        "creator": {  
                "id": 1,
                "username": "nddat1811",
                "email": "datnd@gmail.com"
        },
        "functions": [
        {  
                "id": 2,
                "name": "Xem danh sách user",
                "path": "/users/get-list",
                "description": "Chức năng xem danh sách user",
                "icon_url": "url",
        }
        ]
    },
    {
        "id": 2,
        "name": "User EDIT",
        "description": "Vai trò sửa thông tin user",
        "status": 0,
        "created_at": "2024-04-23T01:39:12.824747",
        "updated_at": "2024-04-23T01:39:12.824747",
        "creator": {  
                "id": 1,
                "username": "nddat1811",
                "email": "datnd@gmail.com"
        },
        "functions": [
        {  
                "id": 2,
                "name": "Sửa thông tin user",
                "path": "/users/edit",
                "description": "Chức năng sửa thông tin user",
                "icon_url": "url",
        }
        ]
    },
    ]
}
class User3Base(BaseModel):
    message: str
    data: User2Base

class UserDisplay(UserBase):
    id : int
    message : str
    role : Role

class UserResetPasswordRequest(BaseModel):
    new_pass: str
    conf_pass: str
    user_id: int

class ResetPasswordResponse(BaseModel):
    id: int
    username: str
    email: str
    dob: date

class UpdateUserRequest(BaseModel):
    role : Role
    dob : date

class UpdateRoleRequest(BaseModel):
    role : Role

class ForgotPasswordRequest(BaseModel):
    email: str

class CheckCodePasswordRequest(BaseModel):
    code: str