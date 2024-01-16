from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys


class WebElement(object):
    _locator = ('', '')
    _web_driver = None
    _page = None
    _timeout = 10
    _wait_after_click = False

    def __init__(self, timeout=10, wait_after_click=False, **kwargs):
        self._timeout = timeout
        self._wait_after_click = wait_after_click

        for attr, value in kwargs.items():
            self._locator = (str(attr).replace('_', ' '), str(value))

    def find(self, timeout=10):
        """ Поиск элемента на странице """

        element = None

        try:
            element = WebDriverWait(self._web_driver, timeout).until(
                EC.presence_of_element_located(self._locator)
            )
        except:
            print("Элемент не найден на странице!")

        return element

    def wait_to_be_clickable(self, timeout=10):
        """ Ожидание пока элемент станет кликабельным. """

        element = None

        try:
            element = WebDriverWait(self._web_driver, timeout).until(
                EC.element_to_be_clickable(self._locator)
            )
        except:
            print("Элемент не кликабелен!")

        return element

    def get_text(self):
        """ Получение текста элемента """

        element = self.find()
        text = ''

        try:
            text = str(element.text)
        except Exception as err:
            print(f"Ошибка: {err}")

        return text

    def get_attribute(self, attr_name):
        """ Получение атрибута элемента """

        element = self.find()

        if element:
            return element.get_attribute(attr_name)

    def click(self, hold_seconds=1, x_offset=1, y_offset=1):
        """ Ожидание, когда элемент станет кликабельным и клик по нему """

        element = self.wait_to_be_clickable()

        if element:
            action = ActionChains(self._web_driver)
            action.move_to_element_with_offset(element, x_offset, y_offset). \
                pause(hold_seconds).click(on_element=element).perform()
        else:
            msg = f"Элемент с локатором '{self._locator}' не найден"
            raise AttributeError(msg)

        if self._wait_after_click:
            self._page.wait_page_loaded()

    def scroll_to_element(self):
        """ Прокрутка страницы к элементу """

        element = self.find()

        try:
            element.send_keys(Keys.DOWN)
        except Exception as err:
            pass


class ManyWebElements(WebElement):

    def __getitem__(self, item):
        """ Получение списка элементов и возврат требуемого элемента """

        elements = self.find()
        return elements[item]

    def find(self, timeout=10):
        """ Поиск элементов на странице """

        elements = []

        try:
            elements = WebDriverWait(self._web_driver, timeout).until(
                EC.presence_of_all_elements_located(self._locator)
            )
        except:
            print('Элементы не найдены на странице!')

        return elements

    def count(self):
        """ Получение количества элементов на странице """

        elements = self.find()
        return len(elements)

    def get_text(self):
        """ Получение текста элементов """

        elements = self.find()
        result = []

        for element in elements:
            text = ''

            try:
                text = str(element.text)
            except Exception as err:
                print(f'Error: {err}')

            result.append(text)

        return result
