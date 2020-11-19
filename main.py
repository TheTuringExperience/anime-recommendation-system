import re
from typing import List, Optional
from fastapi import FastAPI, Query, status
from fastapi.responses import JSONResponse
import pandas as pd
from recommendations_manager import obtain_recommendations, obtain_random_recommendations

api = FastAPI()

anime_names = pd.read_csv("data/anime_data.csv")["name"].tolist()

@api.get("/api/v1/get_recommendations")
async def get_recommendations(anime_name: str = Query("")):
    if anime_name.strip():
        recommendations = obtain_recommendations(
            anime_name)
        return JSONResponse(content=recommendations, status_code=200)

    return JSONResponse(content={"Error": "The anime name is missing"}, status_code=400)

@api.get("/api/v1/get_random_recommendations")
async def get_random_recommendations(n: Optional[int] = Query(10, gt=0, le=20)):
    recommendations = obtain_random_recommendations(n)
    return JSONResponse(content=recommendations, status_code=200)

@api.get("/api/v1/get_names")
async def get_names():    
    names = {"names": [re.sub(r"\s\s*", " ", re.sub(r"[\-\_]", " ", name)) for name in anime_names]}
    return names
