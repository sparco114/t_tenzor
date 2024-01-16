import logging

from selenium import webdriver
from selenium.webdriver.common.by import By

from pages.sbis_ru import MainPageForSecondScript
from conftest import web_browser


def test_define_and_change_region(web_browser):
    page = MainPageForSecondScript(web_browser)
    logging.info("Перешли на страницу https://sbis.ru/")

    page.contacts_link.click()
    logging.info("Кликнули по разделу 'Контакты'")

    def processing_region(unprocessed_region: list) -> str:
        """
        Оставляет только наименование региона, без указания административно-территориальной формы

        :param unprocessed_region: регион с указанием административно-территориальной формы, разбитый по
            пробелам и сохраненный в форме списка (пример ["Ямало-Ненецкий", "автономный", "округ"])
        """

        processed_region = (unprocessed_region[0]
                            if unprocessed_region[0].lower() not in {'республика', 'respublika'}
                            else unprocessed_region[1])

        return processed_region

    def get_user_region() -> list:
        """
        Получает регион пользователя со стороннего ресурса

        :return: регион с указанием административно-территориальной формы, разбитый по пробелам и сохраненный
            в форме списка (пример ["Республика", "Татарстан"])
        """
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')

        driver = webdriver.Chrome(options=options)

        driver.get("https://ip2ruscity.com")

        region_element = driver.find_element(By.ID, 'ip2cityRegionName')
        region_info = region_element.text.strip().split()

        return region_info

    unprocessed_page_region = page.region.get_text().strip().split()
    unprocessed_user_region = get_user_region()

    user_region = processing_region(unprocessed_user_region)
    defined_region = processing_region(unprocessed_page_region)
    logging.info(f"На сайте был определен регион - '{page.region.get_text()}'")

    assert defined_region == user_region, "Неверно определен регион пользователя"
    logging.info(f"Определенный на сайте регион соответствует региону пользователя")

    local_partners_list = [partner for partner in page.partners_list.get_text()]
    local_partners_list_count = len(local_partners_list)
    assert local_partners_list_count > 0, "Отсутствует список партнеров на сайте"
    logging.info(
        f"На сайте был определен список партнеров. Количество партнеров в списке - {local_partners_list_count}")

    page.region.click()
    page.kamchatskij_kraj_link.click()
    logging.info("Сменили регион на 'Камчатский край'")

    assert page.region.get_text() == "Камчатский край", "При выборе региона не изменилось название региона на странице"
    logging.info("Регион на сайте корректно изменился")

    new_partners_list = [partner for partner in page.partners_list.get_text()]
    assert new_partners_list != local_partners_list, "При изменении региона не изменился список партнеров"
    logging.info(
        f"Список партнеров обновлен с учетом смены региона. Количество партнеров в списке - {len(new_partners_list)}")

    unprocessed_page_title_region = page.get_title().split()[3:]
    unprocessed_new_defined_region = page.region.get_text().strip().split()

    page_title_region = processing_region(unprocessed_page_title_region)
    new_defined_region = processing_region(unprocessed_new_defined_region)

    assert page_title_region == new_defined_region, "Регион, указанный в title не соответствует выбранному"
    logging.info("Регион, указанный в title, соответствует выбранному на сайте региону")

    def transliterate_cyrillic_to_latin(text: str) -> str:
        """ Транслитерация текста с кириллицы на латиницу """

        cyrillic_chars = "щ ш ч ц ю я ё ж ъ ы э а б в г д е з и й к л м н о п р с т у ф х ь".split()
        latin_chars = "shh sh ch cz yu ya yo zh `` y` e` a b v g d e z i j k l m n o p r s t u f h `".split()

        translit_dict = dict(zip(cyrillic_chars, latin_chars))
        transliterated_text = text.lower().replace(' ', '-')

        for cyrillic, latin in translit_dict.items():
            transliterated_text = transliterated_text.replace(cyrillic, latin)

        transliterated_text = (transliterated_text
                               .replace('`', '')
                               .replace('(', '')
                               .replace(')', ''))

        return transliterated_text

    unprocessed_region_in_url = page.get_current_url().split('/')[-1].split('?')[0].split('-')[1:]

    region_in_url = processing_region(unprocessed_region_in_url)

    transliterate_new_defined_region = transliterate_cyrillic_to_latin(new_defined_region)

    assert region_in_url == transliterate_new_defined_region, \
        "Регион в адресе url не соответствует выбранному на странице региону"

    logging.info("Регион, указанный в URL-адресе, соответствует выбранному на сайте региону")
