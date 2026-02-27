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

def analyze_sentiment(text: str) -> str:
    text = text.lower()

    # Tokenize words
    words = re.findall(r"\b\w+\b", text)

    positive_words = {
        "love","great","excellent","happy","amazing","good",
        "fantastic","awesome","wonderful","brilliant",
        "best","excited","nice","super","perfect",
        "liked","like","enjoy","enjoyed","positive",
        "delight","delighted","pleased","glad","satisfied",
        "incredible","outstanding","fabulous","marvelous",
        "fun","beautiful","cool","success","successful"
    }

    negative_words = {
        "terrible","bad","sad","hate","awful","worst",
        "horrible","disappointed","angry","upset",
        "poor","boring","annoying","negative",
        "problem","issue","dislike","frustrated",
        "depressed","unhappy","pathetic","useless",
        "lame","dreadful","regret","complaint",
        "fail","failed","failure","ruined","mess"
    }

    pos_score = 0
    neg_score = 0

    for i, word in enumerate(words):
        # Handle negation like "not good"
        if word == "not" and i + 1 < len(words):
            next_word = words[i + 1]
            if next_word in positive_words:
                neg_score += 1
            elif next_word in negative_words:
                pos_score += 1
            continue

        if word in positive_words:
            pos_score += 1
        elif word in negative_words:
            neg_score += 1

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