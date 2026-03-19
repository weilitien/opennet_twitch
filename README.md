# Twitch WAP Test Framework

Mobile-emulated end-to-end tests for [twitch.tv](https://www.twitch.tv) using **Selenium + pytest**.

> Tests run inside Chrome's Mobile Emulator — no physical device needed.

---
## Demo


---

## Repository structure

```
twitch_wap_test/
├── pages/                   # Page Object Model
│   ├── base_page.py         # Shared helpers (scroll, popup, screenshot)
│   ├── home_page.py         
│   ├── search_page.py       
│   └── streamer_page.py     # Individual channel page
├── components/
│   └── popup_handler.py     # Reusable modal/overlay
├── utils/
│   ├── driver_factory.py    # Chrome mobile-emulation setup
│   ├── wait_helpers.py      # Explicit wait wrappers
│   └── screenshot.py        
├── tests/
│   └── test_twitch_wap.py   # Test cases
│   └── conftest.py          # pytest fixtures + auto-screenshot on failure
├── screenshots/             # Auto-created
├── config.py                # Device, URL, and timeout settings
├── pytest.ini               
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
# Run the full spec test with verbose output
pytest tests/ -v

# Generate an HTML report
pytest --html=report.html --self-contained-html
```

---

## Design decisions

| Decision | Rationale |
|----------|-----------|
| **Page Object Model** | Separates selectors from test logic; one place to update when Twitch changes its markup |
| **`PopupHandler` component** | Twitch shows various modals; centralising dismissal prevents duplication across pages |
| **`conftest.py` fixture** | Driver lifecycle (create → test → quit) managed once, not per test |
| **`config.py`** | All magic strings in one file — swap device or URL without touching a test |
| **Auto-screenshot on failure** | `pytest_runtest_makereport` hook captures state at the moment of failure |

---
