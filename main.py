import re
from typing import List, Optional

import pandas as pd

from fastapi import FastAPI, Query, status
from fastapi.responses import JSONResponse

from utils import preprocess_names_with_codes
from recommendations_manager import obtain_recommendations, obtain_random_recommendations

api = FastAPI()

anime_names_codes = pd.read_csv("data/anime_data.csv")[["show_titles", "code"]].to_numpy().tolist()
#Split the concatenated anime names to get list of the names of an anime
names_lists = preprocess_names_with_codes(anime_names_codes)
 
@api.get("/api/v1/get_recommendations")
async def get_recommendations(anime_code: int = Query("")):    
    if anime_code:
        recommendations = obtain_recommendations(anime_code)
        return JSONResponse(content=recommendations, status_code=200)

    return JSONResponse(content={"Error": "The anime name is missing"}, status_code=400)

@api.get("/api/v1/get_random_recommendations")
async def get_random_recommendations(n: Optional[int] = Query(10, gt=0, le=20)):
    recommendations = obtain_random_recommendations(n)
    return JSONResponse(content=recommendations, status_code=200)

@api.get("/api/v1/get_names")
async def get_names():
    names = {"names": names_lists}
    return JSONResponse(content=names, status_code=200)
