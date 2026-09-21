from csv import DictReader
from datetime import date
from pathlib import Path

from model import Department, Expense, ExpenseCategory, ExpenseHeader

# TODO: 全体的に関数に入れる

here = Path(__file__).resolve()
root = here.parent.parent
EXPENSES_PATH_FROM_ROOT = "data/expences.csv"
path = Path(root/EXPENSES_PATH_FROM_ROOT)

expense_list: list[Expense] = []

with path.open(newline="", encoding="utf-8") as f:
    reader = DictReader(f)
    for row in reader:
        # TODO: 型変換時にValueErrorが出る可能性があるためハンドリング必要
        using_date = date.fromisoformat(row[ExpenseHeader.DATE.value])
        department = Department(row[ExpenseHeader.DEPARTMENT.value])
        applicant = row[ExpenseHeader.APPLICANT.value]
        category = ExpenseCategory(row[ExpenseHeader.CATEGORY.value])
        amount = int(row[ExpenseHeader.AMOUNT.value])
        expense_list.append(Expense(
            using_date,
            department,
            applicant,
            category,
            amount
        ))
