import pytest
from dotenv import load_dotenv
from selene import browser


@pytest.fixture(scope="session", autouse=True)
def load_env():
    load_dotenv()


@pytest.fixture(scope="function", autouse=False)
def setup_browser(request):
    yield browser
    browser.quit()
