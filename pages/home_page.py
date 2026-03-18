from selenium.webdriver.common.by import By

from config import BASE_URL
from pages.base_page import BasePage


class TwitchHomePage(BasePage):
    # ── Locators ──────────────────────────────────────────────────────────────
    _SEARCH_ICON = (By.CSS_SELECTOR, "a[href='/directory']")
    _SEARCH_ICON_ALT = (
        By.CSS_SELECTOR,
        "[data-a-target='nav-search-button'], a[href*='search']",
    )

    # ── Actions ───────────────────────────────────────────────────────────────

    def load(self):
        self.open(BASE_URL)
        self._wait_visible(self._SEARCH_ICON)
        return self

    def click_search(self) -> None:
        try:
            btn = self._wait_clickable(self._SEARCH_ICON)
        except Exception:
            btn = self._wait_clickable(self._SEARCH_ICON_ALT)
        btn.click()
