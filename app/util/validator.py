'''
validator.py
'''
from datetime import date
from enum import auto, IntEnum

from model import Department, ExpenseCategory

class Rule(IntEnum):
    DATE_FORMAT = auto()
    DEPARTMENT = auto()
    APPLICANT = auto()
    EXPENSE_CATEGORY = auto()
    NATURAL_NUM = auto()

class ExpenseValidationError(ValueError):
    pass

def validate(target, target_name,  rule: Rule) -> None:
    if target is None:
        raise TypeError("target引数は必須です。")

    if rule == Rule.DATE_FORMAT:
        _validate_date_format(target, target_name)
    elif rule == Rule.DEPARTMENT:
        _validate_department(target, target_name)
    elif rule == Rule.APPLICANT:
        _validate_applicant(target, target_name)
    elif rule == Rule.EXPENSE_CATEGORY:
        _validate_expense_category(target, target_name)
    elif rule == Rule.NATURAL_NUM:
        _validate_natural_num(target, target_name)

def _validate_date_format(target: str, target_name: str) -> None:
    try:
        date.fromisoformat(target)
    except ValueError as e:
        raise ExpenseValidationError(f'「{target_name}」は正常な日付ではありません。')

def _validate_department(target: str, target_name: str) -> None:
    try:
        Department(target)
    except ValueError:
        raise ExpenseValidationError(f'「{target_name}」は存在しない部門です。')

# target_nameは利用しないが統一感と将来性のため引数に含めている。
def _validate_applicant(target: str, target_name: str) -> None:
    if target == "":
        raise ExpenseValidationError(f'申請者が空欄です。')

def _validate_expense_category(target: str, target_name: str) -> None:
    try:
        ExpenseCategory(target)
    except ValueError:
        raise ExpenseValidationError(f'「{target_name}」はカテゴリ名に含まれていません。')

def _validate_natural_num(target: str, target_name: str) -> None:
    try:
        if int(target) < 0:
            raise ExpenseValidationError(f'「{target_name}」が自然数ではありません。')
    except ValueError:
        raise ExpenseValidationError(f'「{target_name}」が自然数ではありません。')

