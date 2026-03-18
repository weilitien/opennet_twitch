import os
import pytest

from pages.home_page    import TwitchHomePage
from pages.search_page  import SearchPage
from pages.streamer_page import StreamerPage
from config import SEARCH_TERM
from time import sleep

@pytest.mark.wap
@pytest.mark.smoke
class TestTwitchWAP:

    def test_search_and_view_streamer(self, driver):
        # ── Step 1: Open Twitch (mobile) ──────────────────────────────────────
        home = TwitchHomePage(driver)
        home.load()
        home.click_search()

        # ── Step 3: Enter search term ─────────────────────────────────────────
        search = SearchPage(driver)
        search.enter_query(SEARCH_TERM)

        current_url = driver.current_url.lower()
        assert "search" in current_url, (
            f"Expected search URL after query, got: {driver.current_url}"
        )

        # ── Step 4: Scroll down 2 times ───────────────────────────────────────
        search.scroll_results(times=2)

        # ── Step 5: Select a streamer ─────────────────────────────────────────
        search.select_first_streamer()

        # ── Step 6: Wait for page, take screenshot ────────────────────────────
        streamer = StreamerPage(driver)
        screenshot_path = streamer.capture(name=f"streamer_{SEARCH_TERM.replace(' ', '_')}")

        # Assert screenshot exists and is non-empty
        assert os.path.exists(screenshot_path), "Screenshot file was not created."
        assert os.path.getsize(screenshot_path) > 0, "Screenshot file is empty."

        print(f"\n✓ Test passed. Screenshot → {screenshot_path}")


    @pytest.mark.wap
    def test_mobile_viewport_is_applied(self, driver):
        """
        Sanity check: verify the driver is actually running in mobile mode.
        The WAP site is served only when the viewport signals a mobile device.
        """
        home = TwitchHomePage(driver)
        home.load()

        width  = driver.execute_script("return window.innerWidth")
        height = driver.execute_script("return window.innerHeight")

        assert width  <= 430,  f"Viewport width {width}px is not mobile-sized."
        assert height >= 600,  f"Viewport height {height}px seems too small."


    @pytest.mark.wap
    def test_search_returns_results(self, driver):
        """
        Verify that searching StarCraft II returns at least one result card.
        Isolated test — does not depend on streamer click.
        """
        home = TwitchHomePage(driver)
        home.load()
        home.click_search()

        search = SearchPage(driver)
        search.enter_query(SEARCH_TERM)
        search.scroll_results(times=1)

        cards = driver.find_elements(
            *("css selector", "[data-a-target='search-result-card'], .tw-card, article")
        )
        assert len(cards) > 0, (
            f"No result cards found after searching '{SEARCH_TERM}'."
        )
