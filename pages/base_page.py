from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from utils.screenshot import take_screenshot
from utils.wait_helpers import wait_for_element, wait_for_clickable
from time import sleep


class BasePage:
    def __init__(self, driver: WebDriver):
        self._driver = driver

    # ── Navigation ────────────────────────────────────────────────────────────

    def open(self, url: str) -> None:
        self._driver.get(url)

    # ── Scroll ────────────────────────────────────────────────────────────────

    def scroll_down(self, times=1):
        for _ in range(times):
            sleep(0.5)
            self._driver.execute_script(
                """
                window.scrollBy({
                top: window.innerHeight,
                behavior: 'smooth'
                });
                """
            )

    def _handle_overlay(self):
        # fuzzy match
        overlays = self._driver.find_elements(
            By.XPATH,
            "//*[contains(@class,'modal') or contains(@class,'overlay') or contains(@class,'consent')]",
        )

        for overlay in overlays:
            if overlay.is_displayed():
                buttons = overlay.find_elements(By.XPATH, ".//button")
                for btn in buttons:
                    text = btn.text.lower()
                    if any(
                        k in text
                        for k in [
                            "accept",
                            "agree",
                            "start",
                            "watch",
                            "understand",
                            "close",
                            "ok",
                            "同意",
                        ]
                    ):
                        btn.click()
                        return True
        return False

    # ── Screenshot ────────────────────────────────────────────────────────────

    def screenshot(self, name: str) -> str:
        return take_screenshot(self._driver, name)

    # ── Element shortcuts ─────────────────────────────────────────────────────

    def _wait_visible(self, locator: tuple):
        return wait_for_element(self._driver, locator)

    def _wait_clickable(self, locator: tuple):
        return wait_for_clickable(self._driver, locator)
