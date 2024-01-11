from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.common import NoSuchElementException
import time
import re



driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

class AF:
    def __init__(self):
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--headless')
        self.options.add_argument("--window-size=1920,1080")
        self.options.add_argument('--disable-extensions')
        self.options.add_argument('--disable-gpu')
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--disable-dev-shm-usage')
        self.options.add_argument('--enable-logging')
        self.options.add_argument('--v=1')
        self.options.add_argument("--incognito")
        self.options.add_argument("--disable-cache")
        self.date_pattern = re.compile(r'\b\d{1,2}/\d{1,2}/\d{4}\b')
        try:
            self.driver = webdriver.Chrome(options=self.options)
        except Exception as e:
            print("Error Creating driver :", e)
        self.driver = webdriver.Chrome(options=self.options)

    def remove_headless(self):
        self.options.arguments.remove('--headless')
        self.options.add_argument("--display=:99")
        self.driver = webdriver.Chrome(options=self.options)

    def go_to_url(self, url):
        self.driver.get(url)

    def take_screenshot(self, filename='screenshot.png'):
        original_size = self.driver.get_window_size()
        total_width = 1920
        total_height = self.driver.execute_script("return document.body.scrollHeight")
        self.driver.set_window_size(total_width, total_height)
        screenshot = self.driver.get_screenshot_as_png()
        self.driver.set_window_size(original_size['width'], original_size['height'])
        self.driver.save_screenshot(filename)
        self.driver.set_window_size(original_size['width'], original_size['height'])
        return filename

    def enter_text_by_id(self, text, ele_id):
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, ele_id)))
        input_field = self.driver.find_element(By.ID, ele_id)
        input_field.clear()
        input_field.send_keys(text)

    def enter_text_by_xpath(self, text, ele_xpath):
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, ele_xpath)))
        input_field = self.driver.find_element(By.XPATH, ele_xpath)
        input_field.clear()
        input_field.send_keys(text)

    def get_element_text(self, ele_xpath):
        try:
            WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, ele_xpath)))
            element = self.driver.find_element(By.XPATH, ele_xpath)
            return element.text
        except:
            try:
                element = self.driver.execute_script(f"""
                    var xpath = "{ele_xpath}";
                    return document.evaluate(xpath, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                 """)
                return element.text
            except:
                return ""

    def enter_text_by_xpath_and_enter(self, text, ele_xpath):
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, ele_xpath)))
        input_field = self.driver.find_element(By.XPATH, ele_xpath)
        input_field.clear()
        input_field.send_keys(text)
        input_field.send_keys(Keys.RETURN)

    def get_input_value(self, ele_xpath):
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, ele_xpath)))
        input_field = self.driver.find_element(By.XPATH, ele_xpath)
        return input_field.get_attribute('value')

    def enter_text_by_xpath_javascript(self, text, ele_xpath):
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, ele_xpath)))
        self.driver.execute_script(
            f'document.evaluate("{ele_xpath}", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.value = "{text}";')

    def enter_text_by_class_and_enter(self, text, classname):
        parent_element = self.driver.find_element(By.CLASS_NAME, classname)
        parent_element.click()
        input_element = parent_element.find_element(By.TAG_NAME, 'input')
        input_element.clear()
        input_element.send_keys(text)
        input_element.send_keys(Keys.RETURN)

    def click_button_by_xpath(self, xpath):
        button = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpath)))
        button.click()

    def click_button_by_xpath_javascript(self, xpath):
        if self.is_element_there_by_xpath(xpath):
            button = self.driver.find_element(By.XPATH, xpath)
            self.driver.execute_script("arguments[0].click();", button)
        else:
            print('element not found')

    def wait_for_element_xpath(self, ele_xpath):
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, ele_xpath)))

    def wait_for_page_to_be(self, url):
        WebDriverWait(self.driver, 10).until(EC.url_to_be(url))

    def wait_url_includes(self, text):
        WebDriverWait(self.driver, 10).until(EC.url_contains(text))

    def wait_text_not_empty(self, ele_xpath):
        def element_text_not_empty(driver):
            element = driver.find_element(By.XPATH, ele_xpath)
            return element.text.strip() != ""

        wait = WebDriverWait(self.driver, 10)
        wait.until(element_text_not_empty)

    def get_href_by_xpath(self, ele_xpath):
        try:
            element = self.driver.find_element(By.XPATH, ele_xpath)
            href_value = element.get_attribute('href')
            return href_value
        except Exception as e:
            return ""

    def wait_element_contains_class(self, classtxt):
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[@class='" + classtxt + "']"))
        )

    def check_text_in_element(self, text, ele_xpath):
        try:
            element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, ele_xpath))
            )
            txtarr = text.lower().split()
            eletxtarr1 = [item.lower().strip() for item in element.text.split(',')]
            eletxtarr2 = [item.lower().strip() for item in element.text.split(',')]
            return all(elem in eletxtarr1 for elem in txtarr) or all(elem in eletxtarr2 for elem in txtarr)
        except:
            return False

    def quit(self):
        self.driver.close()

    def is_element_there(self, ele_id):
        try:
            self.driver.find_element(By.ID, ele_id)
            return True
        except NoSuchElementException:
            return False

    def is_element_there_by_xpath(self, xpath):
        try:
            self.driver.find_element(By.XPATH, xpath)
            return True
        except NoSuchElementException:
            return False

    def change_chrome_size(self):
        total_width = 1920
        total_height = self.driver.execute_script("return document.body.scrollHeight")
        self.driver.set_window_size(total_width, total_height)

    def select_from_dropdown_by_id(self, text, ele_id):
        dropdown = Select(self.driver.find_element(By.ID, ele_id))
        dropdown.select_by_visible_text(text)

    def close_driver(self):
        window_handles = self.driver.window_handles
        for handle in window_handles:
            self.driver.switch_to.window(handle)
            self.driver.close()

    def babyf(self):

        self.go_to_url("https://www.mdquery.com/app/login.aspx?ID=fbdccc68-ca27-4497-8ceb-603c68b1e89c")
        self.enter_text_by_id("Credentialing", 'YourName')
        self.enter_text_by_id("Access Health Care Physicians", 'YourFacilityName')
        self.enter_text_by_id("credentialing@accesshealthcarellc.net", 'Email')
        self.enter_text_by_id("bayfront", 'Login_TextBox')
        self.enter_text_by_id("query", 'Password_TextBox')
        self.click_button_by_xpath('//*[@id="Agree"]')
        self.click_button_by_xpath('//*[@id="Login_Button"]')
        self.enter_text_by_id("1326129214", 'NPI_TextBox')
        self.click_button_by_xpath('//*[@id="Search_Button"]')
        self.click_button_by_xpath('//*[@id="SearchResults_GridView"]/tbody/tr/td[1]/a')
        new_window_handle = self.driver.window_handles[-1]
        self.driver.switch_to.window(new_window_handle)
        screenshot_filename = self.take_screenshot('bayfront_screenshot.png')
        self.quit()

    def babyc(self):
        self.remove_headless()
        self.go_to_url(
            "https://bccactus.baycare.org/iResponse/Account/Login?ReturnUrl=%2FiResponse%2FSearch%2FIndex%E2%80%9D")
        self.enter_text_by_id("eduffin@credaxis.com", 'Email')
        self.enter_text_by_id("1214Mariner", 'Password')
        self.click_button_by_xpath('//*[@id="btnSubmit"]')
        self.enter_text_by_id("1427043421", 'ProviderNPI')
        self.click_button_by_xpath('//*[@id="submit"]')
        self.click_button_by_xpath('/html/body/div/div[2]/div/div[2]/div/div[2]/div/div[1]/a')
        time.sleep(7)
        new_window_handle = self.driver.window_handles[-1]
        self.driver.switch_to.window(new_window_handle)
        screenshot_bytes = self.driver.get_screenshot_as_png()
        return screenshot_bytes
        self.quit()

    def hca(self):
        self.go_to_url("https://hcacredentialing.app.medcity.net/iResponse/ApplicationSpecific/login.asp")
        self.enter_text_by_id("jkaur@ahcpllc.com", 'text1')
        self.enter_text_by_id("Access@1234", 'password1')
        self.click_button_by_xpath(
            '/html/body/div/div[1]/div/div/div/table/tbody/tr/td[1]/form/table/tbody/tr[5]/td/input')
        self.enter_text_by_xpath("1811250913", "/html/body/div/div/div/div/form/table/tbody/tr[4]/td[2]/input")
        self.click_button_by_xpath("/html/body/div/div/div/div/form/table/tbody/tr[6]/td[2]/input")
        self.click_button_by_xpath('/html/body/div/div[2]/div/div/table[1]/tbody/tr[1]/td/a')
        new_window_handle = self.driver.window_handles[-1]
        self.driver.switch_to.window(new_window_handle)
        time.sleep(8)
        return self.take_screenshot()
        self.quit()

    def msow(self):
        self.remove_headless()
        self.go_to_url("https://msonetprod.ahss.org/psv/credverification.aspx")
        self.enter_text_by_id("Raxwal", 'txtPractitionerName')
        self.enter_text_by_id("6449", 'txtNPI')
        self.select_from_dropdown_by_id("AdventHealth North Pinellas", 'dbcFacCode')
        self.click_button_by_xpath_javascript('//*[@id="btnSubmit"]')
        self.click_button_by_xpath_javascript('//*[@id="dgPractList"]/tbody/tr[2]/td[3]/a')
        new_window_handle = self.driver.window_handles[-1]
        self.driver.switch_to.window(new_window_handle)
        time.sleep(17)
        return self.take_screenshot()

    def mdquery(self):
        self.remove_headless()
        self.go_to_url("https://www.mdquery.com/app/login.aspx?ID=d725ac9e-f7e2-4546-9391-72d5256e7d85")
        self.enter_text_by_id("Credentialing", "YourName")
        self.enter_text_by_xpath("Access Health Care Physicians",
                                 "/html/body/form/div[5]/div[1]/div[1]/div/div/div/div[4]/div/input")
        self.enter_text_by_xpath("credentialing@accesshealthcarellc.net",
                                 "/html/body/form/div[5]/div[1]/div[1]/div/div/div/div[10]/div/input")
        self.click_button_by_xpath('//*[@id="Agree"]')
        self.enter_text_by_id("bayfront", "Login_TextBox")
        self.enter_text_by_id("query", "Password_TextBox")
        self.click_button_by_xpath('//*[@id="Login_Button"]')
        self.enter_text_by_id('1811250913', 'NPI_TextBox')
        self.click_button_by_xpath('//*[@id="Search_Button"]')
        self.click_button_by_xpath('//*[@id="SearchResultsV4_GridView"]/tbody/tr/td[1]/a')
        new_window_handle = self.driver.window_handles[-1]
        self.driver.switch_to.window(new_window_handle)
        time.sleep(5)
        return self.take_screenshot()
        self.quit()