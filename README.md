# 🍷 Napa Valley Premium Wines – Smart Conversational Agent

A smart AI-powered conversational agent providing wine knowledge, real-time weather, and web search for Napa Valley Premium Wines.


## 🚀 Quick Setup & Run

### Prerequisites

* Python 3.11+
* Node.js 18+
* MongoDB (local or cloud)
* Emergent LLM API key

---

### Installation

```bash
git clone https://github.com/yourusername/napa-wine-agent.git
cd napa-wine-agent
```

**Backend**

```bash
cd backend
pip install -r requirements.txt
```

**Frontend**

```bash
cd ../frontend
yarn install
```

**Environment Variables**

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
# Terminal 1: Backend
cd backend
uvicorn server:app --host 0.0.0.0 --port 8001 --reload

# Terminal 2: Frontend
cd frontend
yarn start
```

**Production Mode (Supervisor recommended)**

```bash
sudo supervisorctl restart all
sudo supervisorctl status
```

---

## 📋 API Usage

**Ask a Wine Question**

```http
POST /api/wine/ask
Content-Type: application/json

{
  "question": "What wines do you offer?"
}
```

**Get Weather**

```http
GET /api/wine/weather
```

**Get Conversation History**

```http
GET /api/conversations
```

---

## 🔧 Testing

**Backend**

```bash
cd backend
python -m pytest tests/ -v
```

**Frontend**

```bash
cd frontend
yarn test
```


