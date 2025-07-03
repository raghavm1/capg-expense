const API_BASE_URL = 'http://localhost:5000/api';

export interface Expense {
  id: string;
  amount: number;
  category: string;
  date: string;
  description?: string;
}

export interface Statistics {
  total_expense: number;
  total_by_category: Record<string, number>;
  expense_trend: Record<string, number>;
  highest_category: string | null;
  lowest_category: string | null;
}

class ApiService {
  private async fetchApi(endpoint: string, options: RequestInit = {}) {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.error || 'API request failed');
    }

    return response.json();
  }

  async getExpenses(): Promise<Expense[]> {
    return this.fetchApi('/expenses');
  }

  async addExpense(expense: Omit<Expense, 'id'>): Promise<Expense> {
    return this.fetchApi('/expenses', {
      method: 'POST',
      body: JSON.stringify(expense),
    });
  }

  async deleteExpense(id: string): Promise<void> {
    return this.fetchApi(`/expenses/${id}`, {
      method: 'DELETE',
    });
  }

  async getStatistics(): Promise<Statistics> {
    return this.fetchApi('/statistics');
  }

  async getExpensesByCategory(category: string): Promise<Expense[]> {
    return this.fetchApi(`/expenses/category/${category}`);
  }

  async healthCheck(): Promise<{ status: string; message: string }> {
    return this.fetchApi('/health');
  }
}

export const apiService = new ApiService();
