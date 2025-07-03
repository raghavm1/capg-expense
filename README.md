# Expense Tracker Application

A full-stack expense tracking application built with Flask (Python) backend and Next.js (TypeScript) frontend, featuring object-oriented design principles and professional code architecture.

## Approach and Design

### Architecture Overview

- **Backend**: Flask REST API with object-oriented expense management
- **Frontend**: Next.js with TypeScript, modern React components
- **Data Storage**: File-based JSON storage (ready for database migration)
- **Object-Oriented Design**: Category and Expense classes with proper encapsulation

### Key Design Principles

1. **Object-Oriented Programming**:

   - `Category` class for rich category management
   - `Expense` class with validation and business logic
   - `ExpenseTracker` class for expense operations

2. **Data Validation**:

   - Input validation for amounts, dates, and categories
   - Custom exceptions for better error handling
   - Type hints throughout for better code maintainability

3. **API Design**:

   - RESTful endpoints with consistent response formats
   - CORS enabled for frontend-backend communication
   - Backward-compatible API responses

4. **Frontend Architecture**:
   - Component-based React architecture
   - Custom hooks for API integration
   - Responsive design with Tailwind CSS
   - Interactive charts and data visualization

## Project Structure

```
capgemini/
├── cap-backend/               # Flask API Backend
│   ├── app.py                # Main Flask application
│   ├── expenses.py           # Core business logic (Category, Expense, ExpenseTracker)
│   ├── main.py              # Simple CLI demo
│   ├── test_expenses.py     # Test suite
│   ├── requirements.txt     # Python dependencies
│   ├── expenses.json        # Data storage file
│   └── dockerfile          # Docker configuration
│
└── cap-frontend/             # Next.js Frontend
    ├── src/
    │   ├── app/             # Next.js app router
    │   ├── components/      # React components
    │   │   ├── ExpenseTracker.tsx    # Main application component
    │   │   ├── ExpenseForm.tsx       # Add expense form
    │   │   ├── ExpenseList.tsx       # Expense list display
    │   │   ├── ExpenseChart.tsx      # Trend visualization
    │   │   ├── CategoryBreakdown.tsx # Category pie chart
    │   │   └── DashboardCard.tsx     # Stats cards
    │   └── services/
    │       └── api.ts       # API service layer
    ├── package.json         # Node.js dependencies
    └── next.config.ts       # Next.js configuration
```

### Key Files

#### Backend Core Files

- **`expenses.py`**: Contains all business logic classes:
  - `Category`: Object-oriented category management
  - `Expense`: Expense entity with validation
  - `ExpenseTracker`: Main business logic controller
- **`app.py`**: Flask REST API with endpoints for CRUD operations
- **`test_expenses.py`**: Comprehensive test suite

#### Frontend Core Files

- **`ExpenseTracker.tsx`**: Main application component with state management
- **`api.ts`**: API service layer for backend communication
- **`ExpenseForm.tsx`**: Form component with custom category support

## Getting Started

### Prerequisites

- Python 3.8+
- Node.js 18+
- npm or yarn

### Backend Setup

1. **Navigate to backend directory**:

   ```bash
   cd cap-backend
   ```

2. **Create virtual environment**:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Flask API**:
   ```bash
   python app.py
   ```
   Server runs on `http://localhost:5000`

### Frontend Setup

1. **Navigate to frontend directory**:

   ```bash
   cd cap-frontend
   ```

2. **Install dependencies**:

   ```bash
   npm install
   ```

3. **Set up environment variables**:

   ```bash
   cp .env.example .env.local
   # Edit .env.local if needed (API URL is set to localhost:5000 by default)
   ```

4. **Run the development server**:
   ```bash
   npm run dev
   ```
   Application runs on `http://localhost:3000`

## 🧪 Testing and Verification

2. **Test API endpoints**:

   ```bash
   # Health check
   curl http://localhost:5000/api/health

   # Get all expenses
   curl http://localhost:5000/api/expenses

   # Add an expense
   curl -X POST http://localhost:5000/api/expenses \
     -H "Content-Type: application/json" \
     -d '{"category": "Food", "amount": 25.50, "date": "2025-07-01", "description": "Lunch"}'
   ```

### Frontend Testing

1. **Access the application**: Navigate to `http://localhost:3000`
2. **Test core functionality**:
   - Add expenses using the form
   - Select custom categories using "Other" option
   - View expense list and statistics
   - Observe real-time chart updates

### Integration Testing

1. **Start both backend and frontend**
2. **Test full workflow**:

   - Add multiple expenses with different categories
   - Verify data persistence by refreshing the page
   - Check that charts update correctly
   - Test expense deletion

3. **Using the frontend**: Simply use the "Add Expense" form in the web interface

### Data Persistence

- Expenses are automatically saved to `cap-backend/expenses.json`
- Data persists between application restarts
- File is created automatically on first expense addition

## 🔧 API Endpoints

### Core Endpoints

- `GET /api/health` - Health check
- `GET /api/expenses` - Get all expenses
- `POST /api/expenses` - Add new expense
- `DELETE /api/expenses/{id}` - Delete expense
- `GET /api/statistics` - Get expense statistics
- `GET /api/expenses/category/{category}` - Get expenses by category
- `GET /api/categories` - Get category statistics (enhanced endpoint)

### Request/Response Examples

**Add Expense**:

```json
POST /api/expenses
{
  "category": "Food",
  "amount": 25.50,
  "date": "2025-07-01",
  "description": "Optional description"
}
```

**Response**:

```json
{
  "id": "2025-07-01_Food_25.5",
  "category": "Food",
  "amount": 25.5,
  "date": "2025-07-01",
  "description": "Optional description"
}
```

## Features

### Current Features

- Add, view, and delete expenses
- Category management with custom categories
- Real-time expense statistics
- Interactive charts and data visualization
- File-based data persistence
- Input validation and error handling
- Object-oriented backend architecture

### Architecture Benefits

- **Scalable**: Object-oriented design ready for database integration
- **Maintainable**: Clean separation of concerns
- **Extensible**: Easy to add new features (budgets, goals, categories metadata)
- **Professional**: Follows industry best practices and design patterns

## Future Enhancements

The object-oriented architecture enables easy extension:

- Category hierarchies and subcategories
- Budget tracking and alerts
- Multi-currency support
- Database integration (PostgreSQL/Neon)
- Advanced analytics and reporting

### Design Patterns

- Repository pattern (ExpenseTracker)
- Object-oriented encapsulation (Category, Expense)
- Service layer pattern (API service)
- Component composition (React components)
