from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement


class WebDriverWaitBuilder:

    def set_driver(self, driver: WebDriver):
        self._driver = driver
        return self

    def set_timeout(self, timeout: int):
        self._timeout = timeout
        return self

    def set_xpath_of_element_to_wait(self, xpath_of_element_to_wait):
        self._xpath_of_element_to_wait = xpath_of_element_to_wait
        return self

    def wait(self) -> WebElement:
        webdriver_parameters = {
            'driver': self._driver,
            'timeout': self._timeout
        }
        return WebDriverWait(**webdriver_parameters).until(
            EC.presence_of_element_located((
                By.XPATH, self._xpath_of_element_to_wait
            ))
        )
