import random
import pytest
from fastapi.testclient import TestClient
from app.main import app, df

client = TestClient(app)

# Ensure CSV has enough VINs
if len(df) < 5:
    raise ValueError("CSV must contain at least 5 VINs for this test!")

# Pick 5 random VINs
sample_vins = random.sample(list(df["VIN"]), 5)


# Test root endpoint
def test_root():
    """
       Test the root endpoint ("/") for service health.

       Expects:
       - HTTP 200 OK
       - JSON response with message confirming service is running
       """
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "VIN Summary Service is running!"}


# Test /vin-summary endpoint with 5 random VINs
@pytest.mark.parametrize("vin", sample_vins)
def test_vin_summary_multiple(vin):
    """
        Test the /vin-summary endpoint for multiple random VINs from the CSV.

        Steps:
        1. POST VIN to /vin-summary
        2. Verify HTTP 200 response
        3. Check that response contains vin, summary, risk_score, reasoning, and source
        4. Print LLM output for manual verification

        Args:
        - vin (str): VIN from the CSV
        """
    response = client.post("/vin-summary", json={"vin": vin})
    assert response.status_code == 200
    data = response.json()

    # Assertions
    assert data["vin"].upper() == vin.upper()
    assert "summary" in data
    assert "risk_score" in data
    assert isinstance(data["reasoning"], list)

    # Print LLM output for verification
    print("\n--- LLM VIN Summary Output ---")
    print(f"VIN: {data['vin']}")
    print(f"Summary: {data['summary']}")
    print(f"Risk Score: {data['risk_score']}")
    print("Reasoning:")
    for r in data["reasoning"]:
        print(f"- {r}")
    print("-----------------------------\n")


# Test /vin-summary endpoint with an invalid VIN
def test_vin_summary_invalid():
    """
        Test the /vin-summary endpoint with an invalid VIN.

        Expects:
        - HTTP 404 Not Found
        - JSON response with detail "VIN not found in dataset"
        """
    invalid_vin = "INVALIDVIN12345"
    response = client.post("/vin-summary", json={"vin": invalid_vin})
    assert response.status_code == 404
    assert response.json()["detail"] == "VIN not found in dataset"
