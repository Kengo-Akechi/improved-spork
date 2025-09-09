# 🍷 Napa Valley Premium Wines – Smart Conversational Agent

AI-powered conversational agent for Napa Valley Premium Wines, built with **FastAPI**, **React**, and **LangGraph**.


## 🚀 Quick Start

### Prerequisites

* Python **3.11+**
* Node.js **18+**
* MongoDB (local or cloud)
* Emergent LLM API key

---

### Installation

1. **Clone the repository**

```bash
git clone https://github.com/yourusername/napa-wine-agent.git
cd napa-wine-agent
```

2. **Backend Setup**

```bash
cd backend
pip install -r requirements.txt
```

3. **Frontend Setup**

```bash
cd ../frontend
yarn install
```

4. **Configure Environment**

**Backend `.env`**

```env
MONGO_URL="mongodb://localhost:27017"
DB_NAME="wine_agent_db"
CORS_ORIGINS="*"
EMERGENT_LLM_KEY=sk-your-emergent-key
OPENWEATHER_API_KEY=your_openweather_key
```

**Frontend `.env`**

```env
REACT_APP_BACKEND_URL=http://localhost:8001
```

---

### Running the Application

**Development Mode**

```bash
# Terminal 1: Start backend
cd backend
uvicorn server:app --host 0.0.0.0 --port 8001 --reload

# Terminal 2: Start frontend
cd frontend
yarn start
```

**Production Mode (Supervisor recommended)**

```bash
sudo supervisorctl restart all
sudo supervisorctl status
```

---

Would you like me to make this **extra minimal** (just install + run commands), or keep this version with `.env` setup included?
