import React, { useState, useEffect } from "react";
import "./App.css";
import { Button } from "./components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "./components/ui/card";
import { Input } from "./components/ui/input";
import { Textarea } from "./components/ui/textarea";
import { Badge } from "./components/ui/badge";
import { Grape, MessageCircle, Cloud, Search, Wine, MapPin, Phone, Mail } from "lucide-react";
import axios from "axios";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

function App() {
  const [question, setQuestion] = useState("");
  const [response, setResponse] = useState("");
  const [loading, setLoading] = useState(false);
  const [weather, setWeather] = useState("");
  const [conversations, setConversations] = useState([]);

  // Fetch weather on component mount
  useEffect(() => {
    fetchWeather();
    fetchConversations();
  }, []);

  const fetchWeather = async () => {
    try {
      const res = await axios.get(`${API}/wine/weather`);
      setWeather(res.data.weather);
    } catch (error) {
      console.error("Error fetching weather:", error);
      setWeather("Weather service unavailable");
    }
  };

  const fetchConversations = async () => {
    try {
      const res = await axios.get(`${API}/conversations`);
      setConversations(res.data.slice(0, 5)); // Show only last 5
    } catch (error) {
      console.error("Error fetching conversations:", error);
    }
  };

  const handleAskQuestion = async (e) => {
    e.preventDefault();
    if (!question.trim()) return;

    setLoading(true);
    try {
      const res = await axios.post(`${API}/wine/ask`, {
        question: question.trim()
      });
      setResponse(res.data.response);
      setQuestion("");
      fetchConversations(); // Refresh conversation history
    } catch (error) {
      console.error("Error asking question:", error);
      setResponse("Sorry, I encountered an error processing your question. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const handleExampleQuestion = (exampleQ) => {
    setQuestion(exampleQ);
  };

  const exampleQuestions = [
    "What wines do you offer?",
    "What's the weather like today?",
    "Tell me about your Cabernet Sauvignon",
    "What are your tasting hours?",
    "Search for wine pairing with salmon"
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-amber-50 via-orange-50 to-red-50">
      {/* Header */}
      <div className="bg-gradient-to-r from-red-900 via-red-800 to-red-900 text-white shadow-lg">
        <div className="max-w-6xl mx-auto px-6 py-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className="bg-white/20 p-3 rounded-full">
                <Grape className="w-8 h-8" />
              </div>
              <div>
                <h1 className="text-3xl font-bold">Napa Valley Premium Wines</h1>
                <p className="text-red-100">Smart Wine Assistant</p>
              </div>
            </div>
            <div className="flex items-center space-x-4 text-sm">
              <div className="flex items-center space-x-1">
                <MapPin className="w-4 h-4" />
                <span>Napa, CA</span>
              </div>
              <div className="flex items-center space-x-1">
                <Phone className="w-4 h-4" />
                <span>(707) 555-WINE</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-6xl mx-auto px-6 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          
          {/* Main Chat Interface */}
          <div className="lg:col-span-2">
            <Card className="bg-white/80 backdrop-blur-sm border-amber-200 shadow-xl">
              <CardHeader className="bg-gradient-to-r from-amber-600 to-orange-600 text-white rounded-t-lg">
                <CardTitle className="flex items-center space-x-2">
                  <MessageCircle className="w-6 h-6" />
                  <span>Ask Our Wine Expert</span>
                </CardTitle>
                <CardDescription className="text-amber-100">
                  Get answers about our wines, weather updates, and more!
                </CardDescription>
              </CardHeader>
              <CardContent className="p-6 space-y-6">
                
                {/* Question Form */}
                <form onSubmit={handleAskQuestion} className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Your Question
                    </label>
                    <Input
                      type="text"
                      value={question}
                      onChange={(e) => setQuestion(e.target.value)}
                      placeholder="Ask me anything about our wines, weather, or wine-related topics..."
                      className="w-full border-amber-300 focus:border-amber-500 focus:ring-amber-500"
                      disabled={loading}
                    />
                  </div>
                  <Button 
                    type="submit" 
                    disabled={loading || !question.trim()}
                    className="w-full bg-gradient-to-r from-red-700 to-red-800 hover:from-red-800 hover:to-red-900 text-white font-semibold py-3"
                  >
                    {loading ? "Thinking..." : "Ask Question"}
                  </Button>
                </form>

                {/* Example Questions */}
                <div>
                  <h3 className="text-lg font-semibold text-gray-800 mb-3">Try these examples:</h3>
                  <div className="flex flex-wrap gap-2">
                    {exampleQuestions.map((q, index) => (
                      <Badge 
                        key={index}
                        variant="outline"
                        className="cursor-pointer hover:bg-amber-100 border-amber-300 text-amber-800 px-3 py-1"
                        onClick={() => handleExampleQuestion(q)}
                      >
                        {q}
                      </Badge>
                    ))}
                  </div>
                </div>

                {/* Response */}
                {response && (
                  <div className="border-t pt-6">
                    <h3 className="text-lg font-semibold text-gray-800 mb-3 flex items-center space-x-2">
                      <Wine className="w-5 h-5 text-red-600" />
                      <span>Wine Expert Response:</span>
                    </h3>
                    <div className="bg-gradient-to-r from-amber-50 to-orange-50 p-4 rounded-lg border border-amber-200">
                      <Textarea
                        value={response}
                        readOnly
                        className="w-full border-none bg-transparent resize-none text-gray-800"
                        rows={8}
                      />
                    </div>
                  </div>
                )}
              </CardContent>
            </Card>
          </div>

          {/* Sidebar */}
          <div className="space-y-6">
            
            {/* Weather Card */}
            <Card className="bg-white/80 backdrop-blur-sm border-blue-200 shadow-lg">
              <CardHeader className="bg-gradient-to-r from-blue-600 to-cyan-600 text-white rounded-t-lg">
                <CardTitle className="flex items-center space-x-2">
                  <Cloud className="w-5 h-5" />
                  <span>Today's Weather</span>
                </CardTitle>
              </CardHeader>
              <CardContent className="p-4">
                <p className="text-gray-700">{weather || "Loading weather..."}</p>
              </CardContent>
            </Card>

            {/* Wine Info Card */}
            <Card className="bg-white/80 backdrop-blur-sm border-purple-200 shadow-lg">
              <CardHeader className="bg-gradient-to-r from-purple-600 to-pink-600 text-white rounded-t-lg">
                <CardTitle className="flex items-center space-x-2">
                  <Grape className="w-5 h-5" />
                  <span>Featured Wines</span>
                </CardTitle>
              </CardHeader>
              <CardContent className="p-4 space-y-3">
                <div className="space-y-2">
                  <h4 className="font-semibold text-gray-800">Cabernet Sauvignon Reserve</h4>
                  <p className="text-sm text-gray-600">Rich, full-bodied - $85</p>
                </div>
                <div className="space-y-2">
                  <h4 className="font-semibold text-gray-800">Estate Chardonnay</h4>
                  <p className="text-sm text-gray-600">Crisp and elegant - $45</p>
                </div>
                <div className="space-y-2">
                  <h4 className="font-semibold text-gray-800">Pinot Noir Signature</h4>
                  <p className="text-sm text-gray-600">Light and earthy - $65</p>
                </div>
              </CardContent>
            </Card>

            {/* Recent Conversations */}
            {conversations.length > 0 && (
              <Card className="bg-white/80 backdrop-blur-sm border-green-200 shadow-lg">
                <CardHeader className="bg-gradient-to-r from-green-600 to-teal-600 text-white rounded-t-lg">
                  <CardTitle className="flex items-center space-x-2">
                    <Search className="w-5 h-5" />
                    <span>Recent Questions</span>
                  </CardTitle>
                </CardHeader>
                <CardContent className="p-4">
                  <div className="space-y-2">
                    {conversations.map((conv, index) => (
                      <div key={index} className="text-sm border-b border-gray-200 pb-2">
                        <p className="text-gray-800 font-medium truncate">{conv.question}</p>
                        <p className="text-gray-500 text-xs">
                          {new Date(conv.timestamp).toLocaleTimeString()}
                        </p>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            )}

            {/* Contact Info */}
            <Card className="bg-white/80 backdrop-blur-sm border-gray-200 shadow-lg">
              <CardHeader className="bg-gradient-to-r from-gray-700 to-gray-800 text-white rounded-t-lg">
                <CardTitle className="flex items-center space-x-2">
                  <Mail className="w-5 h-5" />
                  <span>Visit Us</span>
                </CardTitle>
              </CardHeader>
              <CardContent className="p-4 space-y-2 text-sm">
                <p className="flex items-center space-x-2">
                  <MapPin className="w-4 h-4 text-gray-600" />
                  <span>1234 Vineyard Lane, Napa, CA</span>
                </p>
                <p className="flex items-center space-x-2">
                  <Phone className="w-4 h-4 text-gray-600" />
                  <span>(707) 555-WINE</span>
                </p>
                <p>Tours: 10 AM, 1 PM, 4 PM daily</p>
                <p>Tastings: $25 per flight</p>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;