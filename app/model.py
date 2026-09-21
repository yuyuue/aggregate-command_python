from datetime import date
from dataclasses import dataclass
from enum import Enum

class Department(Enum):
    HRS = "Human Resource"
    SLS = "Sales"
    ACC = "Account"
    MKT = "Market"

class ExpenseCategory(Enum):
    TRANSPORT = "transport"
    HOUSE = "house"
    OTHER = "other"

@dataclass(frozen=True)
class Expense:
    using_date: date
    department: Department
    applicant: str
    category: ExpenseCategory
    amount: int # 練習なのでint型、余裕があれば変更する。

class ExpenseHeader(Enum):
    DATE = "date"
    DEPARTMENT = "department"
    APPLICANT = "applicant"
    CATEGORY = "category"
    AMOUNT = "amount"
