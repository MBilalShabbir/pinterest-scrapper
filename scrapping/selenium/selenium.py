import logging as log
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
# from selenium.webdriver.firefox.options import Options
import re
import requests
from datetime import datetime, timedelta
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager

from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options


BASE_URL = "https://www.pinterest.com/"


def fetch_data(url):
    results = {}
    try:
        options = Options()
        # options.add_argument("--headless")
        delay = 7  # seconds
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        wait = WebDriverWait(driver, delay)
        driver.get(url)
        driver.set_page_load_timeout(delay)
        driver.execute_script("window.scrollTo(0, 7200)")
        if "/search/" in driver.current_url:
            search_res = []
            pins = wait.until(
                EC.visibility_of_all_elements_located((By.XPATH, '//div[@role="listitem"]'))
            )

            pins_a = [p.find_element(By.TAG_NAME, 'a') for p in pins]
            hrefs = [p.get_attribute('href') for p in pins_a]
            for uri in hrefs:
                try:
                    driver.get(uri)
                    title = driver.find_element(By.TAG_NAME, 'h1').text
                    img = driver.find_element(By.TAG_NAME, 'img').get_attribute('src')
                    videos = driver.find_elements(By.TAG_NAME, 'video')
                    # driver.set_script_timeout(10)
                    video = ''
                    if videos:
                        res = requests.get(url=uri)
                        video = min(list(set(re.findall(r'https://[^"]+' + '[^"]+mp4', res.text))), key=len, default='')
                    search_res.append({
                        "pin": uri,
                        "title": title,
                        "image": img,
                        "video": video
                    })
                except Exception as er:
                    print(str(er))
                results["search_pins"] = search_res

        elif driver.current_url.strip('/').split('/')[-1] == "_saved":
            acc_name = driver.current_url.strip('/').split('_saved')[0].strip('/').split('/')[-1]
            board_a = [a.get_attribute('href') for a in driver.find_elements(By.TAG_NAME, 'a')]
            boards = []
            for board_uri in board_a:
                board_res = []
                driver.get(board_uri)
                board_name = board_uri.strip('/').split('/')[-1]
                pins = wait.until(
                    EC.visibility_of_all_elements_located((By.XPATH, '//div[@role="listitem"]'))
                )

                pins_a = [p.find_element(By.TAG_NAME, 'a') for p in pins]
                hrefs = [p.get_attribute('href') for p in pins_a]
                for uri in hrefs:
                    driver.get(uri)
                    title = driver.find_element(By.TAG_NAME, 'h1').text
                    img = driver.find_element(By.TAG_NAME, 'img').get_attribute('src')
                    videos = driver.find_elements(By.TAG_NAME, 'video')
                    video = ''
                    if videos:
                        res = requests.get(url=uri)
                        video = min(list(set(re.findall(r'https://[^"]+' + '[^"]+mp4', res.text))), key=len, default='')
                    board_res.append({
                        "pin": uri,
                        "title": title,
                        "image": img,
                        "video": video,
                        "board": board_name
                    })

                boards.append({
                    "board_name": board_name,
                    "board_pins": board_res
                })

            results["account"] = {'account_name': acc_name, "boards": boards}

        elif driver.current_url.strip('/').split('/')[-1] == "_created":
            acc_name = driver.current_url.strip('/').split('/')[-2]
            acc_pins_res = []
            pins = wait.until(
                EC.visibility_of_all_elements_located((By.XPATH, '//div[@role="listitem"]'))
            )

            pins_a = [p.find_element(By.TAG_NAME, 'a') for p in pins]
            hrefs = [p.get_attribute('href') for p in pins_a]
            for uri in hrefs:
                driver.get(uri)
                title = driver.find_element(By.TAG_NAME, 'h1').text
                img = driver.find_element(By.TAG_NAME, 'img').get_attribute('src')
                videos = driver.find_elements(By.TAG_NAME, 'video')
                video = ''
                if videos:
                    res = requests.get(url=uri)
                    video = min(list(set(re.findall(r'https://[^"]+' + '[^"]+mp4', res.text))), key=len, default='')
                acc_pins_res.append({
                    "pin": uri,
                    "title": title,
                    "image": img,
                    "video": video
                })

            results["account"] = {"account_name": acc_name, "account_pins": acc_pins_res}

        elif "/" not in driver.current_url.split('pinterest.com')[-1].strip('/'):
            # is_boards = driver.find_elements(By.XPATH, '//div[@data-test-id="pwt-grid-item"]')
            # is_pins = driver.find_elements(By.XPATH, '//div[@role="listitem"]')
            #
            # if is_pins:
            #     acc_name = driver.current_url.split('pinterest.com')[-1].strip('/')
            #     acc_pins_res = []
            #     pins = wait.until(
            #         EC.visibility_of_all_elements_located((By.XPATH, '//div[@role="listitem"]'))
            #     )
            #
            #     pins_a = [p.find_element(By.TAG_NAME, 'a') for p in pins]
            #     hrefs = [p.get_attribute('href') for p in pins_a]
            #     for uri in hrefs:
            #         driver.get(uri)
            #         title = driver.find_element(By.TAG_NAME, 'h1').text
            #         img = driver.find_element(By.TAG_NAME, 'img').get_attribute('src')
            #         videos = driver.find_elements(By.TAG_NAME, 'video')
            #         video = ''
            #         if videos:
            #             res = requests.get(url=uri)
            #             video = min(list(set(re.findall(r'https://[^"]+' + '[^"]+mp4', res.text))), key=len, default='')
            #         acc_pins_res.append({
            #             "pin": uri,
            #             "title": title,
            #             "image": img,
            #             "video": video
            #         })
            #
            #     results["account"] = {"account_name": acc_name, "account_pins": acc_pins_res}
            #
            # elif is_boards:
            acc_name = driver.current_url.strip('/').split('_saved')[0].strip('/').split('/')[-1]
            driver.get(f"{BASE_URL}{acc_name}/_saved")
            driver.execute_script("window.scrollTo(0, 720)")
            board_addresses = wait.until(
                EC.visibility_of_all_elements_located((By.XPATH, '//div[@role="listitem"]'))
            )

            board_a = [p.find_element(By.TAG_NAME, 'a').get_attribute('href') for p in board_addresses]
            boards = []
            for board_uri in board_a:
                board_res = []
                driver.get(board_uri)
                board_name = board_uri.strip('/').split('/')[-1]
                pins = wait.until(
                    EC.visibility_of_all_elements_located((By.XPATH, '//div[@role="listitem"]'))
                )

                pins_a = [p.find_element(By.TAG_NAME, 'a') for p in pins]
                hrefs = [p.get_attribute('href') for p in pins_a]
                for uri in hrefs:
                    driver.get(uri)
                    title = driver.find_element(By.TAG_NAME, 'h1').text
                    img = driver.find_element(By.TAG_NAME, 'img').get_attribute('src')
                    videos = driver.find_elements(By.TAG_NAME, 'video')
                    video = ''
                    if videos:
                        res = requests.get(url=uri)
                        video = min(list(set(re.findall(r'https://[^"]+' + '[^"]+mp4', res.text))), key=len,
                                    default='')
                    board_res.append({
                        "pin": uri,
                        "title": title,
                        "image": img,
                        "video": video,
                        "board": board_name
                    })

                boards.append({
                    "board_name": board_name,
                    "board_pins": board_res
                })

            results["account"] = {'account_name': acc_name, "boards": boards}

        else:
            title = driver.find_element(By.TAG_NAME, 'h1').text
            img = driver.find_element(By.TAG_NAME, 'img').get_attribute('src')
            videos = driver.find_elements(By.TAG_NAME, 'video')
            video = ''
            if videos:
                res = requests.get(url=driver.current_url)
                video = min(list(set(re.findall(r'https://[^"]+' + '[^"]+mp4', res.text))), key=len, default='')

            results["pin"] = {
                    "pin": driver.current_url,
                    "title": title,
                    "image": img,
                    "video": video
                }

            related_pins = []
            pins = wait.until(
                EC.visibility_of_all_elements_located((By.XPATH, '//div[@role="listitem"]'))
            )

            pins_a = [p.find_element(By.TAG_NAME, 'a') for p in pins]
            hrefs = [p.get_attribute('href') for p in pins_a]
            for uri in hrefs:
                driver.get(uri)
                title = driver.find_element(By.TAG_NAME, 'h1').text
                img = driver.find_element(By.TAG_NAME, 'img').get_attribute('src')
                videos = driver.find_elements(By.TAG_NAME, 'video')
                video = ''
                if videos:
                    res = requests.get(url=uri)
                    video = min(list(set(re.findall(r'https://[^"]+' + '[^"]+mp4', res.text))), key=len, default='')
                related_pins.append({
                    "pin": uri,
                    "title": title,
                    "image": img,
                    "video": video
                })
            results["related_pins"] = related_pins
    except Exception as err:
        print(f'error: {err}')

    driver.quit()
    return results
