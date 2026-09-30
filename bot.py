import time
import random
import json
import os

from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from config import APPIUM_URL, DEVICE, TARGET_APPS
from reviews import REVIEW_TEXTS, RATINGS

STATE_FILE = "state.json"


def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_state(state):
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


def start_driver():
    options = UiAutomator2Options()
    for k, v in DEVICE.items():
        options.set_capability(k, v)
    return webdriver.Remote(APPIUM_URL, options=options)


def open_app_page(driver, package_name):
    """Открываем страницу приложения в RuStore через deep link."""
    driver.execute_script("mobile: deepLink", {
        "url": f"rustore://apps/{package_name}",
        "package": "ru.vk.store"
    })
    time.sleep(5)


def leave_review(driver, text, rating):
    wait = WebDriverWait(driver, 20)

    # 1. Скроллим вниз до блока отзывов
    for _ in range(5):
        driver.swipe(500, 1500, 500, 500, 400)
        time.sleep(1)

    # 2. Кнопка "Оставить отзыв" (локатор подгони под реальный!)
    review_btn = wait.until(EC.element_to_be_clickable(
        (AppiumBy.ANDROID_UIAUTOMATOR,
         'new UiSelector().textContains("Оставить отзыв")')
    ))
    review_btn.click()
    time.sleep(3)

    # 3. Звёзды (локатор подгони под реальный!)
    stars = driver.find_elements(
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().resourceIdMatches(".*rating_star.*")'
    )
    if stars and rating <= len(stars):
        stars[rating - 1].click()
    time.sleep(2)

    # 4. Поле ввода текста
    text_field = wait.until(EC.presence_of_element_located(
        (AppiumBy.CLASS_NAME, "android.widget.EditText")
    ))
    text_field.click()
    text_field.send_keys(text)
    time.sleep(2)

    # 5. Кнопка "Отправить"
    send_btn = wait.until(EC.element_to_be_clickable(
        (AppiumBy.ANDROID_UIAUTOMATOR,
         'new UiSelector().textContains("Отправить")')
    ))
    send_btn.click()
    time.sleep(5)


def main():
    state = load_state()
    driver = start_driver()

    try:
        for package in TARGET_APPS:
            if state.get(package) == "done":
                print(f"[SKIP] Уже оставлен отзыв: {package}")
                continue

            text = random.choice(REVIEW_TEXTS)
            rating = random.choice(RATINGS)

            print(f"[*] Открываю {package}")
            open_app_page(driver, package)

            print(f"[*] Оставляю отзыв ({rating}★): {text}")
            leave_review(driver, text, rating)

            state[package] = "done"
            save_state(state)
            print(f"[OK] Отзыв оставлен для {package}")

            # Пауза, чтобы не палиться
            pause = random.randint(60, 180)
            print(f"[*] Пауза {pause} сек...")
            time.sleep(pause)

    finally:
        driver.quit()


if __name__ == "__main__":
    main()