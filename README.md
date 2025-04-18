# Sudoku AI Solver Project

## Project Description
This is a Sudoku game where the puzzle can be generated, solved using AI, and visualized step-by-step. All the code for both the backend and frontend is in the `backend` folder as I mistakenly didn't push the frontend separately.

## Project Structure
The entire project is located inside the `backend` folder and contains:
- **app.py**: The main Flask application (Backend)
- **requirements.txt**: Python dependencies for the backend
- **static/**: Contains CSS and JavaScript files for the frontend
- **templates/**: Contains HTML templates used by Flask

There is **no separate frontend folder** because I didn't push it as intended. The frontend files (HTML, CSS, JavaScript) are located inside the `backend` folder.

## Installation and Setup

### 1. Clone the Repository
To clone the repository to your local machine:

```bash
git clone <repo-url>
cd <repo-directory>/backend

2. Create and Activate  Virtual Environemnt
python -m venv venv
venv\Scripts\activate
    or (or just Activate)
venv\Scripts\activate

3. Install Python Dependencies
pip install -r requirements.txt

4. Run the Flask Application
python app.py 
    or
flask run
5. Open the App in Browser
http://localhost:5000