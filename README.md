# Pokemon API

This project is a FastAPI-based Pokemon API that allows users to fetch and search for Pokemon data.

## Getting Started

Follow these steps to set up and run the project on your local machine.

### Prerequisites

- Python 3.7+
- PostgreSQL

### Installation

1. Clone the repository:
   git clone https://github.com/your-username/pokemon-api.git
   cd pokemon-api
2. Create a virtual environment:
   python -m venv venv
3. Activate the virtual environment:
- On Windows:
  ```
  venv\Scripts\activate
  ```
- On macOS and Linux:
  ```
  source venv/bin/activate
  ```

4. Install the required packages:
   pip install -r requirements.txt
5. Create a PostgreSQL database named `pokemon_db`:
   psql -U postgres
   CREATE DATABASE pokemon_db;
   \q
6. Update the `.env` file with your database credentials:
  DB_USER=your_username
  DB_PASSWORD=your_password
  DB_HOST=localhost
  DB_PORT=5432
  DB_NAME=pokemon_db
7. Run Alembic migrations to create the necessary tables:
  alembic revision --autogenerate -m "Create Pokemon table"
  alembic upgrade head

### Running the Application

1. Start the FastAPI server:
   uvicorn app.main:app --reload
2. Open your web browser and navigate to `http://localhost:8000` to access the Pokemon API UI.

## Usage

- Use the web interface to search for Pokemon by name or type.
- Click "Show Pokemon" to fetch and display Pokemon data.
- Adjust the number of Pokemon to fetch (1-100) using the input field.

## API Endpoints

- GET `/api/v1/pokemons`: Fetch all Pokemon (with optional limit parameter)
- GET `/api/v1/pokemons/search`: Search Pokemon by name and/or type
