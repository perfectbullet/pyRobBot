"""Entrypoint for the package's UI."""
import os
from pyrobbot import GeneralDefinitions
from pyrobbot.app.multipage import MultipageChatbotApp

os.environ["HTTP_PROXY"] = ''
os.environ["HTTPS_PROXY"] = ''
os.environ["all_proxy"] = ''
os.environ["ALL_PROXY"] = ''


def run_app():
    """Create and run an instance of the pacage's app."""
    MultipageChatbotApp(
        page_title=GeneralDefinitions.APP_NAME,
        page_icon=":speech_balloon:",
        layout="wide",
    ).render()


if __name__ == "__main__":
    run_app()
