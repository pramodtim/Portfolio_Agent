# main.py
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Allow your frontend URL to access backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://pramodtim.netlify.app/"],  # Replace * with your frontend URL in production
    allow_methods=["*"],
    allow_headers=["*"]
)

# Initialize Groq client with API key
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Portfolio context
PORTFOLIO_CONTEXT = """
I am an MSc Business Analytics student in London.
I work with data analytics, forecasting, Tableau dashboards,
and business reporting.

Projects:
- Sales forecasting using Prophet
- Manufacturing cost forecasting using ARIMA
- Credit card default prediction using logistic regression
"""

@app.get("/")
def read_root():
    return {"status": "Backend is running"}

@app.post("/chat")
async def chat_endpoint(request: Request):
    try:
        data = await request.json()
        message = data.get("message")
        if not message:
            return {"error": "No message provided"}

        # System message with your portfolio context
        system_message = {
            "role": "system",
            "content": f"You are a helpful assistant. Context about the user:\n{PORTFOLIO_CONTEXT}"
        }

        # User message
        user_message = {"role": "user", "content": message}

        # Call Groq API
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",  # Use the model you have access to
            messages=[system_message, user_message]
        )

        reply = response.choices[0].message.content
        return {"reply": reply}

    except Exception as e:
        print("Error calling Groq API:", e)
        return {"reply": "Sorry, something went wrong with the backend."}


