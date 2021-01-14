import re
from typing import List, Optional

import pandas as pd

from fastapi import FastAPI, Query, status
from fastapi.responses import JSONResponse

from utils import preprocess_anime_info
from recommendations_manager import (obtain_recommendations, obtain_random_recommendations, 
                                    get_single_anime_info, get_recommendation_weight)

api = FastAPI()

anime_data = pd.read_csv("data/anime_data.csv")[["show_titles", "code", "image_url", "type", "genres", "premiered"]].to_dict("records")
#Split the concatenated anime names to get list of the names of an anime
anime_data = preprocess_anime_info(anime_data)
 
@api.get("/api/v1/recommendations")
async def recommendations(anime_code: int = Query(""), n_recommendations: int = Query(5)):    
    if anime_code:
        recommendations = obtain_recommendations(anime_code, n_recommendations)
        return JSONResponse(content=recommendations, status_code=200)

    return JSONResponse(content={"Error": "The anime code is missing"}, status_code=400)

@api.get("/api/v1/random_recommendations")
async def random_recommendations(n: Optional[int] = Query(10, gt=0, le=20)):
    recommendations = obtain_random_recommendations(n)
    return JSONResponse(content=recommendations, status_code=200)

@api.get("/api/v1/search_info")
async def search_info():
    search_info = {"search_info": anime_data}
    return JSONResponse(content=search_info, status_code=200)

@api.get("/api/v1/anime")
async def anime(anime_code: int = Query(0)):
    anime_info = get_single_anime_info(anime_code)
    return JSONResponse(content=anime_info, status_code=200)

@api.get("/api/v1/user_recommendations")
async def user_recommendations(search_anime: int = Query(0), recommended_anime: int = Query(0)):
    recommendation_weight = get_recommendation_weight(search_anime, recommended_anime)
    return JSONResponse(content=recommendation_weight, status_code=200)