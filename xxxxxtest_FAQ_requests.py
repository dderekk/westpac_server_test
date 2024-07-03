import requests
import time

url = 'http://192.168.56.1:5000/ask'  # IP address
question = {"question": "What is the interest rate for savings accounts?"}

def ask_question_with_retry(url, question, retries=3, delay=2):
    for attempt in range(retries):
        try:
            response = requests.post(url, json=question)
            response.raise_for_status()  # Raise an HTTPError for bad responses (4xx, 5xx)
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt < retries - 1:
                print(f"Retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                print("All attempts failed.")
                return None

response_data = ask_question_with_retry(url, question)
if response_data:
    print(response_data)
else:
    print("Failed to get a response from the server.")
