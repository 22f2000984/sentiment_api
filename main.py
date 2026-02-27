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

import re

import re

def analyze_sentiment(text: str) -> str:
    text = text.lower()
    words = re.findall(r"\b\w+\b", text)

    positive_words = {
        "love","great","excellent","happy","amazing","good",
        "fantastic","awesome","wonderful","brilliant",
        "best","excited","nice","super","perfect",
        "liked","like","enjoy","enjoyed","positive",
        "delight","delighted","pleased","glad","satisfied",
        "incredible","outstanding","fabulous","marvelous",
        "fun","beautiful","cool","success","successful",
        "smile","joy","joyful","win","winning","improve",
        "improved","improvement","well","better"
    }

    negative_words = {
        "terrible","bad","sad","hate","awful","worst",
        "horrible","disappointed","angry","upset",
        "poor","boring","annoying","negative",
        "problem","issue","dislike","frustrated",
        "depressed","unhappy","pathetic","useless",
        "lame","dreadful","regret","complaint",
        "fail","failed","failure","ruined","mess",
        "cry","pain","painful","worse","loss","lost"
    }

    # Base scoring
    pos_score = sum(1 for w in words if w in positive_words)
    neg_score = sum(1 for w in words if w in negative_words)

    # Strong emotional intensifiers
    if any(w in text for w in ["very","extremely","really","absolutely","so","too"]):
        if pos_score > 0:
            pos_score += 1
        if neg_score > 0:
            neg_score += 1

    # Negation handling
    for i in range(len(words)-1):
        if words[i] == "not":
            if words[i+1] in positive_words:
                neg_score += 1
            elif words[i+1] in negative_words:
                pos_score += 1

    # Fallback heuristic: exclamation often positive unless negative word exists
    if "!" in text and pos_score == 0 and neg_score == 0:
        return "happy"

    if pos_score > neg_score:
        return "happy"
    elif neg_score > pos_score:
        return "sad"
    else:
        return "neutral"
@app.post("/", response_model=SentimentResponse)
def sentiment_analysis(request: SentimentRequest):
    return {
        "results": [
            {"sentence": s, "sentiment": analyze_sentiment(s)}
            for s in request.sentences
        ]
    }