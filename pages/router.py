from pages.auth import UserSettingsPage


def get(driver, page, *args):
    action = {
        'user settings': lambda: UserSettingsPage(driver=driver)
    }

    return action[page]()