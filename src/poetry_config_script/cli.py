from poetry.console.application import Application

from patch import patch


if __name__ == "__main__":
    patch()
    Application().run()
