'''
reader.py
'''

from csv import DictReader
from datetime import date
from pathlib import Path

from model import Department, Expense, ExpenseCategory, ExpenseHeaderName, ExpenseHeaderKey
from util.validator import ExpenseValidationError, validate, Rule

def retrieve_expenses_file_path(path_from_root: str = "data/expences.csv") -> Path:
    here = Path(__file__).resolve()
    root = here.parent.parent
    return(Path(root/path_from_root))

def read_expenses(path: Path) -> None:
    print('START')
    expense_list: list[Expense] = []

    with path.open(newline="", encoding="utf-8") as f:
        reader = DictReader(f)
        for row in reader:
            try:
                expense_list.append(convert_expense(row))
                print(f'{reader.line_num}行目を変換')
            except ExpenseValidationError as e:
                print(f'{reader.line_num}: {type(e)}: {e}')
            except Exception as e:
                print(f'{reader.line_num}: {type(e)}: {e}')

def convert_expense(expense_dict: dict) -> Expense:
    row_date = expense_dict[ExpenseHeaderKey.DATE.value]
    row_department = expense_dict[ExpenseHeaderKey.DEPARTMENT.value]
    row_applicant = expense_dict[ExpenseHeaderKey.APPLICANT.value]
    row_category = expense_dict[ExpenseHeaderKey.CATEGORY.value]
    row_amount = expense_dict[ExpenseHeaderKey.AMOUNT.value]

    validate(row_date, ExpenseHeaderName.DATE, Rule.DATE_FORMAT)
    validate(row_department, ExpenseHeaderName.DEPARTMENT, Rule.DEPARTMENT)
    validate(row_applicant, ExpenseHeaderName.APPLICANT, Rule.APPLICANT)
    validate(row_category, ExpenseHeaderName.CATEGORY, Rule.EXPENSE_CATEGORY)
    validate(row_amount, ExpenseHeaderName.AMOUNT, Rule.NATURAL_NUM)

    using_date = date.fromisoformat(row_date)
    department = Department(row_department)
    applicant = row_applicant
    category = ExpenseCategory(row_category)
    amount = int(row_amount)

    return Expense(using_date, department, applicant, category, amount)

if __name__ == "__main__":
    read_expenses(
        retrieve_expenses_file_path()
    )
