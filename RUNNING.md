# Running and Deploying Forecasta

This guide provides step-by-step instructions on how to run the Forecasta project locally and how to safely upload it to GitHub.

## 🚀 How to Run the Project

### 1. Prerequisites
Ensure you have the following installed:
- **Python 3.11+**
- **Node.js (LTS)** and **npm**

---

### 2. Back-End Setup (FastAPI)
The back-end handles the data processing and forecasting logic.

1. **Navigate to the backend directory:**
   ```bash
   cd backend
   ```
2. **Create a virtual environment (Recommended):**
   ```bash
   python -m venv venv
   # Activate on Windows:
   venv\Scripts\activate
   # Activate on macOS/Linux:
   source venv/bin/activate
   ```
3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Start the server:**
   ```bash
   python -m uvicorn app.main:app --app-dir app --port 5000 --host 0.0.0.0
   ```
   *The API will be available at `http://127.0.0.1:5000`.*

---

### 3. Front-End Setup (Next.js)
The front-end provides the user interface for uploading data and visualizing forecasts.

1. **Navigate to the frontend directory:**
   ```bash
   cd ../frontend
   ```
2. **Install dependencies:**
   ```bash
   npm install
   ```
3. **Start the development server:**
   ```bash
   npm run dev
   ```
   *The dashboard will be available at `http://localhost:3000`.*

---

## 📤 How to Upload to GitHub Safely

To upload your project to GitHub without leaking sensitive data or bloating the repository with unnecessary files, follow these steps:

### 1. Verify `.gitignore`
Ensure the `.gitignore` file is present in the root directory. This prevents `node_modules`, `__pycache__`, `.env` files, and local databases (`.db`) from being uploaded.

### 2. Initialize Git and Commit
Run these commands from the root directory:
```bash
# Initialize the repository
git init

# Add all files to the staging area
git add .

# Commit the changes
git commit -m "Initial commit: Forecasta sales and demand forecasting platform"
```

### 3. Create a Repository on GitHub
1. Go to [github.com/new](https://github.com/new).
2. Create a new repository with the name `forecasta`.
3. **Do not** initialize the repository with a README, .gitignore, or License (since we already have them locally).

### 4. Push to GitHub
Replace `your-username` with your actual GitHub username:
```bash
# Link the local repo to the remote GitHub repo
git remote add origin https://github.com/your-username/forecasta.git

# Rename the current branch to main
git branch -M main

# Push the code to GitHub
git push -u origin main
```

## ✅ Final Checklist
- [ ] Back-end is running on port 5000.
- [ ] Front-end is running on port 3000.
- [ ] No sensitive keys are hardcoded in the source code.
- [ ] `.gitignore` is verified.
