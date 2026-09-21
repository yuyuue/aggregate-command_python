from datetime import datetime
from dataclasses import dataclass
from enum import Enum

@dataclass(frozen=True)
class ExpenceData:
    datetime: datetime
    department: Department
    applicant: str
    category: ExpenceCategory
    amout: int # 練習なのでint型、余裕があれば変更する。

class Department(Enum):
    HRS = "Human Resource"
    SLS = "Sales"
    ACC = "Account"
    MKT = "Market"

class ExpenceCategory(Enum):
    transport = "transport"
    house = "house"
    Other = "other"