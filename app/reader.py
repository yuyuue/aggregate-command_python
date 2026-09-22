from csv import DictReader
from datetime import date
from pathlib import Path

from model import Department, Expense, ExpenseCategory, ExpenseHeader

def retrieve_expenses_file_path(path_from_root: str = "data/expences.csv") -> Path:
    here = Path(__file__).resolve()
    root = here.parent.parent
    return(Path(root/path_from_root))


def read_expenses(path: Path):
    expense_list: list[Expense] = []

    with path.open(newline="", encoding="utf-8") as f:
        reader = DictReader(f)
        for row in reader:
            expense_list.append(convert_expense(row))


def convert_expense(expense_dict: dict) -> Expense:
    using_date = date.fromisoformat(expense_dict[ExpenseHeader.DATE.value])
    department = Department(expense_dict[ExpenseHeader.DEPARTMENT.value])
    applicant = expense_dict[ExpenseHeader.APPLICANT.value]
    category = ExpenseCategory(expense_dict[ExpenseHeader.CATEGORY.value])
    amount = int(expense_dict[ExpenseHeader.AMOUNT.value])
    return Expense(
        using_date,
        department,
        applicant,
        category,
        amount
    )

if __name__ == "__main__":
    read_expenses(
        retrieve_expenses_file_path()
    )
