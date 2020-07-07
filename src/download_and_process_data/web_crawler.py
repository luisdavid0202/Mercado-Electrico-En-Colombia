# Standard library imports
from time import sleep
import os
import platform
import sys
import time

# Third party imports
from selenium import webdriver

# Local application/library imports
import setup


start = time.time()

parent_dir = os.getcwd()
path_to_download_files = os.path.join(parent_dir, setup.DATA_DIRECTORY_NAME)

try:
    os.makedirs(path_to_download_files)
    print(f"\n[INFO] Creating directory: '{path_to_download_files}'...")
except FileExistsError:
    print(f"\n[INFO] Directory '{path_to_download_files}'' already exist...")
    pass

if platform.system() == "Linux":
    chrome_path = setup.CHROME_LINUX_PATH

elif platform.system() == "Windows":
    chrome_path = setup.CHROME_WINDOWS_PATH

else:
    print(f"[INFO] Operating system {platform.system()} not supported...")
    sys.exit()

print(f"[INFO] Driver loaded successfully, working on {platform.system()}...")

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--start-maximized")

prefs = {"download.default_directory": path_to_download_files}
chrome_options.add_experimental_option("prefs", prefs)

driver = webdriver.Chrome(chrome_path, options=chrome_options)

driver.get(setup.PAGE)
print(f"[INFO] Loading page: {setup.PAGE}...")
sleep(setup.WAIT_FOR_PAGE)

element = driver.find_elements_by_css_selector("td.ms-gb")
count_element = 0
for elements in element:
    count_element += 1
    print(f"[INFO] Clicking elements: {count_element}/{len(element)}...")

    elements.find_element_by_css_selector("a").click()
    sleep(setup.WAIT_FOR_CLICK_IN_ELEMENTS)

inputs = driver.find_elements_by_css_selector("td.ms-vb-icon")
count_input = 0
for input in inputs:
    count_input += 1
    foo = input.find_element_by_css_selector("img").get_attribute("title")
    print(f"[INFO] Downloading a file named '{foo}' {count_input}/{len(inputs)}")

    # input.find_element_by_css_selector('img').click()
    sleep(setup.WAIT_FOR_CLICK_IN_INPUTS)

print(f"[INFO] Chrome driver will be closed in {setup.WAIT_TO_CLOSE_DRIVER} seconds...")
sleep(setup.WAIT_TO_CLOSE_DRIVER)
driver.close()

end = time.time()

if end >= 60:
    print("[INFO] Elapsed time on execution: {:.2f} minutes...".format((end - start) / 60))
else:
    print("[INFO] Elapsed time on execution: {:.2f} seconds...".format(end - start))
