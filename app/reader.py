'''
reader.py
'''

from csv import DictReader
from dataclasses import dataclass
from datetime import date
import logging
from pathlib import Path

from model import Department, Expense, ExpenseCategory, ExpenseHeaderName, ExpenseHeaderKey
from util.validator import ExpenseValidationError, validate, Rule

logging.basicConfig(format="%(asctime)s [%(levelname)s] %(name)s: %(message)s", level=logging.DEBUG)
logger = logging.getLogger(__name__) # エントリーポイントを作成したタイミングで移行する。

@dataclass(frozen=True)
class ReadResult:
    valid_expenses: dict[int, Expense]
    errors: dict[int, str]

def retrieve_expenses_file_path(path_from_root: str = "data/expences.csv") -> Path:
    here = Path(__file__).resolve()
    root = here.parent.parent
    return(Path(root/path_from_root))

def read_expenses(path: Path) -> ReadResult:
    valid_expenses: dict[int, Expense] = {}
    expense_errors: dict[int, str] = {}

    with path.open(newline="", encoding="utf-8") as f:
        reader = DictReader(f)
        for row in reader:
            try:
                valid_expenses[reader.line_num] = convert_expense(row)
                logger.info(f'{reader.line_num}行目を変換')
            except ExpenseValidationError as e:
                expense_errors[reader.line_num] = e.__str__()
                logger.warning(f'{reader.line_num}行目でエラー: {e}')
            except Exception as e:
                expense_errors[reader.line_num] = e.__str__()
                logger.error(f'{reader.line_num}行目でエラー: {e}')

    return ReadResult(valid_expenses, expense_errors)

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
