from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr


class OrderRequest():
    order:str