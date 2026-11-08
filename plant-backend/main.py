from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import requests
import json
import os
from pathlib import Path


def load_env_file():
    # Load KEY=VALUE pairs from plant-backend/.env (kept out of git)
    env_path = Path(__file__).parent / ".env"
    if env_path.exists():
        for line in env_path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, value = line.split("=", 1)
                os.environ.setdefault(key.strip(), value.strip())


load_env_file()

# TLS verification is on by default. It can be turned off only for local
# development behind a filtering proxy, by setting SSL_VERIFY=false in .env.
SSL_VERIFY = os.environ.get("SSL_VERIFY", "true").lower() != "false"
if not SSL_VERIFY:
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_rapidapi_headers():
    return {
        'x-rapidapi-host': "house-plants2.p.rapidapi.com",
        'x-rapidapi-key': os.environ.get("RAPIDAPI_KEY", "")
    }

def convert_objects_to_json(obj):

    if isinstance(obj, dict):
        converted = {}
        for key, value in obj.items():
            if isinstance(value, dict):
                converted[key] = json.dumps(value)
            else:
                converted[key] = value
        return converted
    return obj


@app.get("/plants/", status_code=status.HTTP_200_OK)
def get_all_plants():
    try:
        response = requests.get(
            "https://house-plants2.p.rapidapi.com/all-lite",
            headers=get_rapidapi_headers(),
            verify=SSL_VERIFY,
        )

        if response.status_code == 404:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Plants endpoint not found"
            )

        plants = response.json()
        
        if not plants:
            return JSONResponse(
                status_code=status.HTTP_204_NO_CONTENT,
                content={"message": "No plants found"}
            )
        
        simplified_plants = []
        for plant in plants:
            simplified_plants.append({
                "id": plant.get("id"),
                "Latin name": plant.get("Latin name"),
                "Family": plant.get("Family"),
                "Categories": plant.get("Categories")
            })
        
        return simplified_plants
        
   
    except requests.exceptions.ConnectionError:
       raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Unable to connect to plant database"
        )
    except requests.exceptions.RequestException as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )
    

@app.get("/plants/{plant_id}", status_code=status.HTTP_200_OK)
def get_plant_detail(plant_id: str):
    
    if not plant_id or plant_id.strip() == "":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Plant ID cannot be empty"
        )
    
    try:
        response = requests.get(
            f"https://house-plants2.p.rapidapi.com/id/{plant_id}",
            headers=get_rapidapi_headers(),
            verify=SSL_VERIFY,
        )
        
        if response.status_code == 404:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Plant with ID {plant_id} not found"
            )
        
        plant = response.json()
        
        if not plant:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No data found for plant ID {plant_id}"
            )
        
        converted_plant = convert_objects_to_json(plant)
        
        return converted_plant
        
    except requests.exceptions.ConnectionError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Unable to connect to plant database"
        )
    
    except requests.exceptions.RequestException as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)