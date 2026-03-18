import time

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from pages.base_page import BasePage


class SearchPage(BasePage):

    # ── Locators ──────────────────────────────────────────────────────────────
    _SEARCH_INPUT   = (By.CSS_SELECTOR, "input[type='search'], input[placeholder*='Search']")
    _RESULT_CARDS   = (By.CSS_SELECTOR, "[data-a-target='search-result-card'], .tw-card, article")

    # ── Actions ───────────────────────────────────────────────────────────────

    def enter_query(self, query: str):
        field = self._wait_visible(self._SEARCH_INPUT)
        field.clear()
        field.send_keys(query)
        field.send_keys(Keys.RETURN)
        time.sleep(1.5)   # let results render before any scroll

    def scroll_results(self, times: int = 2):
        self.scroll_down(times)

    def select_first_streamer(self) -> str:
        # Try to find live channel cards first; fall back to any card
        cards = self._driver.find_elements(*self._RESULT_CARDS)
        if not cards:
            raise RuntimeError("No streamer cards found in search results.")

        target = cards[0]
        href   = target.get_attribute("href") or ""
        target.click()
        return href
