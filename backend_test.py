import requests
import sys
import json
from datetime import datetime

class WineAPITester:
    def __init__(self, base_url="https://wine-smart-guide.preview.emergentagent.com/api"):
        self.base_url = base_url
        self.tests_run = 0
        self.tests_passed = 0
        self.failed_tests = []

    def run_test(self, name, method, endpoint, expected_status, data=None, timeout=30):
        """Run a single API test"""
        url = f"{self.base_url}/{endpoint}" if endpoint else self.base_url
        headers = {'Content-Type': 'application/json'}

        self.tests_run += 1
        print(f"\n🔍 Testing {name}...")
        print(f"   URL: {url}")
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers, timeout=timeout)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=headers, timeout=timeout)

            print(f"   Status Code: {response.status_code}")
            
            success = response.status_code == expected_status
            if success:
                self.tests_passed += 1
                print(f"✅ Passed - Status: {response.status_code}")
                try:
                    response_data = response.json()
                    print(f"   Response preview: {str(response_data)[:200]}...")
                    return True, response_data
                except:
                    return True, response.text
            else:
                print(f"❌ Failed - Expected {expected_status}, got {response.status_code}")
                print(f"   Response: {response.text[:300]}...")
                self.failed_tests.append({
                    'name': name,
                    'expected': expected_status,
                    'actual': response.status_code,
                    'response': response.text[:500]
                })
                return False, {}

        except requests.exceptions.Timeout:
            print(f"❌ Failed - Request timed out after {timeout} seconds")
            self.failed_tests.append({
                'name': name,
                'error': f'Timeout after {timeout} seconds'
            })
            return False, {}
        except Exception as e:
            print(f"❌ Failed - Error: {str(e)}")
            self.failed_tests.append({
                'name': name,
                'error': str(e)
            })
            return False, {}

    def test_root_endpoint(self):
        """Test the root API endpoint"""
        return self.run_test("Root API Endpoint", "GET", "", 200)

    def test_weather_endpoint(self):
        """Test weather endpoint"""
        return self.run_test("Weather Endpoint", "GET", "wine/weather", 200)

    def test_conversation_history(self):
        """Test conversation history endpoint"""
        return self.run_test("Conversation History", "GET", "conversations", 200)

    def test_wine_question_basic(self):
        """Test basic wine question"""
        data = {"question": "What wines do you offer?"}
        return self.run_test("Basic Wine Question", "POST", "wine/ask", 200, data, timeout=45)

    def test_wine_question_weather(self):
        """Test weather-related question"""
        data = {"question": "What's the weather like today?"}
        return self.run_test("Weather Question", "POST", "wine/ask", 200, data, timeout=45)

    def test_wine_question_search(self):
        """Test search-related question"""
        data = {"question": "Search for wine pairing with salmon"}
        return self.run_test("Search Question", "POST", "wine/ask", 200, data, timeout=45)

    def test_wine_question_general(self):
        """Test general conversational question"""
        data = {"question": "Tell me about your Cabernet Sauvignon"}
        return self.run_test("General Wine Question", "POST", "wine/ask", 200, data, timeout=45)

    def test_empty_question(self):
        """Test empty question handling"""
        data = {"question": ""}
        return self.run_test("Empty Question", "POST", "wine/ask", 422, data)

    def test_invalid_endpoint(self):
        """Test invalid endpoint"""
        return self.run_test("Invalid Endpoint", "GET", "invalid/endpoint", 404)

def main():
    print("🍷 Starting Napa Valley Premium Wines API Testing...")
    print("=" * 60)
    
    tester = WineAPITester()
    
    # Test all endpoints
    print("\n📡 Testing API Endpoints...")
    tester.test_root_endpoint()
    tester.test_weather_endpoint()
    tester.test_conversation_history()
    
    print("\n🤖 Testing LLM Integration...")
    tester.test_wine_question_basic()
    tester.test_wine_question_weather()
    tester.test_wine_question_search()
    tester.test_wine_question_general()
    
    print("\n🔍 Testing Error Handling...")
    tester.test_empty_question()
    tester.test_invalid_endpoint()
    
    # Print final results
    print("\n" + "=" * 60)
    print(f"📊 FINAL RESULTS:")
    print(f"   Tests Run: {tester.tests_run}")
    print(f"   Tests Passed: {tester.tests_passed}")
    print(f"   Tests Failed: {len(tester.failed_tests)}")
    print(f"   Success Rate: {(tester.tests_passed/tester.tests_run)*100:.1f}%")
    
    if tester.failed_tests:
        print(f"\n❌ FAILED TESTS:")
        for i, test in enumerate(tester.failed_tests, 1):
            print(f"   {i}. {test['name']}")
            if 'expected' in test:
                print(f"      Expected: {test['expected']}, Got: {test['actual']}")
                print(f"      Response: {test['response']}")
            else:
                print(f"      Error: {test['error']}")
    
    return 0 if tester.tests_passed == tester.tests_run else 1

if __name__ == "__main__":
    sys.exit(main())