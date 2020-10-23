import re
from typing import List
from fastapi import FastAPI, Query, status
from fastapi.responses import JSONResponse
import pandas as pd
from recommendations_manager import obtain_recommendations

api = FastAPI()

anime_names = pd.read_csv("data/anime_data.csv")["name"].tolist()

@api.get("/api/v1/get_recommendations")
async def main(user_name: str = Query(None), anime_name: str = Query([])):
    if anime_name:
        recommendations = obtain_recommendations(
            anime_name)
        return JSONResponse(content=recommendations, status_code=200)

    return JSONResponse(content={"missing": "parameters"}, status_code=400)

@api.get("/api/v1/get_names")
async def get_names():    
    names = {"names": [re.sub(r"\s\s*", " ", re.sub(r"[\-\_]", " ", name)) for name in anime_names]}
    return names
