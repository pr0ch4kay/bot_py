# Настройки Appium и устройства
APPIUM_URL = "http://127.0.0.1:4723"

DEVICE = {
    "platformName": "Android",
    "appium:automationName": "UiAutomator2",
    "appium:deviceName": "emulator-5554",
    "appium:platformVersion": "13",
    "appium:appPackage": "ru.vk.store",
    "appium:appActivity": "ru.vk.store.ui.activity.MainActivity",
    "appium:noReset": True,
    "appium:newCommandTimeout": 300,
}

# Пакеты приложений, на которые будем писать отзывы
TARGET_APPS = [
    "com.example.app1",
    "com.example.app2",
]