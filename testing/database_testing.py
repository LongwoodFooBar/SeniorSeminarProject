#! /usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
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
		# assertion
		self.assertEqual(self.driver.current_url, "http://localhost:7777/login")

	@classmethod
	def tearDown(self):
		self.driver.quit()

class inputValidationChecking(unittest.TestCase):
	@classmethod
	def setUp(self):
		self.driver = webdriver.Chrome(chromeLocation)
		self.driver.get(siteURL)
		self.elem = self.driver.find_element_by_link_text("Sign Up")
		self.elem.click()

	def testCreateUserValid(self):
		# Fills in signup options to test inputs
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
		
		self.elem = Select(self.driver.find_element_by_name("securityQuestion"))
		self.elem.select_by_index[0]
		self.elem = self.driver.find_element_by_name("answer")
		self.elem.send_keys("Momma Harp")
		self.elem = driver.driver.find_element_by_name("signupButton")
		self.elem.click()

		time.sleep(2)
		self.elem.send_keys(Keys.ENTER)
		#assertion
		self.assertEqual(self.driver.current_url, "http://localhost:7777/courses")

	def testEmailValidationDot(self):
		# Fills in signup options to test inputs
		self.elem = self.driver.find_element_by_name("email")
		self.elem.send_keys("email@emailcom")
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
		
		self.elem = Select(self.driver.find_element_by_name("securityQuestion"))
		self.elem.select_by_index[0]
		self.elem = self.driver.find_element_by_name("answer")
		self.elem.send_keys("Momma Harp")
		self.elem = driver.driver.find_element_by_name("signupButton")
		self.elem.click()

		self.assertEqual(self.driver.current_url, "http://localhost:7777/signup")

	def testEmailValidationAt(self):
		# Fills in signup options to test inputs
		self.elem = self.driver.find_element_by_name("email")
		self.elem.send_keys("emailemail.com")
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

		self.elem = Select(self.driver.find_element_by_name("securityQuestion"))
		self.elem.select_by_index[0]
		self.elem = self.driver.find_element_by_name("answer")
		self.elem.send_keys("Momma Harp")
		self.elem = self.driver.find_element_by_name("signupButton")
		self.elem.click()

		self.assertEqual(self.driver.current_url, "http://localhost:7777/signup")

	def testPasswordLength(self):
		# Fills in signup options to test inputs
		self.elem = self.driver.find_element_by_name("email")
		self.elem.send_keys("email@email.com")
		self.elem = self.driver.find_element_by_name("firstName")
		self.elem.send_keys("Timmy")
		self.elem = self.driver.find_element_by_name("lastName")
		self.elem.send_keys("Little")
		self.elem = self.driver.find_element_by_name("type")
		self.elem.click()
		self.elem = self.driver.find_element_by_name("password")
		self.elem.send_keys("passwor")
		self.elem = self.driver.find_element_by_name("psw2")
		self.elem.send_keys("passwor")

		self.elem = Select(self.driver.find_element_by_name("securityQuestion"))
		self.elem.select_by_index[0]
		self.elem = self.driver.find_element_by_name("answer")
		self.elem.send_keys("Momma Harp")
		self.elem = self.driver.find_element_by_name("signupButton")
		self.elem.click()

		self.assertEqual(self.driver.current_url, "http://localhost:7777/signup")

	def testPasswordTypePunct(self):
		# Fills in signup options to test inputs
		self.elem = self.driver.find_element_by_name("email")
		self.elem.send_keys("email@email.com")
		self.elem = self.driver.find_element_by_name("firstName")
		self.elem.send_keys("Timmy")
		self.elem = self.driver.find_element_by_name("lastName")
		self.elem.send_keys("Little")
		self.elem = self.driver.find_element_by_name("type")
		self.elem.click()
		self.elem = self.driver.find_element_by_name("password")
		self.elem.send_keys("password!")
		self.elem = self.driver.find_element_by_name("psw2")
		self.elem.send_keys("password!")

		self.elem = Select(self.driver.find_element_by_name("securityQuestion"))
		self.elem.select_by_index[0]
		self.elem = self.driver.find_element_by_name("answer")
		self.elem.send_keys("Momma Harp")
		self.elem = self.driver.find_element_by_name("signupButton")
		self.elem.click()

		self.assertEqual(self.driver.current_url, "http://localhost:7777/signup")

	def testPasswordTypeSpace(self):
		# Fills in signup options to test inputs
		self.elem = self.driver.find_element_by_name("email")
		self.elem.send_keys("email@email.com")
		self.elem = self.driver.find_element_by_name("firstName")
		self.elem.send_keys("Timmy")
		self.elem = self.driver.find_element_by_name("lastName")
		self.elem.send_keys("Little")
		self.elem = self.driver.find_element_by_name("type")
		self.elem.click()
		self.elem = self.driver.find_element_by_name("password")
		self.elem.send_keys("pass word")
		self.elem = self.driver.find_element_by_name("psw2")
		self.elem.send_keys("pass word")

		self.elem = Select(self.driver.find_element_by_name("securityQuestion"))
		self.elem.select_by_index[0]
		self.elem = self.driver.find_element_by_name("answer")
		self.elem.send_keys("Momma Harp")
		self.elem = self.driver.find_element_by_name("signupButton")
		self.elem.click()

		self.assertEqual(self.driver.current_url, "http://localhost:7777/signup")

	def TestPasswordMatch(self):
		# Fills in signup options to test inputs
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
		self.elem.send_keys("passwrod")

		self.elem = Select(self.driver.find_element_by_name("securityQuestion"))
		self.elem.select_by_index[0]
		self.elem = self.driver.find_element_by_name("answer")
		self.elem.send_keys("Momma Harp")
		self.elem = self.driver.find_element_by_name("signupButton")
		self.elem.click()

		self.assertEqual(self.driver.current_url, "http://localhost:7777/signup")

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
		self.elem.send_keys("jacobsc@gmail.com")
		self.elem = self.driver.find_element_by_name("password")
		self.elem.send_keys("password")
		self.elem = self.driver.find_element_by_tag_name("button")
		self.elem.click()
		#assertion
		self.assertEqual(self.driver.current_url, "http://localhost:7777/courses")

	def testNormalAssignment(self):
		pass

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
		self.elem.send_keys("jacobsc@gmail.com")
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
		#assertion
		self.assertTrue(self.driver.find_element_by_name("output").text == 'hello world')

	def testSandboxSystem(self):
		self.elem = self.driver.find_element_by_name("code")
		self.elem.send_keys("#include <iostream>").send_keys(Keys.ENTER)
		self.elem.send_keys("using namespace std;").send_keys(Keys.ENTER)
		self.elem.send_keys(Keys.ENTER)
		self.elem.send_keys("int main() {").send_keys(Keys.ENTER)
		self.elem.send_keys("system('ls -l')").send_keys(Keys.ENTER)
		self.elem.send_keys("return 0;").send_keys(Keys.ENTER)
		self.elem.send_keys("}").send_keys(Keys.ENTER)
		self.elem = self.driver.find_element_by_link_text("Compile")
		self.elem.click()
		time.sleep(6)
		self.elem = self.driver.find_element_by_link_text("Run")
		self.elem.click()
		time.sleep(6)
		#assertion
		self.assertTrue(self.driver.find_element_by_name("output").text == "")

	@classmethod
	def tearDown(self):
		self.driver.close()

if __name__ == "__main__":
	print("Welcome to GLaDOS")
	unittest.main()
