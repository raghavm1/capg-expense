from datetime import datetime
from collections import defaultdict
from typing import List, Tuple
import json


class Category:
    def __init__(self, name, description=None, color=None):
        self.name = name
        self.categories = []

    def load_category_info(self, filepath):
        with open(filepath, "r") as f:
            data = json.load(f)
            self.categories = [Category.from_dict(item) for item in data]


class Expense:
    def __init__(self, category: str, amount: float, date: str):
        """
        category: e.g., 'Food', 'Transport'
        amount: float, e.g., 15.5
        date: str in 'YYYY-MM-DD' format
        """
        self.category = category
        self.amount = amount
        try:
            self.date = datetime.strptime(date, "%Y-%m-%d").date()
        except ValueError:
            raise ValueError("Date must be in YYYY-MM-DD format.")

    def to_dict(self):
        """For saving to JSON easily"""
        return {
            "category": self.category,
            "amount": self.amount,
            "date": self.date.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: dict):
        """Load from JSON easily"""
        return cls(category=data["category"], amount=data["amount"], date=data["date"])

    def __str__(self):
        return f"{self.date} | {self.category} | ${self.amount:.2f}"

    def __repr__(self):
        return f"Expense(category='{self.category}', amount={self.amount}, date='{self.date}')"


class ExpenseTracker:
    def __init__(self):
        self.expenses: List[Expense] = []

    def add_expense(self, category: str, amount: float, date: str):
        expense = Expense(category, amount, date)
        # TODO: check for category and add to stats

        # increment category expense too
        # load stats for that category
        self.expenses.append(expense)

    def get_total_expense(self) -> float:
        return sum(exp.amount for exp in self.expenses)

    def get_total_by_category(self) -> dict:
        category_totals = defaultdict(float)
        for exp in self.expenses:
            category_totals[exp.category] += exp.amount
        return dict(category_totals)

    def get_expense_trend(self) -> dict:
        """
        Returns a dict with dates as keys and total expenses for each date.
        """
        trend = defaultdict(float)
        for exp in self.expenses:
            trend[exp.date.isoformat()] += exp.amount
        return dict(sorted(trend.items()))  # Sorted chronologically

    def get_highest_and_lowest_category(self) -> Tuple[str, str]:
        category_totals = self.get_total_by_category()
        # load this data from storage, so that don't need to comptue again and again
        if not category_totals:
            return (None, None)
        highest = max(category_totals.items(), key=lambda x: x[1])[0]
        lowest = min(category_totals.items(), key=lambda x: x[1])[0]
        return highest, lowest

    def list_expenses(self) -> List[Expense]:
        """
        Returns the list of all expenses, sorted by date.
        """
        return sorted(self.expenses, key=lambda x: x.date)

    def save_to_file(self, filepath: str):
        """
        Saves expenses to a JSON file for persistence.
        """

        with open(filepath, "w") as f:
            json.dump([exp.to_dict() for exp in self.expenses], f, indent=2)

    def load_from_file(self, filepath: str = "expenses.json"):
        """
        Loads expenses from a JSON file.
        """
        try:
            with open(filepath, "r") as f:
                data = json.load(f)
                self.expenses = [Expense.from_dict(item) for item in data]
        except FileNotFoundError:
            # If file doesn't exist, start with empty expenses
            self.expenses = []
