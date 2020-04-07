import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class PurBeurreTest(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()

    def test_login(self, username="leonardo37", password="davinci37"):
        driver = self.driver
        driver.get("http://127.0.0.1:8000/accounts/login/")
        self.assertIn("Pur Beurre", driver.title)
        elem = driver.find_element_by_name("username")
        elem.send_keys(username)
        elem1 = driver.find_element_by_name("password")
        elem1.send_keys(password)
        elem.send_keys(Keys.RETURN)
        assert "Please enter a correct username and password." not in driver.page_source
        driver.implicitly_wait(3)  # seconds
        logout_img = driver.find_element_by_id("logout").is_displayed()  # check if logout img is displayed
        if logout_img:
            print("the logout image is correctly displayed")

    def test_redirection_login_to_saved_product(self):
        driver = self.driver
        driver.get("http://127.0.0.1:8000/")
        self.assertIn("Pur Beurre", driver.title)
        elem = driver.find_element_by_name("query")
        elem.send_keys("eau")
        elem.send_keys(Keys.RETURN)
        driver.implicitly_wait(1)  # seconds
        button = driver.find_element_by_name("button_id_3977")
        button.send_keys(Keys.RETURN)
        elem_to_check = driver.find_element_by_id("login")
        message = elem_to_check.text
        assert "Login" in message

    def test_search(self, product_in_db="eau"):
        driver = self.driver
        driver.get("http://127.0.0.1:8000/")
        self.assertIn("Pur Beurre", driver.title)
        elem = driver.find_element_by_name("query")
        elem.send_keys(product_in_db)
        elem.send_keys(Keys.RETURN)
        assert "Votre produit n'existe pas dans notre base de données !" not in driver.page_source

    def test_search_with_empty_query(self):
        driver = self.driver
        driver.get("http://127.0.0.1:8000/")
        self.assertIn("Pur Beurre", driver.title)
        elem = driver.find_element_by_name("query")
        elem.send_keys("")
        elem.send_keys(Keys.RETURN)
        driver.implicitly_wait(2)  # seconds
        elem_to_check = driver.find_element_by_id("message_to_display")
        message = elem_to_check.text
        assert "Votre saisie est vide !" in message

    def test_search_with_nonsense_query(self):
        driver = self.driver
        driver.get("http://127.0.0.1:8000/")
        self.assertIn("Pur Beurre", driver.title)
        elem = driver.find_element_by_name("query")
        elem.send_keys("blabla")
        elem.send_keys(Keys.RETURN)
        driver.implicitly_wait(2)  # seconds
        elem_to_check = driver.find_element_by_id("message_to_display")
        message = elem_to_check.text
        assert "Votre produit n'existe pas dans notre base de donnée !" in message

    def test_change_password(self, username="leonardo37", password="davinci37"):
        driver = self.driver
        driver.get("http://127.0.0.1:8000/accounts/login/")
        elem = driver.find_element_by_name("username")
        elem.send_keys(username)
        elem1 = driver.find_element_by_name("password")
        elem1.send_keys(password)
        elem.send_keys(Keys.RETURN)
        driver.implicitly_wait(1)  # seconds
        to_user_account = driver.find_element_by_id("link_to_user_account")
        to_user_account.send_keys(Keys.RETURN)
        driver.implicitly_wait(1)  # seconds
        to_change_password = driver.find_element_by_id("link_change_password")
        to_change_password.send_keys(Keys.RETURN)
        driver.implicitly_wait(1)
        elem_to_check = driver.find_element_by_id("change_password_title")
        message = elem_to_check.text
        assert "Change your password" in message

    def tearDown(self):
        self.driver.close()


if __name__ == '__main__':
    unittest.main()
