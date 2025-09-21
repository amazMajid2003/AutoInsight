import pandas as pd
import re
import os
from typing import Optional, Dict, Any


def load_csv(path: str) -> pd.DataFrame:
    """
    Load the CSV dataset into a Pandas DataFrame.

    Args:
        path (str): Path to the CSV file.

    Returns:
        pd.DataFrame: Loaded dataset.

    Raises:
        FileNotFoundError: If the file does not exist at the given path.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"CSV file not found at {path}")
    return pd.read_csv(path)


def parse_number(value: Any) -> Optional[float]:
    """
    Convert mixed-format strings into floats.

    Examples:
        "$12,000" → 12000.0
        "120 days" → 120.0
        "15%" → 15.0

    Args:
        value (Any): Input value, possibly string, int, float, or NaN.

    Returns:
        Optional[float]: Parsed float value, or None if parsing fails.
    """
    if pd.isna(value):
        return None
    if isinstance(value, (int, float)):
        return float(value)

    # Clean formatting like $, commas
    s = str(value).strip()
    s = re.sub(r"[\$,]", "", s)

    # Extract first numeric match
    match = re.search(r"(-?\d+\.?\d*)", s.replace("%", ""))
    if not match:
        return None

    try:
        return float(match.group(1))
    except ValueError:
        return None


def deterministic_summary(row: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate a fallback VIN summary and risk score without LLM.

    Args:
        row (Dict[str, Any]): Row of vehicle data from dataset.

    Returns:
        Dict[str, Any]: Summary dictionary containing:
            - vin (str): VIN code
            - summary (str): Human-readable description
            - risk_score (float): Risk rating scaled 1.0–10.0
            - reasoning (list[str]): Explanation of weighted factors
    """
    # Vehicle basics
    vin = str(row.get("VIN", "")).upper().strip()
    year = (
        int(row.get("Year"))
        if row.get("Year") and not pd.isna(row.get("Year"))
        else None
    )
    make = str(row.get("Make", "Unknown")).upper()
    model = row.get("Model", "Unknown")

    # Parse numeric fields
    price_to_market = parse_number(row.get("Current price to market %")) or 0.0
    days_on_lot = parse_number(row.get("DOL")) or 0
    mileage = parse_number(row.get("Mileage")) or 0
    vdp_views = parse_number(row.get("Total VDPs (lifetime)")) or 0

    # Normalize contributors (0..1)
    ndays = min(days_on_lot / 120.0, 1.0)
    nprice = min(max(price_to_market - 100.0, -50.0) / 50.0, 1.0)  # relative to 100%
    nmileage = min(mileage / 200000.0, 1.0)
    nviews = 1.0 - min(vdp_views / 2000.0, 1.0)  # more views → lower risk

    # Weighted risk calculation
    w_days, w_price, w_mileage, w_views = 0.45, 0.30, 0.15, 0.10
    weighted = (
        w_days * ndays + w_price * nprice + w_mileage * nmileage + w_views * nviews
    )
    risk_score = max(1.0, min(10.0, weighted * 10))  # Scale to 1–10

    # Pricing description (relative to 100% = market)
    diff = price_to_market - 100
    if diff > 2:
        price_phrase = f"{diff:.1f}% above market"
    elif diff < -2:
        price_phrase = f"{abs(diff):.1f}% below market"
    else:
        price_phrase = "near market price"

    # Human-readable summary
    summary = (
        f"{year} {make} {model} with {int(mileage):,} miles, "
        f"priced {price_phrase}, has been on the lot for {int(days_on_lot)} days."
    )

    # Step-by-step reasoning
    reasoning = [
        f"days_on_lot={int(days_on_lot)} (norm {ndays:.2f}, w={w_days})",
        f"price_to_market={price_to_market:.2f}% (norm {nprice:.2f}, w={w_price})",
        f"mileage={int(mileage):,} (norm {nmileage:.2f}, w={w_mileage})",
        f"vdp_views={int(vdp_views)} (inv-norm {nviews:.2f}, w={w_views})",
        f"Weighted={weighted:.3f} → risk {risk_score:.2f}/10"
    ]

    return {
        "vin": vin,
        "summary": summary,
        "risk_score": risk_score,
        "reasoning": reasoning,
    }
