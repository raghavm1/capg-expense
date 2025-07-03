from flask import Flask, jsonify, request
from flask_cors import CORS
from expenses import ExpenseTracker, ExpenseValidationError, CategoryError
import json
from datetime import datetime
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize expense tracker in memory TODO: add SQL later
tracker = ExpenseTracker()


@app.route("/api/expenses", methods=["GET"])
def get_expenses():
    """Get all expenses"""
    expenses = []
    for expense in tracker.list_expenses():
        expenses.append(
            {
                "id": f"{expense.date.isoformat()}_{expense.category.name}_{expense.amount}",
                "category": expense.category.name,
                "amount": expense.amount,
                "date": expense.date.isoformat(),
                "description": expense.description or "",
            }
        )
    return jsonify(expenses)


@app.route("/api/expenses", methods=["POST"])
def add_expense():
    """Add a new expense"""
    data = request.json

    if not data or "category" not in data or "amount" not in data or "date" not in data:
        return (
            jsonify({"error": "Missing required fields: category, amount, date"}),
            400,
        )

    try:
        expense = tracker.add_expense(
            category=data["category"],
            amount=float(data["amount"]),
            date_str=data["date"],
            description=data.get("description"),
        )

        # Save to file immediately after adding
        try:
            tracker.save_to_file("expenses.json")
            print(
                f"Expense added and saved to file: {data['category']} - ${data['amount']}"
            )
        except Exception as e:
            print(f"Error saving expense to file: {e}")

        return (
            jsonify(
                {
                    "id": f"{expense.date.isoformat()}_{expense.category.name}_{expense.amount}",
                    "category": expense.category.name,
                    "amount": expense.amount,
                    "date": expense.date.isoformat(),
                    "description": expense.description or "",
                }
            ),
            201,
        )
    except (ValueError, Exception) as e:
        return jsonify({"error": str(e)}), 400


@app.route("/api/expenses/<expense_id>", methods=["DELETE"])
def delete_expense(expense_id):
    """Delete an expense by ID"""
    # For in-memory implementation, we'll need to parse the ID and remove the expense
    try:
        # Parse the ID format: date_category_amount
        parts = expense_id.split("_")
        if len(parts) < 3:
            return jsonify({"error": "Invalid expense ID format"}), 400

        date_str = parts[0]
        category = "_".join(parts[1:-1])  # Handle categories with underscores
        amount = float(parts[-1])

        # Find and remove the expense
        for expense in tracker.expenses:
            if (
                expense.date.isoformat() == date_str
                and expense.category.name == category
                and expense.amount == amount
            ):
                if tracker.remove_expense(expense):
                    # Save to file immediately after deleting
                    try:
                        tracker.save_to_file("expenses.json")
                        print(
                            f"Expense deleted and saved to file: {expense.category.name} - ${expense.amount}"
                        )
                    except Exception as e:
                        print(f"Error saving after deletion to file: {e}")
                    return jsonify({"message": "Expense deleted successfully"}), 200

        return jsonify({"error": "Expense not found"}), 404
    except (ValueError, IndexError) as e:
        return jsonify({"error": "Invalid expense ID format"}), 400


@app.route("/api/statistics", methods=["GET"])
def get_statistics():
    """Get expense statistics"""
    total_expense = tracker.get_total_expense()
    total_by_category = tracker.get_total_by_category()
    expense_trend = tracker.get_expense_trend()
    highest_category, lowest_category = tracker.get_highest_and_lowest_category()

    return jsonify(
        {
            "total_expense": total_expense,
            "total_by_category": total_by_category,
            "expense_trend": expense_trend,
            "highest_category": highest_category,
            "lowest_category": lowest_category,
        }
    )


@app.route("/api/expenses/category/<category>", methods=["GET"])
def get_expenses_by_category(category):
    """Get expenses for a specific category"""
    expenses = []
    for expense in tracker.get_expenses_by_category(category):
        expenses.append(
            {
                "id": f"{expense.date.isoformat()}_{expense.category.name}_{expense.amount}",
                "category": expense.category.name,
                "amount": expense.amount,
                "date": expense.date.isoformat(),
                "description": expense.description or "",
            }
        )
    return jsonify(expenses)


@app.route("/api/health", methods=["GET"])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "message": "Expense Tracker API is running"})


if __name__ == "__main__":
    # Load some sample data if available
    try:
        tracker.load_from_file("expenses.json")
        print("Loaded existing expenses from file")
    except FileNotFoundError:
        print("No existing expenses file found, starting with empty tracker")

    app.run(debug=True, host="0.0.0.0", port=5000)
