from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# ✅ CORS FIX
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # 👈 IMPORTANT
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

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
            return {"reply": "Please type a message."}

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": f"You are a portfolio assistant. Context:\n{PORTFOLIO_CONTEXT}"
                },
                {
                    "role": "user",
                    "content": message
                }
            ]
        )

        return {"reply": response.choices[0].message.content}

    except Exception as e:
        print("Groq error:", e)
        return {"reply": "Sorry, something went wrong with the backend."}

