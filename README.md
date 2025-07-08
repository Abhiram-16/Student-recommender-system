# Student Recommender System 🎓

An intelligent course recommendation system that predicts the most suitable elective subjects for students based on their academic performance and interests.

---

## 🔍 Project Overview

This project uses machine learning and basic NLP to analyze a student's academic history and recommend electives for upcoming semesters. It supports:
- Semester 3-2 recommendations
- Semester 4-1 recommendations
- Course pools for personalized selection
- Optional interest-based input using NLP (extendable)

Built using **Flask**, **scikit-learn**, and **pandas**, the system provides a web interface for students to input their marks and get recommendations.

---

## 🚀 How It Works

- **Step 1**: Student logs in / registers
- **Step 2**: Enters subject marks (core subjects)
- **Step 3**: ML model predicts scores for elective subjects
- **Step 4**: Highest-scoring electives from each pool are recommended

Machine Learning Models:
- Trained on structured academic data
- Use `RandomForestRegressor` to predict subject performance

Optional (future scope):
- NLP model matches student's free-text interests with course descriptions

---

## 🛠️ Tech Stack

- 🧠 **Python 3.9**
- 🌐 **Flask**
- 📊 **pandas**, **scikit-learn**
- 🗃️ **SQLAlchemy** for user management
- 🧠 Optional: `sentence-transformers` for NLP-based interest analysis

---

## 📷 Screenshots

> _Add screenshots here of the web interface and prediction results_

---

## 📦 Project Structure

<pre> <code> ``` Student-recommender-system/ ├── app.py # Flask app ├── dataset.csv # Training data for sem 3-2 ├── New dataset.csv # Training data for sem 4-1 ├── modelfor3_2.pkl # Trained ML model (sem 3-2) ├── modelfor4_1.pkl # Trained ML model (sem 4-1) ├── templates/ # HTML pages ├── static/ # CSS and assets ├── venv/ # Virtual environment (excluded via .gitignore) └── requirements.txt # Python dependencies ``` </code> </pre>
