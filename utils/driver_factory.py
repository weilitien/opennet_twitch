from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from config import MOBILE_DEVICE_IPHONE_14_RPOMAX, IMPLICIT_WAIT


def create_mobile_driver() -> webdriver.Chrome:
    """Return a Chrome driver emulating a mobile device."""
    options = Options()

    mobile_emulation = MOBILE_DEVICE_IPHONE_14_RPOMAX
    options.add_experimental_option("mobileEmulation", mobile_emulation)

    options.add_argument("--no-sandbox")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    # Uncomment to run headless in CI:
    # options.add_argument("--headless=new")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(IMPLICIT_WAIT)
    return driver
