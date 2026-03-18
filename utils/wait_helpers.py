"""
Centralised wait helpers — keep Explicit Wait logic out of pages and tests.
"""

import time
from typing import Callable, Optional

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from config import EXPLICIT_WAIT, IMPLICIT_WAIT


def wait_for_element(
    driver: WebDriver,
    locator: tuple,
    timeout: int = EXPLICIT_WAIT,
) -> WebElement:
    """Wait until an element is visible and return it."""
    return WebDriverWait(driver, timeout).until(
        EC.visibility_of_element_located(locator)
    )


def wait_for_clickable(
    driver: WebDriver,
    locator: tuple,
    timeout: int = EXPLICIT_WAIT,
) -> WebElement:
    """Wait until an element is clickable and return it."""
    return WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable(locator)
    )


def wait_for_url_contains(
    driver: WebDriver,
    fragment: str,
    timeout: int = EXPLICIT_WAIT,
) -> bool:
    """Wait until the current URL contains *fragment*."""
    return WebDriverWait(driver, timeout).until(
        EC.url_contains(fragment)
    )


def element_exists(
    driver: WebDriver,
    locator: tuple,
    timeout: int = 3,
) -> bool:
    """Return True if element appears within *timeout* seconds, else False."""
    try:
        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located(locator)
        )
        return True
    except TimeoutException:
        return False


def wait_for_condition(
    driver: WebDriver,
    condition: Callable,
    timeout: int = EXPLICIT_WAIT,
    poll: float = 0.5,
) -> bool:
    """Poll *condition(driver)* until it returns truthy or timeout expires."""
    end = time.time() + timeout
    while time.time() < end:
        try:
            if condition(driver):
                return True
        except Exception:
            pass
        time.sleep(poll)
    raise TimeoutException(f"Condition not met within {timeout}s")
