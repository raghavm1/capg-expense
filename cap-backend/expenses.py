from datetime import datetime, date
from collections import defaultdict
from typing import List, Tuple, Optional, Dict, Any
from decimal import Decimal, InvalidOperation
import json
import logging


logger = logging.getLogger(__name__)


class ExpenseValidationError(Exception):
    """Raised when expense data validation fails."""

    def __init__(self, message: str, field: Optional[str] = None, value: Any = None):
        self.message = message
        self.field = field
        self.value = value
        super().__init__(self.message)

    def __str__(self) -> str:
        if self.field:
            return f"Validation error in field '{self.field}': {self.message}"
        return f"Validation error: {self.message}"


class CategoryError(Exception):
    """Raised when category operations fail."""

    def __init__(self, message: str, category_name: Optional[str] = None):
        self.message = message
        self.category_name = category_name
        super().__init__(self.message)

    def __str__(self) -> str:
        if self.category_name:
            return f"Category error for '{self.category_name}': {self.message}"
        return f"Category error: {self.message}"


class Category:
    def __init__(
        self, name: str, description: Optional[str] = None, color: Optional[str] = None
    ):
        if not name or not name.strip():
            raise CategoryError("Category name cannot be empty", category_name=name)
        self.name = name.strip()
        self.description = description
        self.color = color

    def to_dict(self) -> Dict[str, Any]:
        return {"name": self.name, "description": self.description, "color": self.color}

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Category":
        return cls(
            name=data["name"],
            description=data.get("description"),
            color=data.get("color"),
        )

    def __eq__(self, other) -> bool:
        if not isinstance(other, Category):
            return False
        return self.name == other.name

    def __hash__(self) -> int:
        return hash(self.name)

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f"Category(name='{self.name}', description='{self.description}', color='{self.color}')"


class Expense:
    def __init__(
        self,
        category: str,
        amount: float,
        date_str: str,
        description: Optional[str] = None,
    ):
        self.category = self._validate_and_create_category(category)
        self.amount = self._validate_amount(amount)
        self.date = self._validate_date(date_str)
        self.description = description.strip() if description else None

    @staticmethod
    def _validate_and_create_category(category: str) -> Category:
        if not category or not category.strip():
            raise ExpenseValidationError(
                "Category cannot be empty", field="category", value=category
            )
        return Category(name=category.strip())

    @staticmethod
    def _validate_amount(amount: float) -> float:
        try:
            amount_decimal = Decimal(str(amount))
            if amount_decimal <= 0:
                raise ExpenseValidationError(
                    "Amount must be positive", field="amount", value=amount
                )
            return float(amount_decimal)
        except (InvalidOperation, ValueError):
            raise ExpenseValidationError(
                "Invalid amount format", field="amount", value=amount
            )

    @staticmethod
    def _validate_date(date_str: str) -> date:
        try:
            return datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            raise ExpenseValidationError(
                "Date must be in YYYY-MM-DD format", field="date", value=date_str
            )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "category": self.category.name,
            "amount": self.amount,
            "date": self.date.isoformat(),
            "description": self.description,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Expense":
        return cls(
            category=data["category"],
            amount=data["amount"],
            date_str=data["date"],
            description=data.get("description"),
        )

    def __eq__(self, other) -> bool:
        if not isinstance(other, Expense):
            return False
        return (
            self.category == other.category
            and self.amount == other.amount
            and self.date == other.date
        )

    def __hash__(self) -> int:
        return hash((self.category, self.amount, self.date))

    def __str__(self) -> str:
        return f"{self.date} | {self.category.name} | ${self.amount:.2f}"

    def __repr__(self) -> str:
        return f"Expense(category='{self.category.name}', amount={self.amount}, date='{self.date}', description='{self.description}')"


