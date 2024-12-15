from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tkinter import Tk, Label, Entry, Button, Listbox, MULTIPLE, END, Toplevel
import os
import time

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

# Set up the download directory
DOWNLOAD_DIR = os.path.join(os.getcwd(), "Downloads")
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

def download_files_from_course(driver, course_name, course_url):
    """Navigate to a course page, follow each resource link, and download files."""
    # Create a folder for each course inside DOWNLOAD_DIR
    course_folder = os.path.join(DOWNLOAD_DIR, course_name)
    os.makedirs(course_folder, exist_ok=True)

    driver.get(course_url)
    time.sleep(2)  # Let the page load

    # Find rows under the tbody containing valid file links
    rows = driver.find_elements(By.CSS_SELECTOR, "tbody tr")  # Get all rows inside the <tbody>
    resources = []

    for row in rows:
        try:
            td = row.find_element(By.CSS_SELECTOR, "td.cell.c1")  # Locate the specific <td> element with files
            img = td.find_element(By.TAG_NAME, "img")  # Check if <img> exists
            link_element = td.find_element(By.TAG_NAME, "a")  # Check if <a> exists

            if img and "activityicon" in img.get_attribute("class") and link_element:
                resource_name = link_element.text.strip()
                resource_link = link_element.get_attribute("href")

                # Further filter: Ensure it's a file resource
                if "mod/resource/view.php" in resource_link:
                    resources.append((resource_name, resource_link))
                    print(f"Found resource: {resource_name} with link {resource_link}")
        except Exception as e:
            print(f"Error processing row: {e}")
            continue

    # Check if resources were found and display them
    if resources:
        print(f"Found {len(resources)} resources.")  # Debug: Print the number of resources found
        open_resource_selection_window(driver, resources, course_folder)  # Pass the course folder to the selection window
    else:
        print("No resources found.")  # Debug: No resources found

def open_resource_selection_window(driver, resources, course_folder):
    """Create a Tkinter window for selecting which resources to download."""
    def on_submit():
        selected_indices = resource_listbox.curselection()
        selected_resources = [resources[i] for i in selected_indices]

        if not selected_resources:
            print("No resources selected.")
            return

        # Download selected files
        for resource_name, resource_url in selected_resources:
            driver.get(resource_url)
            time.sleep(2)  # Wait for the page to load

            try:
                # Find the link inside the element with class 'resourceworkaround' that contains 'Click'
                download_link_element = driver.find_element(By.CLASS_NAME, "resourceworkaround")
                download_href = download_link_element.find_element(By.TAG_NAME, "a").get_attribute("href")

                # Save the file to the course folder
                download_link = download_href.split("/")[-1]  # Get the filename from the link
                file_path = os.path.join(course_folder, download_link)  # Save it inside the course folder

                # Start the download by visiting the file link
                driver.get(download_href)
                print(f"Downloaded {resource_name} and saved to {file_path}")
            except Exception as e:
                print(f"No downloadable file found in {resource_url}. Error: {e}")
        resource_window.destroy()

    # Create the selection window
    resource_window = Toplevel()
    resource_window.title("Select Resources to Download")

    Label(resource_window, text="Select Resources:").pack(padx=5, pady=5)

    # Create a listbox with the resources, displaying filenames
    resource_listbox = Listbox(resource_window, selectmode=MULTIPLE, width=40, height=10)
    for resource_name, _ in resources:
        resource_listbox.insert(END, resource_name)  # Show resource names
    resource_listbox.pack(padx=5, pady=5)

    # Submit button to start the download
    Button(resource_window, text="Download Selected Files", command=on_submit).pack(pady=10)

    resource_window.mainloop()

def start_scraping(username, password, selected_courses):
    """Log in and download files from selected courses."""
    # Set up Chrome WebDriver with specified download directory
    chrome_options = Options()
    chrome_options.add_experimental_option("prefs", {
        "download.default_directory": DOWNLOAD_DIR,  # Set custom download directory
        "download.prompt_for_download": False,  # Disable download prompt
        "download.directory_upgrade": True,  # Allow upgrading the download directory
        "plugins.always_open_pdf_externally": True  # Force PDFs to open externally (not in Chrome)
    })
    service = Service(r"C:\Users\lenovo\Documents\ChromeDriver\chromedriver-win64\chromedriver.exe")  # Ensure the path to chromedriver is correct
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        # Log in to USTEP
        driver.get("https://ustep.ustp.edu.ph/login/index.php")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "username"))).send_keys(username)
        driver.find_element(By.ID, "password").send_keys(password + Keys.RETURN)

        # Wait for login to complete
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "page-header")))

        for course_name in selected_courses:
            course_url = COURSES[course_name]
            download_files_from_course(driver, course_name, course_url)

    finally:
        driver.quit()

def main():
    """Main function to run the Tkinter GUI."""
    def on_submit():
        username = username_entry.get()
        password = password_entry.get()
        selected_indices = course_listbox.curselection()
        selected_courses = [course_listbox.get(i) for i in selected_indices]

        if not username or not password or not selected_courses:
            print("Please provide login credentials and select at least one course.")
            return

        # Start scraping
        start_scraping(username, password, selected_courses)

    # Tkinter GUI setup
    root = Tk()
    root.title("USTEP File Downloader")

    Label(root, text="Username:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
    username_entry = Entry(root, width=30)
    username_entry.grid(row=0, column=1, padx=5, pady=5)

    Label(root, text="Password:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
    password_entry = Entry(root, width=30, show="*")
    password_entry.grid(row=1, column=1, padx=5, pady=5)

    Label(root, text="Select Courses:").grid(row=2, column=0, padx=5, pady=5, sticky="ne")
    course_listbox = Listbox(root, selectmode=MULTIPLE, width=40, height=10)
    for course_name in COURSES.keys():
        course_listbox.insert(END, course_name)
    course_listbox.grid(row=2, column=1, padx=5, pady=5)

    Button(root, text="Download Files", command=on_submit).grid(row=3, column=0, columnspan=2, pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()