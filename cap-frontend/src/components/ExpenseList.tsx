"use client";

import { format } from "date-fns";
import { Trash2, Calendar, Tag, DollarSign } from "lucide-react";
import { Expense } from "../services/api";

interface ExpenseListProps {
  expenses: Expense[];
  onDeleteExpense: (id: string) => void;
}

export default function ExpenseList({
  expenses,
  onDeleteExpense,
}: ExpenseListProps) {
  // Sort expenses by date (newest first)
  const sortedExpenses = [...expenses].sort(
    (a, b) => new Date(b.date).getTime() - new Date(a.date).getTime()
  );

  if (expenses.length === 0) {
    return (
      <div className="text-center py-12">
        <div className="text-gray-400 mb-4">
          <DollarSign size={48} className="mx-auto" />
        </div>
        <p className="text-gray-500 dark:text-gray-400 text-lg">
          No expenses recorded yet
        </p>
        <p className="text-gray-400 dark:text-gray-500 text-sm mt-2">
          Start by adding your first expense above
        </p>
      </div>
    );
  }

  return (
    <div className="space-y-3">
      {sortedExpenses.map((expense) => (
        <div
          key={expense.id}
          className="flex items-center justify-between p-4 bg-gray-50 dark:bg-gray-700 rounded-lg border border-gray-200 dark:border-gray-600 hover:bg-gray-100 dark:hover:bg-gray-600 transition-colors"
        >
          <div className="flex-1">
            <div className="flex items-center gap-3 mb-2">
              <div className="flex items-center gap-2">
                <Tag size={16} className="text-blue-500" />
                <span className="font-medium text-gray-900 dark:text-white">
                  {expense.category}
                </span>
              </div>
              <div className="flex items-center gap-2">
                <Calendar size={16} className="text-gray-500" />
                <span className="text-sm text-gray-500 dark:text-gray-400">
                  {format(new Date(expense.date), "MMM dd, yyyy")}
                </span>
              </div>
            </div>

            {expense.description && (
              <p className="text-sm text-gray-600 dark:text-gray-300 mb-2">
                {expense.description}
              </p>
            )}

            <div className="flex items-center gap-2">
              <DollarSign size={16} className="text-green-500" />
              <span className="text-lg font-semibold text-green-600 dark:text-green-400">
                ${expense.amount.toFixed(2)}
              </span>
            </div>
          </div>

          <button
            onClick={() => onDeleteExpense(expense.id)}
            className="ml-4 p-2 text-red-500 hover:text-red-700 hover:bg-red-50 dark:hover:bg-red-900/20 rounded-full transition-colors"
            title="Delete expense"
          >
            <Trash2 size={18} />
          </button>
        </div>
      ))}
    </div>
  );
}
