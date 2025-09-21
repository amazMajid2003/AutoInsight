import pytest
from playwright.sync_api import sync_playwright

# Example VINs for testing
TEST_VINS = [
    "JTDBCMFE8T3112879",
    "",
    "1C6RJTAG957840148"
]

@pytest.mark.parametrize("vin", TEST_VINS)
def test_vin_summary_ui(vin):
    """
    Test the Streamlit UI for the /vin-summary endpoint using a given VIN.

    Steps:
    1. Navigate to the local Streamlit app.
    2. Enter the VIN in the input field (if provided).
    3. Click 'Generate Vehicle Summary'.
    4. Wait for summary and risk score panels to appear (if VIN provided).
    5. Expand reasoning panel if present and assert that items exist.
    """
    if not vin:
        pytest.skip("Skipping test for empty VIN input")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto("http://localhost:8501")

        # Fill VIN
        page.fill("input[placeholder='e.g. 5J6RS5H54RL006999']", vin)
        page.click("text=Generate Vehicle Summary")

        # Wait for summary and risk score panels
        page.wait_for_selector("text=Vehicle Summary", timeout=60000)
        page.wait_for_selector("text=Risk Score", timeout=60000)

        # Capture displayed text
        summary_text = page.text_content("text=Vehicle Summary")
        risk_score_text = page.text_content("text=Risk Score")

        # Check if reasoning expander exists
        reasoning_expanders = page.locator("text=View detailed reasoning")
        if reasoning_expanders.count() > 0:
            page.click("text=View detailed reasoning")
            reasoning_items = page.locator("div[role='region'] li")
            reasoning_count = reasoning_items.count()
            assert reasoning_count > 0
        else:
            # It's OK if no reasoning is shown
            reasoning_count = 0

        # Assertions
        assert vin.upper() in page.content()
        assert summary_text and len(summary_text) > 0
        assert risk_score_text and len(risk_score_text) > 0

        browser.close()
