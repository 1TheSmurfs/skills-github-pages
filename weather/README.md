# Weather Dashboard

A full-stack weather dashboard application built with FastAPI and HTMX, featuring real-time weather updates and interactive visualizations.

## Features

- Current weather information display
- Short-term and extended forecasts
- Interactive visualizations (temperature trends, precipitation chances)
- Location search functionality
- Responsive design for mobile and desktop use

## Tech Stack

- Backend: FastAPI
- Frontend: HTMX, Tailwind CSS
- Data Visualization: Plotly
- Weather Data: OpenWeatherMap API
- Testing: Pytest
- Type Checking: Mypy
- Code Formatting: Black, Ruff

## Setup and Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd weather-dashboard
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root and add your OpenWeatherMap API key:
```
OPENWEATHERMAP_API_KEY=your_api_key_here
```

5. Run the development server:
```bash
uvicorn app.main:app --reload
```

The application will be available at `http://localhost:8000`

## Project Structure

```
weather-dashboard/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── api/
│   ├── core/
│   ├── models/
│   ├── services/
│   └── templates/
├── tests/
├── static/
├── docs/
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

## Development

- Run tests: `pytest`
- Type checking: `mypy .`
- Format code: `black . && ruff check --fix .`

## Documentation

Detailed documentation is available at our [GitHub Pages site](https://your-username.github.io/weather-dashboard/).

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 