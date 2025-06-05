# 🚀 Lead Generator Tool

The **Lead Generator Tool** is an intelligent lead enrichment web app that enhances raw lead CSVs using a **local machine learning model** and smart scraping techniques — no external APIs required.

---

## 🧠 What It Does

- ✅ Predicts email deliverability using a trained ML model  
- ✅ Detects company tech stack using headless scraping (Selenium + BeautifulSoup)  
- ✅ Estimates LinkedIn engagement from company profiles  
- ✅ Allows download of enriched leads with a single click

---

## 🗂 Project Structure

```
lead-generator-ml/
├── app.py                    # Flask backend
├── lead_generator_tool.py    # Main enrichment logic (ML + scraping)
├── ml_model.py               # Email deliverability ML logic
├── train_model.py             # Script to train and export email_model.pkl
├── templates/
│   └── index.html            # Frontend UI
├── static/
│   └── style.css             # Styling for UI
├── models/
│   └── email_model.pkl       # Trained ML model (logistic regression)
├── requirements.txt          # Python dependencies
├── .gitignore                # Git exclusions
└── README.md                 # You're reading it!
```

---

## ⚙️ Setup Instructions

### 1. 🔧 Install Python Dependencies

```bash
pip install -r requirements.txt
```

Or manually:

```bash
pip install flask selenium beautifulsoup4 requests scikit-learn numpy webdriver-manager
```

> **Make sure you have Google Chrome installed.**

---

### 2. 🧠 Train ML Model (Optional)

If `email_model.pkl` doesn't exist, run:

```bash
python train_model.py
```

This will train a logistic regression model on sample email data.

---

### 3. 🚀 Run the App

```bash
python app.py
```

Then visit:  
http://localhost:5000

---

## 💡 Features

- Upload CSV of company domains  
- Auto-detect tech stack via headless scraping  
- Predict email deliverability using ML (no API)  
- Estimate LinkedIn reach using followers  
- Outputs: `Email Used`, `ML Deliverability`, `Tech Stack`, `Engagement Score`  
- One-click CSV download  

---

## 🔒 Notes

- LinkedIn scraping may occasionally fail or be throttled  
- Tech stack detection depends on page HTML structure  
- ML model uses simple email pattern features (dot structure, length, etc.)


---

## 🧑‍💻 Built With

- Python 3  
- Flask  
- BeautifulSoup  
- Selenium + ChromeDriver  
- scikit-learn (Logistic Regression)

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

**Built by [@swordboom](https://github.com/swordboom)**
