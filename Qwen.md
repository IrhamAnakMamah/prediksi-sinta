# 🎓 SINTA Cluster Predictor & Simulator

## 📖 Project Overview

This repository contains a collection of **Streamlit-based simulation tools** designed to help universities predict and simulate SINTA (Science and Technology Index) scores. The primary goal is to assist institutions in developing ranking strategies, especially to analyze gaps in points needed to achieve the **Independent Cluster (Cluster Mandiri)** position.

The project consists of multiple modules that simulate different aspects of SINTA evaluation criteria, allowing users to manipulate input variables to see the impact on total normalized scores.

## 🏗️ Architecture & Files

### Main Application
- `main.py`: Centralized dashboard that integrates all modules and calculates the final total score prediction

### Module Files
- `publikasi.py`: Publication score calculation based on scientific publication productivity
- `research.py`: Research performance calculation based on faculty research activities  
- `abdimas.py`: Community service performance calculation
- `hki.py`: Intellectual Property Rights (HKI) output calculation
- `kelembagaan.py`: Institutional performance calculation
- `sdm.py`: Human Resources (SDM) qualification-based scoring

### Supporting Elements
- `README.md`: Comprehensive documentation with installation and usage instructions
- `__pycache__/`: Python bytecode cache files
- `.venv/`: Virtual environment directory

## 🌟 Features

### 1. 📚 Publication Simulation (`publikasi.py`)
- Calculates raw and normalized scores based on academic publication metrics
- Indicators: International journal articles (Q1-Q4, Non-Q), National journals (S1-S6), Proceedings, Citations, Books
- Normalizer: `1776.69`

### 2. 🔬 Research Simulation (`research.py`)
- Calculates research performance scores for faculty members
- Indicators: Foreign grants, External grants, Internal grants, Total research funding (Rupiah)
- Normalizer: `261,491.37`

### 3. 💡 HKI Simulation (`hki.py`)
- Calculates Intellectual Property Rights output scores
- Indicators: Patent, Simple Patent, Copyright, Industrial Design, Plant Variety Protection, etc.
- Normalizer: `14.7`

### 4. 🏛️ Institutional Simulation (`kelembagaan.py`)
- Calculates institutional performance scores
- Indicators: Program accreditation (Excellent/Good), Number of accredited journals
- Applies adjustment factor (30%) before normalization
- Normalizer: `2181.33`

### 5. 🤝 Community Service Simulation (`abdimas.py`)
- Calculates community service performance scores
- Indicators: International, National, Local services, Funding amount (Million Rupiah)
- Normalizer: `447,937.99`

### 6. 👥 Human Resources Simulation (`sdm.py`)
- Calculates scores based on Human Resources qualifications
- Indicators: Journal reviewers (International/National) and faculty functional positions (Professors to non-functional lecturers)
- Normalizer: `2.443`

### 7. 🏆 Main Dashboard (`main.py`)
- Central navigation that combines all modules for final score prediction
- Status: Under construction (fixing integration errors)
- Features: Sidebar navigation and Independent Cluster pass percentage calculation

## ⚙️ Technical Stack

- **Python 3.8+**: Primary programming language
- **Streamlit**: Interactive web dashboard framework
- **Pandas**: Data manipulation and calculation
- **Plotly Express**: Interactive visualization (Pie Charts)

## 🧩 Project Dependencies

Based on the code analysis, the project requires:

- `streamlit`
- `pandas`
- `plotly`
- `python` (version 3.8 or higher recommended)

## 🚀 Setup Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/username-anda/prediksi-cluster-sinta.git
   cd prediksi-cluster-sinta
   ```

2. Install required libraries:
   ```bash
   pip install streamlit pandas plotly
   ```

3. Run the application modules:
   ```bash
   # For community service simulation
   streamlit run abdimas.py
   
   # For HR simulation
   streamlit run sdm.py
   
   # For other modules, replace with respective filenames
   ```

## 📊 Scoring System

The final score calculation follows these weight distributions:
- Publication (25%)
- Research (15%) 
- Community Service (15%)
- Intellectual Property (10%)
- Human Resources (15%)
- Institutional (15%)

The system applies normalization factors and adjustment percentages according to SINTA evaluation standards.

## 🛣️ Development Roadmap

- ✅ Publication Simulation
- ✅ Research Simulation
- ✅ HKI Simulation
- ✅ Institutional Simulation
- ✅ Community Service Simulation
- ✅ Human Resources Simulation
- ❌ Stabilize Main Dashboard: Fix cross-page state integration bugs
- ❌ Independent Cluster Percentage Prediction: Finalize threshold score logic

## 🔄 Data Persistence Mechanism

The main application implements a custom data persistence system using `st.session_state["SINTA_DB"]` to maintain form data across different Streamlit page navigations, ensuring user inputs are preserved when switching between modules.