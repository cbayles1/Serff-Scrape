from selenium import webdriver
from selenium.webdriver.chrome.options import Options
...

# configure webdriver
options = Options()
options.headless = True  # hide GUI
options.add_argument("--window-size=1920,1080")  # set window size to native GUI size
options.add_argument("start-maximized")  # ensure window is full-screen

...
driver = webdriver.Chrome(options=options)
#                         ^^^^^^^^^^^^^^^
driver.get("https://www.twitch.tv/directory/game/Art")
