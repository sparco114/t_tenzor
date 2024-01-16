import logging

from pages.sbis_ru import MainPageForFirstScript
from conftest import web_browser


# logging.basicConfig(level=logging.INFO, format="%(filename)s:%(funcName)s - %(asctime)s [%(levelname)s] %(message)s")

def test_pictures_size(web_browser):
    page = MainPageForFirstScript(web_browser)
    logging.info("Перешли на страницу https://sbis.ru/")

    page.contacts_link.click()
    logging.info("Кликнули по разделу 'Контакты'")

    page.tenzor_link.click()
    logging.info("Кликнули по ссылке 'Тензор'")

    if len(page.window_handles()) > 1:
        page.switch_to_new_tab()
        logging.info(f"Переключились на открывшуюся новую вкладку ({page.get_current_url()})")
        page.wait_page_loaded()

    assert page.power_in_people_details, "Отсутствует блок 'Сила в людях'"
    logging.info("Проверили на странице наличие блока 'Сила в людях'")

    page.power_in_people_details.scroll_to_element()
    logging.info("Прокрутили страницу до блока 'Сила в людях'")

    page.power_in_people_details.click()
    logging.info("В блоке 'Сила в людях' кликнули 'Подробнее'")

    assert page.get_current_url() == "https://tensor.ru/about", "Текущий URL не соотвутсвует 'https://tensor.ru/about'"
    logging.info("Проверили, что ссылка ведет на корректный URL-адрес")

    working_pictures_list = page.working_pictures
    logging.info(f"В разделе 'Работаем' нашли изображения ({working_pictures_list.count()} шт.)")

    unique_pictures_sizes = set()  # set для сохранения только уникальных размеров картинок

    for picture in working_pictures_list:
        picture_size = (picture.get_attribute('width'), picture.get_attribute('height'))
        unique_pictures_sizes.add(picture_size)

    assert len(unique_pictures_sizes) == 1, \
        f"На странице {page.get_current_url()} в разделе 'Работаем' не все картинки одинакового размера"

    logging.info(
        f"У всех найденных изображений одинаковый размер: "
        f"'{tuple(unique_pictures_sizes)[0][0]}x{tuple(unique_pictures_sizes)[0][1]}'")
