from selenium import webdriver  # for webdriver
from selenium.webdriver.support.ui import Select
import easyocr
import random
import os

PATH = "./driver/chromedriver.exe"
URL = "https://www.gturesults.in/"
CAPTCHA_FILE_NAME = "captcha.jpg"
INPUT_FILE_NAME = "./input/input.txt"
RESULT_FILE_NAME = "./Result/result.csv"
ENROLLMENT_LIST = ["180320107540"]

# Set exam type.
def set_exam(exam_name):
    exam_drop_down = driver.find_element_by_id("ddlbatch")
    exam_list = Select(exam_drop_down)
    exam_list.select_by_visible_text(exam_name)

    # printing all option from dropdown
    # for option in exam_list.options:
    #     print(option.text)


# Getting Enrollment data from txt file.
def get_enrollment_data(file):
    with open(file, "r") as f:
        el_list = f.read().splitlines()
        return el_list


# Set enrollment no.
def set_enrollment(enrollment):
    enrollment_el = driver.find_element_by_id("txtenroll")
    enrollment_el.clear()
    enrollment_el.send_keys(enrollment)


# Locate the captcha and save in the captcha.png
def get_captcha():
    captcha = driver.find_element_by_id("imgCaptcha")
    with open(CAPTCHA_FILE_NAME, "wb") as file:
        file.write(captcha.screenshot_as_png)


# Set captcha.
def set_captcha():
    # Getting the captcha from the website.
    get_captcha()

    # Recognition text from captcha.
    text = reader.readtext(CAPTCHA_FILE_NAME, detail=0)[0]

    # Set captcha in captcha field.
    captcha_el = driver.find_element_by_id("CodeNumberTextBox")
    captcha_el.clear()
    captcha_el.send_keys(text)


# Search result.
def search():
    search_el = driver.find_element_by_id("btnSearch")
    search_el.click()


# Check whether captcha is valid or not.
def is_invalid_captcha():
    message = driver.find_element_by_id("lblmsg").get_attribute("innerHTML")
    return False if "Sorry" in message or "Congratulation" in message else True


# Printing Student Result.
def print_result():
    name = driver.find_element_by_id("lblName").get_attribute("innerHTML")
    enrollment = driver.find_element_by_id("lblEnrollmentNo").get_attribute("innerHTML")
    seatno = driver.find_element_by_id("lblExam").get_attribute("innerHTML")
    exam = driver.find_element_by_id("lblExamName").get_attribute("innerHTML")
    branch = driver.find_element_by_id("lblBranchName").get_attribute("innerHTML")
    curr_backlog = driver.find_element_by_id("lblCUPBack").get_attribute("innerHTML")
    total_backlog = driver.find_element_by_id("lblTotalBack").get_attribute("innerHTML")
    spi = driver.find_element_by_id("lblSPI").get_attribute("innerHTML")
    cpi = driver.find_element_by_id("lblCPI").get_attribute("innerHTML")
    cgpa = driver.find_element_by_id("lblCGPA").get_attribute("innerHTML")

    '''
    result = f"""\n\n
    ** Student Info **
    Name : {name}
    Enrollment No : {enrollment}
    Seat No : {seatno}
    Exam : {exam}
    Branch : {branch}

    ** Result **
    Current Sem. Backlog : {curr_backlog}
    Total Backlog : {total_backlog}
    SPI = {spi}
    CPI = {cpi}
    CGPA = {cgpa}
    \n"""

    print(result)
    '''

    return f"{name},{enrollment},{seatno},{exam},{branch},{curr_backlog},{total_backlog},{spi},{cpi},{cgpa}"


# Storing data in csv file.
def store_result(file, data):
    with open(file, "w") as f:
        f.write("\n".join(data))


""" ------------------- Main Program --------------------- """

# Getting enrollment list form file
ENROLLMENT_LIST = get_enrollment_data(INPUT_FILE_NAME)

# Loading the model for recogniting text from image.
reader = easyocr.Reader(["en"])

""" Without Opening Browser """
option = webdriver.ChromeOptions()
option.add_argument("headless")
option.add_argument("--disable-logging")
driver = webdriver.Chrome(PATH, options=option)
driver.get(URL)

""" With Browser """
# driver = webdriver.Chrome(PATH)
# driver.get(URL)

# Setting the information and search.
set_exam(".....BE SEM 5 - Regular (JAN 2021)")
results = [
    "Name, Enrollment No., Seat No., Exam, Branch, Current Backlog, Toatl Backlog, SPI, CPI, CGPA"
]

for index, enrollment in enumerate(ENROLLMENT_LIST):
    set_enrollment(enrollment)
    is_invalid = True
    while is_invalid:
        # print(f"retring..... {enrollment}")
        set_captcha()
        search()
        is_invalid = is_invalid_captcha()

    print(f"\n{index+1}. {enrollment} result is fetched.")
    results.append(print_result())

# Storing data in csv file.
try:
    store_result(RESULT_FILE_NAME, results)
    print(f"\nResult stored in {RESULT_FILE_NAME}")
except:
    print(f"\nProblem to open {RESULT_FILE_NAME}.")
    new_file = f"{RESULT_FILE_NAME[:-4]}_{random.randint(100,2000)}.csv"
    store_result(new_file, results)
    print(f"\nResult stored in {new_file}")

os.system(f"del {CAPTCHA_FILE_NAME}")
print(f"\nToatal {len(results)-1} result are fetched.")

driver.close()
