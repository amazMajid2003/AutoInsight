from fastapi import FastAPI, HTTPException
from app.models import VINRequest, VINResponse
from app.utils import load_csv, deterministic_summary
from app.llm import generate_vin_summary
from dotenv import load_dotenv
import os

# Load environment variables (e.g., OpenAI API key) from .env file
load_dotenv()

# Initialize FastAPI application
app = FastAPI(title="VIN Summary Service", version="1.0.0")

# Load CSV data once when app starts, so it's available globally
CSV_PATH = os.path.join("data", "sample_data.csv")
df = load_csv(CSV_PATH)


@app.get("/")
def root():
    """
    Health check endpoint.

    This route is used to confirm that the VIN Summary Service is up and running.
    It returns a simple JSON message when accessed.
    """
    return {"message": "VIN Summary Service is running!"}


@app.post("/vin-summary", response_model=VINResponse)
def get_vin_summary(request: VINRequest):
    """
    VIN summary endpoint.

    This endpoint accepts a VIN (Vehicle Identification Number) via POST request.
    Steps:
    1. Normalize the VIN input (trim + convert to uppercase).
    2. Look up the VIN in the loaded CSV dataset.
    3. If the VIN is not found, return a 404 error.
    4. If found:
       - Use LLM to generate a detailed summary if an OpenAI API key is available.
       - Otherwise, fall back to a deterministic, rule-based summary.

    Returns:
        VINResponse: Object containing the vehicle summary.
    """

    # Normalize VIN input
    vin = request.vin.strip().upper()

    # Check if VIN exists in the dataset
    row = df[df["VIN"].str.upper() == vin]
    if row.empty:
        raise HTTPException(status_code=404, detail="VIN not found in dataset")

    # Extract vehicle data as dictionary
    vehicle_data = row.iloc[0].to_dict()

    # Choose summary method based on presence of OpenAI API key
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        # LLM-based summary
        return generate_vin_summary(vehicle_data)
    else:
        # Deterministic (rule-based) summary
        return deterministic_summary(vehicle_data)
