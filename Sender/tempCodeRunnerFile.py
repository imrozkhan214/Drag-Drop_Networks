from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import socket

from selenium.webdriver.common.devtools.v85 import browser

def set_download_directory(driver, path):
    driver.execute_cdp_cmd("Page.setDownloadBehavior", {
        "behavior": "allow",
        "downloadPath": path
    })

# Predefined course list with URLs
COURSES = {
    "GNS": "https://ustep.ustp.edu.ph/course/resources.php?id=11550",
    "CS311": "https://ustep.ustp.edu.ph/course/resources.php?id=11559",
    "CS316": "https://ustep.ustp.edu.ph/course/resources.php?id=11567",
    "CS312": "https://ustep.ustp.edu.ph/course/resources.php?id=11568",
    "CS313": "https://ustep.ustp.edu.ph/course/resources.php?id=11571",
    "CS314": "https://ustep.ustp.edu.ph/course/resources.php?id=11572",
    "CS315": "https://ustep.ustp.edu.ph/course/resources.php?id=11574",
    "IT314": "https://ustep.ustp.edu.ph/course/resources.php?id=11619",
}

DOWNLOAD_DIR = os.path.join(os.getcwd(), "Downloads")
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

def download_files_from_course(driver, course_name, course_url):
    course_folder = os.path.join(DOWNLOAD_DIR, course_name)
    os.makedirs(course_folder, exist_ok=True)

    driver.get(course_url)
    time.sleep(2)

    rows = driver.find_elements(By.CSS_SELECTOR, "tbody tr")
    resources = []

    for row in rows:
        try:
            td = row.find_element(By.CSS_SELECTOR, "td.cell.c1")