import re
from typing import List
from fastapi import FastAPI, Query, status
from fastapi.responses import JSONResponse
import pandas as pd
from recommendations_manager import obtain_recommendations

api = FastAPI()

animes_df = pd.read_csv("data/anime_codes.csv")

@api.get("/api/v1/get_recommendations")
async def main(user_name: str = Query(None), anime_names: List[str] = Query([])):
    if anime_names and anime_names[0].strip():
        recommendations = obtain_recommendations(
            anime_names)
        return JSONResponse(content=recommendations, status_code=200)

    return JSONResponse(content={"missing": "parameters"}, status_code=400)

@api.get("/api/v1/get_names")
async def get_names():    
    names = {"names":animes_df["name"].apply(lambda x: re.sub(r"\s\s*", " ", re.sub(r"[\-\_]", " ", x))).tolist()}
    return names
