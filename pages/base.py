import os
import time

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class WebPage(object):
    _web_driver = None
    _tmpdir = None

    def __init__(self, web_driver=None, url='', tmpdir=None):
        self._web_driver = web_driver
        self.get(url)
        self._tmpdir = tmpdir

    def __getattribute__(self, item):
        attr = object.__getattribute__(self, item)

        if not item.startswith('_') and not callable(attr):
            attr._web_driver = self._web_driver
            attr._page = self

        return attr

    def get(self, url):

        self._web_driver.get(url)
        self.wait_page_loaded()

    def get_current_url(self):
        return self._web_driver.current_url

    def current_window_handle(self):
        """ Идентификатор текущей вкладка браузера """

        return self._web_driver.current_window_handle

    def window_handles(self):
        """ Список идентификаторов всех открытых вкладок браузера """

        return self._web_driver.window_handles

    def switch_to_new_tab(self):
        """ Переключение на другую открытую вкладку браузера """

        original_window = self._web_driver.current_window_handle
        WebDriverWait(self._web_driver, 10).until(EC.number_of_windows_to_be(2))

        for window_handle in self._web_driver.window_handles:
            if window_handle != original_window:
                self._web_driver.switch_to.window(window_handle)
                break

    def get_title(self):
        """ title html-страницы """

        return self._web_driver.execute_script('return document.title')

    def wait_for_file_downloaded(self, file_name, timeout=30):
        """ Ожидание завершения загрузки файла """

        download_directory = str(self._tmpdir)
        file_path = os.path.join(download_directory, file_name)

        start_time = time.time()
        is_file_exist = False

        while not is_file_exist:
            time.sleep(1)
            is_file_exist = os.path.isfile(file_path)

            assert time.time() - start_time < timeout, f"Файл не загружен в течение {timeout} секунд!"

    def downloaded_file_size_mb(self, file_name):
        """ Размер загруженного файла (МБ) """

        download_directory = str(self._tmpdir)
        file_path = os.path.join(download_directory, file_name)
        file_size = os.path.getsize(file_path) / (1024 * 1024)
        return file_size

    def wait_page_loaded(self, timeout=60, sleep_time=2):
        """ Ожидание полной загрузки страницы """

        page_loaded = False
        double_check = False
        start_time = time.time()

        if sleep_time:
            time.sleep(sleep_time)

        while not page_loaded:
            time.sleep(0.5)

            # пробуем прокрутить страницу до конца вниз
            try:
                self._web_driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
                page_loaded = self._web_driver.execute_script("return document.readyState == 'complete';")
            except Exception as err:
                pass

            assert (time.time() - start_time) < timeout, f"Страница не загружена в течение {timeout} секунд!"

            # Дважды проверяем, что страница загружена полностью
            if page_loaded and not double_check:
                page_loaded = False
                double_check = True

        # прокручиваем страницу обратно вверх до конца
        self._web_driver.execute_script('window.scrollTo(document.body.scrollHeight, 0);')
