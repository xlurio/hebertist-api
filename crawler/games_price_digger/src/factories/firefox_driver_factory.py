import os

from . import DriveFactory
from selenium.webdriver.firefox.options import Options
from selenium import webdriver
from selenium.webdriver.firefox.service import Service


class FirefoxDriveFactory(DriveFactory):

    def make_driver(self, **kwargs):
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--no-sandbox')
        driver_binary = self._get_driver_path()
        service = Service(driver_binary)
        return webdriver.Firefox(service=service, options=options)

    def _get_driver_path(self):
        module_path = os.path.dirname(__file__)
        absolute_module_path = os.path.abspath(module_path)
        root_path = os.path.join(
            absolute_module_path, '../../..'
        )
        return os.path.join(root_path, 'geckodriver')
