"use client";

import { useState, useEffect } from "react";
import { format } from "date-fns";
import {
  PlusCircle,
  DollarSign,
  TrendingUp,
  BarChart3,
  PieChart,
} from "lucide-react";
import {
  ExpenseForm,
  ExpenseList,
  DashboardCard,
  ExpenseChart,
  CategoryBreakdown,
} from "./index";
import { apiService, Expense } from "../services/api";

export type { Expense };

export default function ExpenseTracker() {
  const [expenses, setExpenses] = useState<Expense[]>([]);
  const [showForm, setShowForm] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Load expenses from API on component mount
  useEffect(() => {
    loadExpenses();
  }, []);

  const loadExpenses = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await apiService.getExpenses();
      setExpenses(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load expenses");
    } finally {
      setLoading(false);
    }
  };

  const addExpense = async (expense: Omit<Expense, "id">) => {
    try {
      const newExpense = await apiService.addExpense(expense);
      setExpenses([...expenses, newExpense]);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to add expense");
    }
  };

  const deleteExpense = async (id: string) => {
    try {
      await apiService.deleteExpense(id);
      setExpenses(expenses.filter((expense) => expense.id !== id));
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to delete expense");
    }
  };

  // Calculate total expenses
  const totalExpenses = expenses.reduce(
    (sum, expense) => sum + expense.amount,
    0
  );

  // Calculate expenses by category
  const expensesByCategory = expenses.reduce((acc, expense) => {
    acc[expense.category] = (acc[expense.category] || 0) + expense.amount;
    return acc;
  }, {} as Record<string, number>);

  // Find highest and lowest spending categories
  const categoryEntries = Object.entries(expensesByCategory);
  const highestCategory = categoryEntries.reduce(
    (max, [category, amount]) =>
      amount > max.amount ? { category, amount } : max,
    { category: "", amount: 0 }
  );

  const lowestCategory = categoryEntries.reduce(
    (min, [category, amount]) =>
      amount < min.amount ? { category, amount } : min,
    { category: "", amount: Infinity }
  );

  // Calculate monthly trend (last 6 months)
  const monthlyTrend = expenses.reduce((acc, expense) => {
    const monthYear = format(new Date(expense.date), "MMM yyyy");
    acc[monthYear] = (acc[monthYear] || 0) + expense.amount;
    return acc;
  }, {} as Record<string, number>);

  return (
    <div className="container mx-auto p-6 max-w-7xl">
      <div className="mb-8">
        <div className="flex items-center justify-between mb-6">
          <h1 className="text-4xl font-bold text-gray-900 dark:text-white">
            Expense Tracker
          </h1>
          <button
            onClick={() => setShowForm(!showForm)}
            className="inline-flex items-center gap-2 bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors"
          >
            <PlusCircle size={20} />
            Add Expense
          </button>
        </div>

        {error && (
          <div className="mb-4 p-4 bg-red-100 border border-red-300 text-red-700 rounded-lg">
            {error}
            <button
              onClick={() => {
                setError(null);
                loadExpenses();
              }}
              className="ml-2 underline hover:no-underline"
            >
              Retry
            </button>
          </div>
        )}

        {loading && (
          <div className="mb-4 p-4 bg-blue-100 border border-blue-300 text-blue-700 rounded-lg">
            Loading expenses...
          </div>
        )}

        {showForm && (
          <div className="mb-6">
            <ExpenseForm
              onAddExpense={addExpense}
              onCancel={() => setShowForm(false)}
            />
          </div>
        )}

        {/* Dashboard Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <DashboardCard
            title="Total Expenses"
            value={`$${totalExpenses.toFixed(2)}`}
            icon={<DollarSign size={24} />}
            color="bg-blue-500"
          />
          <DashboardCard
            title="Total Categories"
            value={Object.keys(expensesByCategory).length.toString()}
            icon={<PieChart size={24} />}
            color="bg-green-500"
          />
          <DashboardCard
            title="Highest Category"
            value={highestCategory.category || "N/A"}
            subValue={
              highestCategory.amount > 0
                ? `$${highestCategory.amount.toFixed(2)}`
                : ""
            }
            icon={<TrendingUp size={24} />}
            color="bg-red-500"
          />
          <DashboardCard
            title="Lowest Category"
            value={lowestCategory.category || "N/A"}
            subValue={
              lowestCategory.amount < Infinity
                ? `$${lowestCategory.amount.toFixed(2)}`
                : ""
            }
            icon={<BarChart3 size={24} />}
            color="bg-purple-500"
          />
        </div>

        {/* Charts Section */}
        {expenses.length > 0 && (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
            <div className="bg-white dark:bg-gray-800 rounded-lg p-6 shadow-md">
              <h2 className="text-xl font-semibold mb-4 text-gray-900 dark:text-white">
                Expense Trend
              </h2>
              <ExpenseChart monthlyTrend={monthlyTrend} />
            </div>
            <div className="bg-white dark:bg-gray-800 rounded-lg p-6 shadow-md">
              <h2 className="text-xl font-semibold mb-4 text-gray-900 dark:text-white">
                Category Breakdown
              </h2>
              <CategoryBreakdown expensesByCategory={expensesByCategory} />
            </div>
          </div>
        )}

        {/* Expenses List */}
        <div className="bg-white dark:bg-gray-800 rounded-lg p-6 shadow-md">
          <h2 className="text-xl font-semibold mb-4 text-gray-900 dark:text-white">
            Recent Expenses
          </h2>
          <ExpenseList expenses={expenses} onDeleteExpense={deleteExpense} />
        </div>
      </div>
    </div>
  );
}
