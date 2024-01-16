import logging

from pages.sbis_ru import MainPageForThirdScript
from conftest import web_browser


def test_download_file_size(web_browser, tmpdir):
    page = MainPageForThirdScript(web_browser, tmpdir)
    logging.info("Перешли на страницу https://sbis.ru/")

    page.download_sbis_section.scroll_to_element()
    page.download_sbis_section.click()
    logging.info("Прокрутили страницу до ссылки 'Скачать СБИС' в footer'e и кликнули по ней")

    page.plagin_button.click()
    logging.info("Кликнули по разделу 'СБИС Плагин'")

    page.download_file_link.click()
    logging.info("В блоке 'Веб-установщик' кликнули 'Скачать'")

    page.wait_for_file_downloaded("sbisplugin-setup-web.exe")

    unformatted_target_file_size = page.download_file_link.get_text().split()[-2]
    target_file_size = float(unformatted_target_file_size)

    unformatted_downloaded_file_size = page.downloaded_file_size_mb("sbisplugin-setup-web.exe")
    downloaded_file_size = round(unformatted_downloaded_file_size, 2)

    assert downloaded_file_size == target_file_size, "Размер файла не соответствует указанному на сайте"
    logging.info(f"Размер скачанного файла соответствует указанному на сайте - {target_file_size} МБ.")
