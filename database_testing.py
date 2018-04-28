#! /usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import unittest

chromeLocation = "/Users/joe/Downloads/chromedriver"
siteURL = "localhost:7777"

class checkInjection(unittest.TestCase):
	@classmethod
	def setUp(self):
		self.driver = webdriver.Chrome(chromeLocation)
		self.driver.get(siteURL)

	# attempts SQL injection attack
	def testInjectSQLTestA(self):
		self.elem = self.driver.find_element_by_name("username")
		self.elem.send_keys("joe'); DROP TABLE login")
		self.elem = self.driver.find_element_by_name("password")
		self.elem.send_keys("BLAH")
		self.elem = self.driver.find_element_by_xpath("/html/body/form/div[2]/button")
		self.elem.click()

		self.assertEqual(self.driver.current_url, "http://localhost:7777/login")

	@classmethod
	def tearDown(self):
		self.driver.quit()

class inputValidationChecking(unittest.TestCase):
	@classmethod
	def setUp(self):
		self.driver = webdriver.Chrome(chromeLocation)
		self.driver.get(siteURL)

	# because of email validation, doesnt work
	def testCreateUserValid(self):
		# Fills in signup options to test inputs
		self.elem = self.driver.find_element_by_link_text("Sign Up")
		self.elem.click()
		self.elem = self.driver.find_element_by_name("email")
		self.elem.send_keys("email@email.com")
		self.elem = self.driver.find_element_by_name("firstName")
		self.elem.send_keys("Timmy")
		self.elem = self.driver.find_element_by_name("lastName")
		self.elem.send_keys("Little")
		self.elem = self.driver.find_element_by_name("type")
		self.elem.click()
		self.elem = self.driver.find_element_by_name("password")
		self.elem.send_keys("password")
		self.elem = self.driver.find_element_by_name("psw2")
		self.elem.send_keys("password")
		time.sleep(2)
		self.elem.send_keys(Keys.ENTER)
		self.assertEqual(self.driver.current_url, "http://localhost:7777/courses")

	def testEmailValidation(self):
		pass

	def testCreateUserInvalid(self):
		pass

	@classmethod
	def tearDown(self):
		self.driver.close()

class normalFunctions(unittest.TestCase):
	@classmethod
	def setUp(self):
		self.driver = webdriver.Chrome(chromeLocation)
		self.driver.get(siteURL)

	def testNormalSignIn(self):
		self.elem = self.driver.find_element_by_name("username")
		self.elem.send_keys("carneyjs@gmail.com")
		self.elem = self.driver.find_element_by_name("password")
		self.elem.send_keys("password")
		self.elem = self.driver.find_element_by_tag_name("button")
		self.elem.click()
		self.assertEqual(self.driver.current_url, "http://localhost:7777/courses")

	@classmethod
	def tearDown(self):
		self.driver.close()

class testSandboxFunctionality(unittest.TestCase):
	@classmethod
	def setUp(self):
		# Get to the sandbox page
		self.driver = webdriver.Chrome(chromeLocation)
		self.driver.get(siteURL)
		self.elem = self.driver.find_element_by_name("username")
		self.elem.send_keys("carneyjs@gmail.com")
		self.elem = self.driver.find_element_by_name("password")
		self.elem.send_keys("password")
		self.elem = self.driver.find_element_by_tag_name("button")
		self.elem.click()
		self.elem = self.driver.find_element_by_id("sandbox")
		self.elem.click()

	def testSandboxNormal(self):
		self.elem = self.driver.find_element_by_name("code")
		self.elem.send_keys("#include <iostream>").send_keys(Keys.ENTER)
		self.elem.send_keys("using namespace std;").send_keys(Keys.ENTER)
		self.elem.send_keys(Keys.ENTER)
		self.elem.send_keys("int main() {").send_keys(Keys.ENTER)
		self.elem.send_keys("cout << 'hello world!' << endl;").send_keys(Keys.ENTER)
		self.elem.send_keys("return 0;").send_keys(Keys.ENTER)
		self.elem.send_keys("}").send_keys(Keys.ENTER)
		self.elem = self.driver.find_element_by_link_text("Compile")
		self.elem.click()
		time.sleep(6)
		self.elem = self.driver.find_element_by_link_text("Run")
		self.elem.click()
		time.sleep(6)
		self.assertTrue(self.driver.find_element_by_name("output").text == 'hello world')

	def testSandboxSystem(self):
		pass

	@classmethod
	def tearDown(self):
		self.driver.close()

if __name__ == "__main__":
	print("Welcome to GLaDOS")
	unittest.main()
