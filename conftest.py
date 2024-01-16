import pytest
from selenium import webdriver


@pytest.fixture
def web_browser(tmpdir):
    download_directory = str(tmpdir)
    prefs = {"download.default_directory": download_directory}

    options = webdriver.ChromeOptions()
    options.add_experimental_option("prefs", prefs)
    options.add_argument('--headless')

    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()
