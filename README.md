# Twitch WAP Test Framework

Mobile-emulated end-to-end tests for [twitch.tv](https://www.twitch.tv) using **Selenium + pytest**.

> 📱 Tests run inside Chrome's Mobile Emulator (Pixel 5 profile) — no physical device needed.

---

## Demo

> *(Add a GIF here showing the test running locally — e.g. recorded with [LICEcap](https://www.cockos.com/licecap/) or [peek](https://github.com/phw/peek))*

---

## Repository structure

```
twitch_wap_test/
├── pages/                   # Page Object Model
│   ├── base_page.py         # Shared helpers (scroll, popup, screenshot)
│   ├── home_page.py         # Twitch landing page
│   ├── search_page.py       # Search input + results
│   └── streamer_page.py     # Individual channel page
├── components/
│   └── popup_handler.py     # Reusable modal/overlay dismissal
├── utils/
│   ├── driver_factory.py    # Chrome mobile-emulation setup
│   ├── wait_helpers.py      # Explicit wait wrappers
│   └── screenshot.py        # Timestamped screenshot helper
├── tests/
│   └── test_twitch_wap.py   # Test cases
├── screenshots/             # Auto-created; holds captured PNGs
├── config.py                # Device, URL, and timeout settings
├── conftest.py              # pytest fixtures + auto-screenshot on failure
├── pytest.ini               # Runner config and custom markers
└── requirements.txt
```

---

## Setup

```bash
# 1. Clone the repo
git clone <your-repo-url>
cd twitch_wap_test

# 2. Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate

# 3. Install dependencies (ChromeDriver is managed automatically)
pip install -r requirements.txt
```

---

## Running the tests

```bash
# Run all WAP tests
pytest -m wap

# Run only the smoke suite
pytest -m smoke

# Run the full spec test with verbose output
pytest tests/test_twitch_wap.py::TestTwitchWAP::test_search_and_view_streamer -v

# Generate an HTML report
pytest --html=report.html --self-contained-html
```

---

## Test cases

| # | Test | Markers | Description |
|---|------|---------|-------------|
| 1 | `test_search_and_view_streamer` | `wap, smoke` | Full happy-path: open Twitch → search StarCraft II → scroll × 2 → select streamer → screenshot |
| 2 | `test_mobile_viewport_is_applied` | `wap` | Sanity check that Chrome mobile emulation is active |
| 3 | `test_search_returns_results` | `wap` | Verify search returns ≥ 1 result card for StarCraft II |

---

## Design decisions

| Decision | Rationale |
|----------|-----------|
| **Page Object Model** | Separates selectors from test logic; one place to update when Twitch changes its markup |
| **`PopupHandler` component** | Twitch shows various modals; centralising dismissal prevents duplication across pages |
| **`conftest.py` fixture** | Driver lifecycle (create → test → quit) managed once, not per test |
| **`config.py`** | All magic strings in one file — swap device or URL without touching a test |
| **Auto-screenshot on failure** | `pytest_runtest_makereport` hook captures state at the moment of failure |
| **Explicit waits only** | `implicitly_wait` is kept low (5 s); all critical waits use `WebDriverWait` for precision |

---

## Extending the framework

- **New page** → add a class in `pages/` that extends `BasePage`
- **New device** → update `MOBILE_DEVICE` in `config.py`
- **New popup type** → add a locator to `_POPUP_LOCATORS` in `components/popup_handler.py`
- **CI** → uncomment `--headless=new` in `utils/driver_factory.py`
