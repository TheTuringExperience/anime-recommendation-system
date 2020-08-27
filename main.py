from fastapi import FastAPI, Query, status
from typing import List
from recommendations_manager import obtain_recommendations

api = FastAPI()

@api.get("/api/v1/get_recommendations")
async def main(user_name: str = Query(None), anime_names: List[str] = Query([])):
    if anime_names:
        recommendations = obtain_recommendations(anime_names)
        return recommendations

    return {"missing": "parameters"}
