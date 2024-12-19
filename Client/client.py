import os
import time
import tkinter as tk
from tkinter import filedialog, Toplevel, Label, Entry, Button, Listbox, MULTIPLE, END
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
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
            link_element = td.find_element(By.TAG_NAME, "a")
            resource_name = link_element.text.strip()
            resource_link = link_element.get_attribute("href")
            if "mod/resource/view.php" in resource_link:
                resources.append((resource_name, resource_link))
        except Exception:
            continue

    if resources:
        open_resource_selection_window(driver, resources, course_folder)
    else:
        print("No resources found.")

def open_resource_selection_window(driver, resources, course_folder):
    def on_submit():
        selected_indices = resource_listbox.curselection()
        selected_resources = [resources[i] for i in selected_indices]
        if not selected_resources:
            print("No resources selected.")
            return

        for resource_name, resource_url in selected_resources:
            driver.get(resource_url)
            time.sleep(2)
            try:
                download_link_element = driver.find_element(By.CLASS_NAME, "resourceworkaround")
                download_href = download_link_element.find_element(By.TAG_NAME, "a").get_attribute("href")
                driver.get(download_href)
            except Exception as e:
                print(f"Error downloading {resource_name}: {e}")
        resource_window.mainloop()
        # resource_window.destroy()

    resource_window = Toplevel()
    resource_window.title("Select Resources to Download")

    Label(resource_window, text="Select Resources:").pack(padx=5, pady=5)
    resource_listbox = Listbox(resource_window, selectmode=MULTIPLE, width=40, height=10)
    for resource_name, _ in resources:
        resource_listbox.insert(END, resource_name)
    resource_listbox.pack(padx=5, pady=5)

    Button(resource_window, text="Download Selected Files", command=on_submit).pack(pady=10)
    Button(resource_window, text="Send Files", command=open_send_prompt).pack(pady=10)

    resource_window.mainloop()

def start_scraping(username, password, selected_courses):
    chrome_options = Options()
    chrome_options.add_experimental_option("prefs", {
        "download.default_directory": DOWNLOAD_DIR,
        "download.prompt_for_download": False,
        "plugins.always_open_pdf_externally": True
    })
    service = Service("E:\\USTP FILES\\3rd year - 1st sem\\Newts and Comms\\EasyFileTransfer\\chromedriver-win64\\chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        driver.get("https://ustep.ustp.edu.ph/login/index.php")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "username"))).send_keys(username)
        driver.find_element(By.ID, "password").send_keys(password + Keys.RETURN)

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "page-header")))

        for course_name in selected_courses:
            course_folder = os.path.join(DOWNLOAD_DIR, course_name)
            os.makedirs(course_folder, exist_ok=True)
            
            # Set the download directory dynamically
            set_download_directory(driver, course_folder)
            
            # Download files for the course
            try:
                download_files_from_course(driver, course_name, COURSES[course_name])
            except Exception as e:
                print(f"Error processing {course_name}: {e}")

        # open_send_prompt()  # Trigger file sending prompt after downloads

    finally:
        driver.quit()

def open_send_prompt():
    def on_yes():
        root.destroy()
        open_file_sender()

    root = tk.Tk()
    root.title("Send File")

    Label(root, text="Do you want to send a file?").pack(pady=10)
    Button(root, text="Yes", command=on_yes).pack(side="left", padx=20, pady=10)
    Button(root, text="No", command=root.destroy).pack(side="right", padx=20, pady=10)

    root.mainloop()

def open_file_sender():
    def send_file():
        file_path = file_entry.get()
        host = host_entry.get()
        port = port_entry.get()

        if file_path and host and port:
            try:
                port = int(port)
                with open(file_path, 'rb') as f:
                    filename = os.path.basename(file_path)
                    file_size = os.path.getsize(file_path)
                    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    client_socket.connect((host, port))
                    client_socket.send(len(filename).to_bytes(4, 'big'))
                    client_socket.send(filename.encode())
                    client_socket.send(file_size.to_bytes(8, 'big'))
                    while chunk := f.read(1024):
                        client_socket.send(chunk)
                    print("File sent successfully!")
                    client_socket.close()
            except Exception as e:
                print(f"Error: {e}")

    def browse_file():
        file_path = filedialog.askopenfilename(initialdir=DOWNLOAD_DIR)
        file_entry.delete(0, tk.END)
        file_entry.insert(0, file_path)

    root = tk.Tk()
    root.title("File Sender")

    Label(root, text="File:").grid(row=0, column=0, pady=5, padx=5)
    file_entry = Entry(root, width=40)
    file_entry.grid(row=0, column=1, pady=5, padx=5)
    Button(root, text="Browse", command=browse_file).grid(row=0, column=2, pady=5, padx=5)

    Label(root, text="Host:").grid(row=1, column=0, pady=5, padx=5)
    host_entry = Entry(root, width=40)
    host_entry.grid(row=1, column=1, pady=5, padx=5)

    Label(root, text="Port:").grid(row=2, column=0, pady=5, padx=5)
    port_entry = Entry(root, width=40)
    port_entry.grid(row=2, column=1, pady=5, padx=5)

    Button(root, text="Send", command=send_file).grid(row=3, column=1, pady=10)
    root.mainloop()

def main():
    def on_submit():
        username = username_entry.get()
        password = password_entry.get()
        selected_indices = course_listbox.curselection()
        selected_courses = [course_listbox.get(i) for i in selected_indices]

        if not username or not password or not selected_courses:
            print("Please provide login credentials and select at least one course.")
            return

        start_scraping(username, password, selected_courses)

    root = tk.Tk()
    root.title("USTEP File Downloader")

    Label(root, text="Username:").grid(row=0, column=0, pady=5, padx=5)
    username_entry = Entry(root, width=40)
    username_entry.grid(row=0, column=1, pady=5, padx=5)

    Label(root, text="Password:").grid(row=1, column=0, pady=5, padx=5)
    password_entry = Entry(root, show="*", width=40)
    password_entry.grid(row=1, column=1, pady=5, padx=5)

    Label(root, text="Courses:").grid(row=2, column=0, pady=5, padx=5)
    course_listbox = Listbox(root, selectmode=MULTIPLE, width=40, height=10)
    for course in COURSES.keys():
        course_listbox.insert(END, course)
    course_listbox.grid(row=2, column=1, pady=5, padx=5)

    Button(root, text="Start", command=on_submit).grid(row=3, column=1, pady=10)
    root.mainloop()

if __name__ == "__main__":
    main()
