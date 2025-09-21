# 🚘 AutoInsight — AI-Powered Vehicle Analysis & Risk Assessment  

<p align="center">
  <img src="https://img.shields.io/badge/API-FastAPI-009688?logo=fastapi" alt="FastAPI"/>
  <img src="https://img.shields.io/badge/Frontend-Streamlit-FF4B4B?logo=streamlit" alt="Streamlit"/>
  <img src="https://img.shields.io/badge/Deploy-Docker-2496ED?logo=docker" alt="Docker"/>
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?logo=python" alt="Python"/>
  <img src="https://img.shields.io/badge/Tests-Pytest%20%2B%20Playwright-6DB33F?logo=pytest" alt="Tests"/>
</p>

---

## 📖 Overview  

**AutoInsight** is a **full-stack AI-powered platform** that blends:  
- ⚡ **FastAPI** for a robust backend  
- 🎨 **Streamlit** for an interactive frontend  
- 🤖 **LLM intelligence** for smart vehicle insights  

With just a **VIN number**, AutoInsight generates:  
- 📋 **Detailed vehicle summaries**  
- 🛡️ **Risk assessment reports**  
- 💡 **Data-driven insights** for buyers, sellers, and the automotive community  

This helps users **make smarter, more informed decisions** when analyzing or purchasing vehicles.  

---

## 📂 Project Structure

```plaintext
├── app/                     # Backend (FastAPI service)
│   ├── llm.py               # LLM integration with OpenAI
│   ├── main.py              # FastAPI entrypoint
│   ├── models.py            # Pydantic models (request/response)
│   ├── prompts.py           # LLM system & user prompts
│   ├── utils.py             # CSV loading & fallback deterministic summary
│   └── __init__.py
│
├── data/
│   └── sample_data.csv      # Vehicle dataset (VINs, pricing, mileage, etc.)
│
├── GUI/
│   └── graphical_user_interface.py   # Streamlit app (frontend)
│
├── tests/                   # Automated test suite
│   ├── test_api.py          # API tests (pytest + FastAPI TestClient)
│   └── test_ui.py           # UI tests (pytest + Playwright)
│
├── docker-compose.yml       # Orchestration of backend + frontend
├── Dockerfile               # Backend container (FastAPI)
├── Dockerfile.GUI           # Frontend container (Streamlit)
├── requirements.txt         # Python dependencies
├── .env                     # Environment variables (create your own for security)
└── README.md                # Project documentation
```

---

## ⚙️ Features

* **Backend (FastAPI)**

  * `/` → Health check
  * `/vin-summary` → Accepts VIN, looks up dataset, and returns:

    * Human-readable vehicle summary
    * Risk score (1.0–10.0)
    * Step-by-step reasoning
  * Uses **OpenAI LLMs** if API key available, otherwise falls back to **deterministic scoring**

* **Frontend (Streamlit)**

  * Modern, responsive UI for VIN lookups
  * Instant vehicle summary + risk score
  * Expandable reasoning section
  * Buyer, seller, and community benefit cards

* **LLM Integration**

  * Powered by **OpenAI Responses API**
  * Custom prompts ensure structured JSON outputs
  * Automatic fallback to rule-based scoring if LLM unavailable

* **Testing**

  * **API tests** with `pytest`
  * **UI tests** with `Playwright` (end-to-end flow)

* **Deployment**

  * Fully **Dockerized** with `docker-compose`
  * `backend` → FastAPI (port **8000**)
  * `frontend` → Streamlit (port **8501**)

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/amazMajid2003/autoinsight.git
cd autoinsight
```

### 2. Setup Environment

Create a `.env` file at the project root:

```env
OPENAI_API_KEY=your_openai_api_key   # Optional, enables LLM mode
OPENAI_MODEL=gpt-5-mini              # Default model
VIN_API_URL=http://localhost:8000/vin-summary
```

### 3. Install Dependencies (Local Development)

```bash
pip install -r requirements.txt
```

### 4. Run Backend (FastAPI)

```bash
uvicorn app.main:app --reload --port 8000
```

➡ Backend available at → [http://localhost:8000/docs](http://localhost:8000/docs)

### 5. Run Frontend (Streamlit)

```bash
streamlit run GUI/graphical_user_interface.py
```

➡ Frontend available at → [http://localhost:8501](http://localhost:8501)

---

## 🐳 Dockerized Deployment

Run both backend & frontend with one command:

```bash
docker-compose up --build
```

* FastAPI backend → [http://localhost:8000](http://localhost:8000)
* Streamlit frontend → [http://localhost:8501](http://localhost:8501)

---

## 🧪 Testing

### Run API Tests

```bash
pytest tests/test_api.py -v
```

### Run UI Tests (Playwright)

Ensure backend & frontend are running (`http://localhost:8000` & `http://localhost:8501`):

```bash
pytest tests/test_ui.py -v
```

---

## 📊 Example API Call

**Request**

```bash
curl -X POST "http://localhost:8000/vin-summary" \
     -H "Content-Type: application/json" \
     -d '{"vin": "JTDBCMFE8T3112879"}'
```

**Response**

```json
{
  "vin": "JTDBCMFE8T3112879",
  "summary": "2019 TOYOTA COROLLA with 42,000 miles, competitively priced...",
  "risk_score": 4.3,
  "reasoning": [
    "Days on lot: 35 → moderate risk",
    "Price near market value → neutral",
    "Low mileage → reduces risk"
  ],
  "source": "llm"
}
```

---

## 🛠 Tech Stack

* **Backend**: FastAPI, Pydantic, Pandas
* **Frontend**: Streamlit
* **LLM**: OpenAI Responses API
* **Testing**: pytest, Playwright
* **Deployment**: Docker, docker-compose

---

## 🤝 Contributing  

We welcome contributions from the community! 🚀  

If you'd like to help improve **AutoInsight**, please follow these steps:  

1. **Fork** the repository  
2. **Create** a new feature branch (`git checkout -b feature/your-feature`)  
3. **Commit** your changes (`git commit -m "Add new feature"`)  
4. **Push** to your branch (`git push origin feature/your-feature`)  
5. **Submit** a Pull Request 🎉  

---

## 👤 Author  

<p align="start">
  <b>Muhammad Amaz Majid</b><br/>
  <i>Computer Scientist | AI & Full-Stack Developer</i><br/><br/>
  
  <a href="https://github.com/amazMajid2003">
    <img src="https://img.shields.io/badge/GitHub-amazMajid2003-181717?logo=github" alt="GitHub"/>
  </a>
  <a href="https://www.linkedin.com/in/muhammad-amaz-majid-6715272ab">
    <img src="https://img.shields.io/badge/LinkedIn-Connect-blue?logo=linkedin" alt="LinkedIn"/>
  </a>
</p>


