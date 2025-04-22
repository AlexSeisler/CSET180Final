# 🛍️ Multi-Vendor E-Commerce Store (Flask + MySQL)

A full-stack e-commerce platform where multiple vendors can list products and manage orders, built with Flask (Python) and MySQL Workbench (local storage).  

---

## ⚙️ Project Tech Stack

- **Backend**: Flask
- **Database**: MySQL Workbench (local)
- **Frontend**: HTML, CSS, JavaScript
- **Version Control**: Git + GitHub

---

## 🗃️ Project Structure


---

## 🧠 Git Branching Strategy

| Branch        | Purpose                             |
|---------------|--------------------------------------|
| `main`        | Production-ready code ONLY           |
| `dev`         | All features merged here and tested  |
| `feature/*`   | Active development work              |

### 👥 Example Team Branches

| Developer     | Branch Name              | Task Focus                         |
|---------------|--------------------------|-------------------------------------|
| Alex           | `feature/backend-core`   | Routes, DB logic, product mgmt     |
| Teammate A    | `feature/frontend-ui`    | Templates, UI/UX design            |
| Teammate B    | `feature/auth-system`    | Login, registration, session logic |

---

## 🔁 Daily Workflow Guide

### 💻 Setup (one-time)

```bash
# Clone the repo (only starting out)
git clone https://github.com/<your-username>/multi-vendor-store.git
cd multi-vendor-store

# Install packages (optional for team)
pip install -r requirements.txt


# Push base to main
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/<your-username>/multi-vendor-store.git
git push -u origin main

# Create dev branch
git checkout -b dev
git push -u origin dev


# 1. Sync latest changes
git checkout dev
git pull origin dev

# 2. Create or switch to your feature branch
git checkout -b feature/<your-feature>  # if new
git checkout feature/<your-feature>     # if exists

# 3. Do your work...

# 4. Stage & commit
git add .
git commit -m "Add: your meaningful message"

# 5. Push to your branch
git push origin feature/<your-feature>

---

## ✅ Best Practices

### ✅ DOs
- ✅ Commit often with **clear, meaningful messages**
- ✅ Always start your work from the `dev` branch — **never `main`**
- ✅ Use a `.env` file for storing local credentials and **add it to `.gitignore`**
- ✅ **Pull from `dev`** every day before starting your work to stay updated

### ❌ DON'Ts
- ❌ Never push directly to `main` or `dev` branches
- ❌ Don’t commit sensitive files like `.env`, **passwords**, or **OS/system files**
