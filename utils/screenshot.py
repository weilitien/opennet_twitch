"""
Screenshot utility — consistent naming, automatic directory creation.
"""

import os
from datetime import datetime

from selenium.webdriver.remote.webdriver import WebDriver

from config import SCREENSHOT_DIR


def take_screenshot(driver: WebDriver, name: str) -> str:
    """
    Save a screenshot and return its file path.

    Args:
        driver: active WebDriver instance
        name:   descriptive label (spaces become underscores)

    Returns:
        Absolute path of the saved file.
    """
    os.makedirs(SCREENSHOT_DIR, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_name = name.replace(" ", "_").lower()
    filename = f"{safe_name}_{timestamp}.png"
    filepath = os.path.join(SCREENSHOT_DIR, filename)

    driver.save_screenshot(filepath)
    print(f"[screenshot] saved → {filepath}")
    return filepath
