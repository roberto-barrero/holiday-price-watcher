from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from functools import wraps
import time
import calendar


def execution_logger(func):
	@wraps(func)
	def wrapper(*args, **kwargs):
		print(f"Start: {func.__name__}")
		result = func(*args, **kwargs)
		print(f"End: {func.__name__}")
		return result
	return wrapper


class ExpediaScraper:
	def __init__(self):
		self.driver = webdriver.Chrome(
			service=Service(ChromeDriverManager().install()))
		self.wait = WebDriverWait(self.driver, 10)
		self.driver.maximize_window()

	@execution_logger
	def get_section_tabs(self):
		self.wait.until(EC.presence_of_element_located(
			(By.CSS_SELECTOR, "div.uitk-tabs-container")))
		tabs_container = self.driver.find_element(
			By.CSS_SELECTOR, "div.uitk-tabs-container > ul")
		tabs_elements = tabs_container.find_elements(By.TAG_NAME, "li")
		tabs = {}
		for tab in tabs_elements:
			tab_name = tab.text
			tabs[tab_name] = tab
		return tabs

	@execution_logger
	def open_expedia(self):
		self.driver.get("https://www.expedia.mx")
		self.wait.until(EC.presence_of_element_located(
			(By.ID, "tab-hotel-tab-hp")))

	@execution_logger
	def search_hotels(self, destination, check_in, check_out):
		self.driver.find_element(By.ID, "tab-hotel-tab-hp").click()
		destination_input = self.driver.find_element(
			By.ID, "hotel-destination-hp-hotel")
		destination_input.clear()
		destination_input.send_keys(destination)
		check_in_input = self.driver.find_element(
			By.ID, "hotel-checkin-hp-hotel")
		check_in_input.clear()
		check_in_input.send_keys(check_in)
		check_out_input = self.driver.find_element(
			By.ID, "hotel-checkout-hp-hotel")
		check_out_input.clear()
		check_out_input.send_keys(check_out)
		check_out_input.send_keys(Keys.RETURN)

	@execution_logger
	def wait_for_user_interaction(self):
		input("Press Enter to continue after interacting with the browser...")

	@execution_logger
	def get_hotel_details(self):
		self.wait.until(EC.presence_of_element_located(
			(By.CLASS_NAME, "hotel")))
		hotels = self.driver.find_elements(By.CLASS_NAME, "hotel")
		hotel_details = []
		for hotel in hotels:
			name = hotel.find_element(By.CLASS_NAME, "hotel-name").text
			price = hotel.find_element(By.CLASS_NAME, "price").text
			hotel_details.append({"name": name, "price": price})
		return hotel_details

	@execution_logger
	def close(self):
		self.driver.quit()

	@execution_logger
	def get_section_tabs(self):
		self.wait.until(EC.presence_of_element_located(
			(By.CSS_SELECTOR, "div.uitk-tabs-container")))
		tabs_container = self.driver.find_element(
			By.CSS_SELECTOR, "div.uitk-tabs-container > ul")
		tabs_elements = tabs_container.find_elements(By.TAG_NAME, "li")
		tabs = {}
		for tab in tabs_elements:
			tab_name = tab.text
			tabs[tab_name] = tab
		self.tabs = tabs
		return tabs

	@execution_logger
	def open_expedia(self):
		self.driver.get("https://www.expedia.mx")
		initial_wait = WebDriverWait(self.driver, 60)
		initial_wait.until(EC.presence_of_element_located(
			(By.ID, "app-lotus-home-ui")))

	def select_dates(self, start_date, end_date):
		dates_container_selector = (By.CSS_SELECTOR, "section.uitk-date-selector-popover")
		self.wait.until(EC.presence_of_element_located(dates_container_selector))
		dates_container = self.driver.find_element(*dates_container_selector)

		start_day, start_month, start_year = start_date.split("-")
		end_day, end_month, end_year = end_date.split("-")

		prev_month_btn_selector = (By.CSS_SELECTOR, "div.uitk-cal-controls-button-prev > button")
		next_month_btn_selector = (By.CSS_SELECTOR, "div.uitk-cal-controls-button-next > button")

		self.wait.until(EC.presence_of_element_located(prev_month_btn_selector))
		prev_month_btn = self.driver.find_element(*prev_month_btn_selector)
		self.wait.until(EC.presence_of_element_located(next_month_btn_selector))
		next_month_btn = self.driver.find_element(*next_month_btn_selector)

		left_datepicker_selector = (By.CSS_SELECTOR, "div.uitk-month.uitk-month-double.uitk-month-double-left")
		self.wait.until(EC.presence_of_element_located(left_datepicker_selector))
		left_datepicker = self.driver.find_element(*left_datepicker_selector)
		left_month_label = left_datepicker.find_element(By.CSS_SELECTOR, "span.uitk-month-label")
		print("start_month_label: ", left_month_label.text)

		# Navigate to the start month
		while calendar.month_name[int(start_month)] not in left_month_label.text and start_year not in left_month_label.text:
			if calendar.month_name[:].index(left_month_label.text.split(" ")[0]) > int(start_month):
				prev_month_btn.click()
			else:
				next_month_btn.click()
			self.wait.until(EC.presence_of_element_located(left_datepicker_selector))
			left_datepicker = self.driver.find_element(By.CSS_SELECTOR, "div.uitk-month.uitk-month-double.uitk-month-double-left")
			left_month_label = left_datepicker.find_element(By.CSS_SELECTOR, "span.uitk-month-label")
			print("start_month_label: ", left_month_label.text)

		dates_table = left_datepicker.find_element(By.TAG_NAME, "table")
		days = dates_table.find_elements(By.TAG_NAME, "td")

		for day in days:
			if day.text == str(int(start_day)):
				day.click()
				print("day clicked: ", day.text)
				break

		# Navigate to the end month
		while calendar.month_name[int(end_month)] not in left_month_label.text and end_year not in left_month_label.text:
			if calendar.month_name[:].index(left_month_label.text.split(" ")[0]) > int(end_month):
				prev_month_btn.click()
			else:
				next_month_btn.click()
			self.wait.until(EC.presence_of_element_located(left_datepicker_selector))
			left_datepicker = self.driver.find_element(By.CSS_SELECTOR, "div.uitk-month.uitk-month-double.uitk-month-double-left")
			left_month_label = left_datepicker.find_element(By.CSS_SELECTOR, "span.uitk-month-label")
			print("start_month_label: ", left_month_label.text)

		print("end_month_label: ", left_month_label.text)
		dates_table = left_datepicker.find_element(By.TAG_NAME, "table")
		days = dates_table.find_elements(By.TAG_NAME, "td")

		for day in days:
			if day.text == str(int(end_day)):
				day.click()
				print("day clicked: ", day.text)
				break

		# time.sleep(3)
		footer = dates_container.find_element(By.TAG_NAME, "footer")
		submit_btn = footer.find_element(By.TAG_NAME, "button")
		submit_btn.click()

		time.sleep(3)


		# months = self.driver.find_elements(By.CSS_SELECTOR, "div.uitk-new-date-picker-month")
		# for month in months:
		# 	month_name = month.find_element(By.CSS_SELECTOR, "h2").text
		# 	if month_name in dates:
		# 		days = month.find_elements(By.CSS_SELECTOR, "button.uitk-new-date-picker-day")
		# 		for day in days:
		# 			if day.text == dates[month_name]:
		# 				day.click()
		# 				break
		# 		break
	@execution_logger
	def search_packages(self, origin, destination, start_date, end_date, people, rooms):
		"""Search for packages in Expedia
		
		Args:
			origin (str): Origin location
			destination (str): Destination location
			start_date (str): Start date in format "dd-mm-YYYY"
			end_date (str): End date in format "dd-mm-YYYY"
			people (int): Number of people
			rooms (int): Number of rooms
			"""
		if 'Paquetes' in self.tabs:
			self.tabs['Paquetes'].click()
		else:
			raise Exception("Paquetes tab not found")
		
		# Origin selection
		origin_container_selector = (By.CSS_SELECTOR, "div.uitk-input-swapper-start-input")

		self.wait.until(EC.presence_of_element_located(origin_container_selector))

		origin_container = self.driver.find_element(*origin_container_selector)

		origin_input_btn = origin_container.find_element(By.TAG_NAME, "button")
		origin_input_btn.click()

		self.wait.until(EC.presence_of_element_located((By.ID, "origin_select")))
		origin_input = self.driver.find_element(By.ID, "origin_select")
		
		origin_input.click()
		origin_input.send_keys(origin)
		origin_input.send_keys(Keys.RETURN)

		# Destination selection

		destination_container_selector = (By.CSS_SELECTOR, "div.uitk-input-swapper-end-input")
		self.wait.until(EC.presence_of_element_located(destination_container_selector))
		destination_container = self.driver.find_element(*destination_container_selector)

		destination_input_btn = destination_container.find_element(By.TAG_NAME, "button")
		destination_input_btn.click()


		self.wait.until(EC.presence_of_element_located((By.ID, "destination_select")))
		destination_input = self.driver.find_element(By.ID, "destination_select")

		destination_input.click()
		destination_input.send_keys(destination)
		destination_input.send_keys(Keys.RETURN)

		dates_btn_selector = (By.NAME, "EGDSDateRange-date-selector-trigger")
		self.wait.until(EC.presence_of_element_located(dates_btn_selector))
		self.driver.find_element(*dates_btn_selector).click()
		self.select_dates(start_date, end_date)

		search_btn = self.driver.find_element(By.ID, "search_button")
		search_btn.click()

		self.wait_for_user_interaction("Continue after confirming human validation...")

	@execution_logger
	def search_hotels(self, destination, check_in, check_out):
		if 'Hospedaje' in self.tabs:
			self.tabs['Hospedaje'].click()
		else:
			raise Exception("Hospedaje tab not found")
		destination_input = self.driver.find_element(
			By.ID, "hotel-destination-hp-hotel")
		destination_input.clear()
		destination_input.send_keys(destination)
		check_in_input = self.driver.find_element(
			By.ID, "hotel-checkin-hp-hotel")
		check_in_input.clear()
		check_in_input.send_keys(check_in)
		check_out_input = self.driver.find_element(
			By.ID, "hotel-checkout-hp-hotel")
		check_out_input.clear()
		check_out_input.send_keys(check_out)
		check_out_input.send_keys(Keys.RETURN)

	@execution_logger
	def wait_for_user_interaction(self, message="Press Enter to continue after interacting with the browser..."):
		input(message)

	@execution_logger
	def get_hotel_details(self):
		self.wait.until(EC.presence_of_element_located(
			(By.CLASS_NAME, "hotel")))
		hotels = self.driver.find_elements(By.CLASS_NAME, "hotel")
		hotel_details = []
		for hotel in hotels:
			name = hotel.find_element(By.CLASS_NAME, "hotel-name").text
			price = hotel.find_element(By.CLASS_NAME, "price").text
			hotel_details.append({"name": name, "price": price})
		return hotel_details

	def close(self):
		self.driver.quit()
