from pages.base import WebPage
from pages.elements import WebElement
from pages.elements import ManyWebElements

URL_SBUS = "https://sbis.ru/"


class MainPageForFirstScript(WebPage):

    def __init__(self, web_driver):
        url = URL_SBUS
        super().__init__(web_driver, url)

    contacts_link = WebElement(xpath='//a[contains(@href, "/contacts")]')

    tenzor_link = WebElement(class_name='sbisru-Contacts__logo-tensor')

    power_in_people_block = WebElement(
        xpath='//div[contains(@class, "tensor_ru-Index__card") and p[normalize-space(text())="Сила в людях"]]')

    # TODO: можно оптимизировать
    power_in_people_details = WebElement(
        xpath='//div[contains(@class, "tensor_ru-Index__card") and p[normalize-space(text())="Сила в людях"]]'
              '//a[contains(@class, "tensor_ru-link tensor_ru-Index__link") '
              'and normalize-space(text())="Подробнее"]',
        wait_after_click=True)

    working_pictures = ManyWebElements(
        xpath='//div[contains(@class, "tensor_ru-container tensor_ru-section") and '
              './/h2[normalize-space(text())="Работаем"]]//div[contains(@class, "s-Grid-container")]//img')


class MainPageForSecondScript(WebPage):

    def __init__(self, web_driver):
        url = URL_SBUS
        super().__init__(web_driver, url)

    contacts_link = WebElement(xpath='//a[contains(@href, "/contacts")]', wait_after_click=True)

    region = WebElement(
        xpath='//div[contains(@class, '
              '"s-Grid-container s-Grid-container--alignBaseline s-Grid-container--noGutter")]'
              '//span[contains(@class, "sbis_ru-Region-Chooser__text sbis_ru-link")]')

    partners_list = ManyWebElements(xpath='//div[contains(@class, "sbisru-Contacts-List__name")]')

    kamchatskij_kraj_link = WebElement(xpath='//span[contains(@title, "Камчатский край")]', wait_after_click=True)


class MainPageForThirdScript(WebPage):

    def __init__(self, web_driver, tmpdir):
        url = URL_SBUS
        super().__init__(web_driver, url, tmpdir)

    download_sbis_section = WebElement(xpath='//a[normalize-space(text())="Скачать СБИС"]', wait_after_click=True)

    plagin_button = WebElement(
        xpath='//div[contains(@class, "controls-TabButton__caption") and normalize-space(text())="СБИС Плагин"]',
        wait_after_click=True)

    download_file_link = WebElement(
        xpath='//div[contains(@class, "sbis_ru-DownloadNew-block") and '
              './/h3[normalize-space(text())="Веб-установщик"]]'
              '//a[contains(@class, "sbis_ru-DownloadNew-loadLink__link")]')
