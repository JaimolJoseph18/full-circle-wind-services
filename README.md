# FastAPI Project

This project is a FastAPI application. This guide will help you set up and run it locally.

---

## Prerequisites

- Python 3.9.13 installed ([Download Python](https://www.python.org/downloads/))
- `pip` (comes with Python)
- (Optional) `venv` for virtual environments
- create a virtual environment
  python -m venv venv
- Activate the virtual environment
  .\venv\Scripts\Activate.ps1
- Install dependencies
  pip install --upgrade pip
  pip install -r requirements.txt
- Start the monitering engine
  uvicorn backend.monitering_engine.main:app --reload --port 8001
- Start the api
  uvicorn backend.api.main:app --reload --port 8000

# React+Typescript Project

This project is a React application. This guide will help you set up and run it locally.

---

## Prerequisites

- Make sure node.js is installed
  node -v
  npm -v
- navigate to react app folder
  cd FullCircleWindServices\frontend\data-monitering-ui
- Install all packages
  npm install
- Start the Vite development server
  npm run dev
- Local: http://localhost:5173/
