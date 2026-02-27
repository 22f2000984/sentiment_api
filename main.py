from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

app = FastAPI()

# 🔥 THIS FIXES "Failed to fetch"
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SentimentRequest(BaseModel):
    sentences: List[str]

class SentimentResult(BaseModel):
    sentence: str
    sentiment: str

class SentimentResponse(BaseModel):
    results: List[SentimentResult]

def analyze_sentiment(text: str) -> str:
    text = text.lower()

    positive_words = [
        "love","great","excellent","happy","amazing","good",
        "fantastic","awesome","wonderful","brilliant",
        "best","excited","nice","super","perfect",
        "liked","like","enjoy","enjoyed","positive"
    ]

    negative_words = [
        "terrible","bad","sad","hate","awful","worst",
        "horrible","disappointed","angry","upset",
        "poor","boring","annoying","negative",
        "problem","issue","dislike"
    ]

    if any(word in text for word in positive_words):
        return "happy"
    if any(word in text for word in negative_words):
        return "sad"
    return "neutral"

@app.post("/sentiment", response_model=SentimentResponse)
def sentiment_analysis(request: SentimentRequest):
    return {
        "results": [
            {"sentence": s, "sentiment": analyze_sentiment(s)}
            for s in request.sentences
        ]
    }