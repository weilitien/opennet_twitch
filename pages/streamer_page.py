"""
StreamerPage — the individual channel/stream page.

Key responsibility: wait for the page to be fully loaded before screenshot.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from config import EXPLICIT_WAIT
from pages.base_page import BasePage


class StreamerPage(BasePage):

    # ── Locators ──────────────────────────────────────────────────────────────
    # Any of these present → page is "ready enough" to screenshot
    _VIDEO_PLAYER   = (By.CSS_SELECTOR, "video, [data-a-target='video-player']")
    _CHANNEL_HEADER = (By.CSS_SELECTOR, "[data-a-target='channel-header-title'], h1")

    # ── Actions ───────────────────────────────────────────────────────────────

    def wait_until_loaded(self, timeout: int = EXPLICIT_WAIT) -> None:
        try:
            WebDriverWait(self._driver, timeout).until(
                EC.any_of(
                    EC.visibility_of_element_located(self._VIDEO_PLAYER),
                    EC.visibility_of_element_located(self._CHANNEL_HEADER),
                )
            )
        except Exception:
            pass   # if neither loads, screenshot whatever state we're in

        # Handle mature-content or custom streamer popup
        self.handle_popup(timeout=5)


    def wait_video_play_via_execute(self, timeout=30):
        # readyState 0/1/2/3/4/5 is nothing/meta/current/future...etc
        wait = WebDriverWait(self._driver, timeout)
        self._handle_overlay()

        wait.until(EC.presence_of_element_located((By.TAG_NAME, "video")))

        wait.until(
            lambda d: d.execute_script("""
            const v = document.querySelector('video');
            return !!v &&
                v.readyState >= 2 &&
                !v.paused &&
                !v.ended &&
                v.videoWidth > 0 &&
                v.videoHeight > 0;
        """)
        )


    def capture(self, name: str = "streamer_page") -> str:
        """Wait for load, then take and return the screenshot path."""
        self.wait_video_play_via_execute()
        return self.screenshot(name)
