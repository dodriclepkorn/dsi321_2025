
# DSI321_2025: News Scraper & Word Cloud for Alternative Construction

## 📌 Project Description

This "News Scraper & Word Cloud for Alternative Construction" project is developed as part of the DSI321 (Data Science and Innovation) / Big Data Infrastructure course for the academic year 2025 at Thammasat University.

It aims to collect news articles related to **alternative construction** using web scraping, clean and process the text data, and generate **Word Clouds** to visually represent key terms and emerging trends in the sector.

---

## ✨ Key Features

- **Automated Web Scraping** from online news websites or blogs.
- **Text Filtering & Cleaning** for relevance and clarity.
- **Text Preprocessing** using NLP techniques (tokenization, stop word removal).
- **Dynamic Word Cloud Generation** based on word frequency.
- **Interactive Streamlit Dashboard** to visualize results.
- **Customization Options** (if implemented) for keywords and sources.
- **Data Refresh Capability** to fetch the latest news.

---

## 🛠 Technologies Used

- **Python**
- **Requests & BeautifulSoup4** – for scraping
- **NLTK** – for text preprocessing
- **WordCloud** – for word cloud generation
- **Pandas** – for data handling
- **Streamlit** – for dashboard UI
- **Jupyter Notebooks** – for prototyping
- **Docker & Docker Compose**
- **Git & GitHub**

---

## 📁 Repository Structure

```
myproject/
├── news_data/
│   └── news_data.csv
├── data/
├── metadata/
├── myehv/
├── app.py
├── create_wordcloud.py
├── main.py
├── main_2.py
├── main_main.py
├── config_path.py
├── Dockerfile.cli
├── Dockerfile.streamlit
├── docker-compose.yml
├── requirements.txt
├── start.sh
├── .gitignore
├── pyproject.toml
└── README.md
```

---

## ⚙️ Installation and Running

### ✅ Prerequisites

- **Git**: https://git-scm.com/
- **Python 3.8+**: https://www.python.org/downloads/
- **Docker & Docker Compose** (Recommended): https://www.docker.com/products/docker-desktop/

### 📥 Clone the Repository

```bash
git clone https://github.com/dodriclepkorn/dsi321_2025.git
cd dsi321_2025
```

### 🚀 Run with Docker Compose (Recommended)

```bash
docker-compose up --build
```

### ⚠️ Manual Setup (Optional)

```bash
python -m venv venv
source venv/bin/activate  # Or .\venv\Scripts\activate on Windows
pip install -r requirements.txt
```

---

## 🧪 Usage

Once the app is running, open:

- `http://localhost:8501` (local)
- `http://<your-ip>:8501` (network)

Use the dashboard to:
- Scrape new data
- View word clouds
- Customize scraping options (if enabled)

---

## 🤝 Contributing

1. Fork the repo: https://github.com/dodriclepkorn/dsi321_2025
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Commit your changes and push
4. Open a Pull Request with a detailed description

---

## 👩‍💻 Author

Kanokporn Samathathanyakorn 6524651152 
GitHub: [dodriclepkorn](https://github.com/dodriclepkorn)

---
