
# FastAPI Todos Project

## Overview

This project is a web application built using [FastAPI](https://fastapi.tiangolo.com/), a modern, fast (high-performance) web framework for building APIs with Python 3.7+ based on standard Python type hints.

## Features

- **High Performance**: FastAPI is one of the fastest Python frameworks available.
- **Easy to Use**: Designed to be easy to use and learn, making it a good choice for both new and experienced developers.
- **Dependency Injection**: FastAPI supports dependency injection, allowing you to write modular and testable code.
- **Automatic Documentation**: FastAPI automatically generates interactive API documentation using Swagger UI and ReDoc.

## Installation

### Prerequisites

- Python 3.7+
- `pip` (Python package installer)

### Clone the Repository

```bash
git clone https://github.com/pmondal100/todos-fastapi.git
cd todos-fastapi
```

### Setup

Install the required packages by running:

```bash
python3 -m venv todos_env
source todos_env/bin/activate
pip install -r requirements.txt
```

## Starting the Server

### Development

To start the server in development mode with auto-reload:

```bash
cd ..
uvicorn Todos.main:app --reload
```

### Production

To start the server in production mode:

```bash
cd ..
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

## Running Test Cases

To run the test cases with verbose output:

```bash
pytest -vv
```

## Miscellaneous

- **Running Test Cases**: Run the test cases from inside the project folder.
- **Running the Server/Application**: To start the server, navigate to the parent folder (one level up from the project folder).