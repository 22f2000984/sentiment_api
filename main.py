from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Enable CORS
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

    positive = ["love", "great", "excellent", "happy", "amazing", "good"]
    negative = ["terrible", "bad", "sad", "hate", "awful", "worst"]

    if any(word in text for word in positive):
        return "happy"
    if any(word in text for word in negative):
        return "sad"
    return "neutral"

@app.post("/sentiment", response_model=SentimentResponse)
def sentiment_analysis(request: SentimentRequest):
    return {
        "results": [
            {
                "sentence": s,
                "sentiment": analyze_sentiment(s)
            }
            for s in request.sentences
        ]
    }

import os

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))