from pydantic import BaseModel, Field
from typing import List


class VINRequest(BaseModel):
    """
    Request model for VIN summary endpoint.

    Attributes:
        vin (str): The Vehicle Identification Number provided by the user.
    """
    vin: str = Field(..., min_length=5, max_length=50, description="Vehicle Identification Number")


class VINResponse(BaseModel):
    """
    Response model for VIN summary endpoint.

    Attributes:
        vin (str): The VIN that was looked up.
        summary (str): Human-readable summary of the vehicle.
        risk_score (float): Risk score calculated for the vehicle (1.0 to 10.0).
        reasoning (List[str]): Step-by-step reasoning or key points behind the summary.
    """
    vin: str
    summary: str
    risk_score: float = Field(..., ge=1.0, le=10.0, description="Risk score between 1.0 and 10.0")
    reasoning: List[str]
