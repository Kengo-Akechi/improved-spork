from fastapi import FastAPI, APIRouter, HTTPException
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field
from typing import List, Optional
import uuid
from datetime import datetime
import requests
import asyncio
from emergentintegrations.llm.chat import LlmChat, UserMessage

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app without a prefix
app = FastAPI()

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Wine Business Knowledge Base
WINE_BUSINESS_CONTENT = """
Welcome to Napa Valley Premium Wines - Your Gateway to Excellence

About Our Winery:
Founded in 1985, Napa Valley Premium Wines is a family-owned boutique winery located in the heart of Napa Valley, California. We specialize in crafting exceptional Cabernet Sauvignon, Chardonnay, and Pinot Noir wines using sustainable farming practices and traditional winemaking techniques.

Our Wine Collection:
1. Cabernet Sauvignon Reserve 2020 - $85
   - Rich, full-bodied with notes of dark cherry, cassis, and oak
   - Aged 18 months in French oak barrels
   - Perfect with red meats and aged cheeses

2. Estate Chardonnay 2022 - $45
   - Crisp and elegant with citrus and green apple flavors
   - Partial malolactic fermentation adds complexity
   - Excellent with seafood and poultry

3. Pinot Noir Signature 2021 - $65
   - Light to medium-bodied with cherry and earthy notes
   - 14 months in neutral oak
   - Pairs beautifully with salmon and mushroom dishes

4. Rosé Spring Blend 2023 - $32
   - Fresh and vibrant with strawberry and peach notes
   - Perfect for summer occasions and light appetizers

Vineyard Tours & Tastings:
- Daily tours: 10 AM, 1 PM, 4 PM
- Tasting flights: $25 (includes 4 wines)
- Private group tastings available by appointment
- Seasonal wine pairing dinners

Contact Information:
- Address: 1234 Vineyard Lane, Napa, CA 94558
- Phone: (707) 555-WINE
- Email: info@napavalleypremium.com
- Website: www.napavalleypremium.com

Special Events:
- Harvest Festival: September 15-17, 2024
- Wine Club member exclusive events quarterly
- Wedding and private event venue available

Our Philosophy:
We believe in creating wines that reflect the unique terroir of Napa Valley while maintaining respect for the environment through sustainable practices including solar power, water conservation, and organic farming methods.
"""

# Define Models
class WineQuery(BaseModel):
    question: str
    
class WineResponse(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    question: str
    response: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class ConversationHistory(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    session_id: str
    question: str
    response: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

# Weather function
def get_napa_weather():
    """Get current weather for Napa Valley, California"""
    try:
        api_key = os.environ.get('OPENWEATHER_API_KEY', 'demo_key')
        if api_key == 'demo_key' or api_key == 'YOUR_API_KEY_HERE':
            return "Weather service is currently unavailable. Please set up OpenWeatherMap API key for real weather data. Demo: Napa Valley is currently 72°F with partly cloudy skies, perfect for vineyard visits!"
        
        url = f"http://api.openweathermap.org/data/2.5/weather?q=Napa,CA,US&appid={api_key}&units=imperial"
        response = requests.get(url, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            temp = data['main']['temp']
            description = data['weather'][0]['description']
            humidity = data['main']['humidity']
            return f"Current weather in Napa Valley: {temp}°F, {description}, humidity {humidity}%. Perfect conditions for wine tasting!"
        else:
            return "Weather service temporarily unavailable. Please try again later."
    except Exception as e:
        return f"Weather service error: {str(e)}"

# Web search function  
def web_search(query: str):
    """Perform a simple web search - placeholder for demonstration"""
    # In a real implementation, you'd use a search API like SerpAPI, Bing, or Google Custom Search
    return f"Web search results for '{query}': This feature would integrate with a web search API to provide real-time information. For demonstration purposes, this shows where search results would appear."

# Conversational Agent using LangGraph concepts
class WineConversationalAgent:
    def __init__(self):
        self.api_key = os.environ.get('EMERGENT_LLM_KEY', '')
        
    async def process_query(self, question: str, session_id: str = None) -> str:
        """Process user query using LLM with context awareness"""
        try:
            if not session_id:
                session_id = str(uuid.uuid4())
                
            # Initialize LLM chat
            chat = LlmChat(
                api_key=self.api_key,
                session_id=session_id,
                system_message=f"""You are a knowledgeable wine business assistant for Napa Valley Premium Wines. 

Your knowledge base includes:
{WINE_BUSINESS_CONTENT}

You can also:
1. Answer questions about our wine business using the knowledge base above
2. Get current weather for Napa Valley when asked
3. Perform web searches for additional information when needed

Guidelines:
- Be friendly, professional, and knowledgeable about wine
- Use the wine business content to answer specific questions about our winery
- When asked about weather, call the weather function
- When asked to search for information not in your knowledge base, use web search
- Always stay in character as a Napa Valley wine business representative
- If unsure about wine business details not in the knowledge base, be honest and offer to search for more information
"""
            ).with_model("openai", "gpt-4o-mini")
            
            # Check if query is about weather
            if any(word in question.lower() for word in ['weather', 'temperature', 'climate', 'forecast']):
                weather_info = get_napa_weather()
                enhanced_question = f"{question}\n\nCurrent weather information: {weather_info}"
                user_message = UserMessage(text=enhanced_question)
            
            # Check if query requires web search
            elif any(word in question.lower() for word in ['search', 'find', 'look up', 'research']):
                search_results = web_search(question)
                enhanced_question = f"{question}\n\nWeb search information: {search_results}"
                user_message = UserMessage(text=enhanced_question)
            
            else:
                user_message = UserMessage(text=question)
            
            # Get response from LLM
            response = await chat.send_message(user_message)
            return response
            
        except Exception as e:
            logging.error(f"Error in conversational agent: {str(e)}")
            return f"I'm sorry, I encountered an error processing your question. Please try again. Error: {str(e)}"

# Initialize the agent
wine_agent = WineConversationalAgent()

# API Routes
@api_router.get("/")
async def root():
    return {"message": "Napa Valley Premium Wines - Smart Wine Assistant API"}

@api_router.post("/wine/ask", response_model=WineResponse)
async def ask_wine_question(query: WineQuery):
    """Ask a question to the wine business conversational agent"""
    try:
        # Validate question is not empty
        if not query.question or not query.question.strip():
            raise HTTPException(status_code=422, detail="Question cannot be empty")
            
        session_id = str(uuid.uuid4())
        response_text = await wine_agent.process_query(query.question, session_id)
        
        # Create response object
        wine_response = WineResponse(
            question=query.question,
            response=response_text
        )
        
        # Store in database
        conversation = ConversationHistory(
            session_id=session_id,
            question=query.question,
            response=response_text
        )
        await db.conversations.insert_one(conversation.dict())
        
        return wine_response
        
    except Exception as e:
        logging.error(f"Error processing wine question: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing question: {str(e)}")

@api_router.get("/wine/weather")
async def get_weather():
    """Get current weather for Napa Valley"""
    weather_info = get_napa_weather()
    return {"weather": weather_info}

@api_router.get("/wine/search/{query}")
async def search_web(query: str):
    """Perform web search"""
    search_results = web_search(query)
    return {"query": query, "results": search_results}

@api_router.get("/conversations", response_model=List[ConversationHistory])
async def get_conversation_history():
    """Get recent conversation history"""
    conversations = await db.conversations.find().sort("timestamp", -1).limit(20).to_list(20)
    return [ConversationHistory(**conv) for conv in conversations]

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()