class ExpenseTracker:
    def __init__(self):
        self._expenses: List[Expense] = []

    @property
    def expenses(self) -> List[Expense]:
        return self._expenses.copy()

    def add_expense(
        self,
        category: str,
        amount: float,
        date_str: str,
        description: Optional[str] = None,
    ) -> Expense:
        try:
            expense = Expense(category, amount, date_str, description)
            self._expenses.append(expense)
            logger.info(f"Added expense: {expense}")
            return expense
        except ExpenseValidationError as e:
            logger.error(f"Failed to add expense: {e}")
            raise

    def remove_expense(self, expense: Expense) -> bool:
        try:
            self._expenses.remove(expense)
            logger.info(f"Removed expense: {expense}")
            return True
        except ValueError:
            logger.warning(f"Expense not found for removal: {expense}")
            return False

    def get_total_expense(self) -> float:
        return sum(exp.amount for exp in self._expenses)

    def get_total_by_category(self) -> Dict[str, float]:
        category_totals = defaultdict(float)
        for exp in self._expenses:
            category_totals[exp.category.name] += exp.amount
        return dict(category_totals)

    def get_expense_trend(self) -> Dict[str, float]:
        trend = defaultdict(float)
        for exp in self._expenses:
            trend[exp.date.isoformat()] += exp.amount
        return dict(sorted(trend.items()))

    def get_highest_and_lowest_category(self) -> Tuple[Optional[str], Optional[str]]:
        category_totals = self.get_total_by_category()
        if not category_totals:
            return None, None

        highest = max(category_totals.items(), key=lambda x: x[1])[0]
        lowest = min(category_totals.items(), key=lambda x: x[1])[0]
        return highest, lowest

    def list_expenses(self, sort_by_date: bool = True) -> List[Expense]:
        if sort_by_date:
            return sorted(self._expenses, key=lambda x: x.date)
        return self._expenses.copy()

    def get_expenses_by_category(self, category: str) -> List[Expense]:
        return [
            exp
            for exp in self._expenses
            if exp.category.name.lower() == category.lower()
        ]

    def get_expenses_by_date_range(
        self, start_date: date, end_date: date
    ) -> List[Expense]:
        return [exp for exp in self._expenses if start_date <= exp.date <= end_date]

    def get_all_categories(self) -> List[Category]:
        """Get all unique categories used in expenses."""
        categories = set()
        for exp in self._expenses:
            categories.add(exp.category)
        return list(categories)

    def get_category_statistics(self) -> Dict[str, Dict[str, Any]]:
        """Get detailed statistics for each category."""
        category_stats = {}
        category_totals = self.get_total_by_category()

        for category_name, total in category_totals.items():
            category_expenses = self.get_expenses_by_category(category_name)
            category_stats[category_name] = {
                "total_amount": total,
                "expense_count": len(category_expenses),
                "average_amount": (
                    total / len(category_expenses) if category_expenses else 0
                ),
                "min_amount": (
                    min(exp.amount for exp in category_expenses)
                    if category_expenses
                    else 0
                ),
                "max_amount": (
                    max(exp.amount for exp in category_expenses)
                    if category_expenses
                    else 0
                ),
            }

        return category_stats

    def save_to_file(self, filepath: str) -> None:
        try:
            with open(filepath, "w") as f:
                json.dump([exp.to_dict() for exp in self._expenses], f, indent=2)
            logger.info(f"Saved {len(self._expenses)} expenses to {filepath}")
        except (IOError, OSError) as e:
            logger.error(f"Failed to save expenses to file: {e}")
            raise

    def load_from_file(self, filepath: str = "expenses.json") -> None:
        try:
            with open(filepath, "r") as f:
                data = json.load(f)
                self._expenses = [Expense.from_dict(item) for item in data]
            logger.info(f"Loaded {len(self._expenses)} expenses from {filepath}")
        except FileNotFoundError:
            logger.info(f"File {filepath} not found, starting with empty expenses")
            self._expenses = []
        except (json.JSONDecodeError, KeyError, ExpenseValidationError) as e:
            logger.error(f"Failed to load expenses from file: {e}")
            raise

    def clear_all_expenses(self) -> None:
        count = len(self._expenses)
        self._expenses.clear()
        logger.info(f"Cleared {count} expenses")

    def get_statistics(self) -> Dict[str, Any]:
        total = self.get_total_expense()
        by_category = self.get_total_by_category()
        trend = self.get_expense_trend()
        highest, lowest = self.get_highest_and_lowest_category()

        return {
            "total_expenses": total,
            "expense_count": len(self._expenses),
            "categories": list(by_category.keys()),
            "category_totals": by_category,
            "expense_trend": trend,
            "highest_category": highest,
            "lowest_category": lowest,
        }
