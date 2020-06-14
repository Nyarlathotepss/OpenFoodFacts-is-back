from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys
from products_app.models import User, Product, Category
from selenium.common.exceptions import NoSuchElementException


class MySeleniumTests(StaticLiveServerTestCase):

    def setUp(self):
        super(MySeleniumTests, self).setUp()
        self.selenium = WebDriver()
        self.user = User.objects.create_user(username='test', password='Test1234', email='test@test.com',
                                             is_active=True)
        self.category = Category.objects.create(name='boissons')
        self.category.save()
        self.product = Product.objects.create(id=1, name='coca', nutriscore='c', url='www.coca.com',
                                              image_url='www.linktojpg', category=self.category)
        self.product_alt = Product.objects.create(id=2, name='eau', nutriscore='a', url='www.eau.com',
                                                  image_url='www.linktojpg', category=self.category)
        self.user.save(), self.product.save(), self.product_alt.save()

    def tearDown(self):
        self.selenium.quit()
        super(MySeleniumTests, self).tearDown()

    def test_login(self, username="test", password="Test1234"):
        self.selenium.get('%s%s' % (self.live_server_url, "/accounts/login/"))
        self.selenium.implicitly_wait(1)
        self.selenium.find_element_by_id('logo').is_displayed()
        self.selenium.find_element_by_name("username").send_keys(username)
        self.selenium.find_element_by_name("password").send_keys(password)
        self.selenium.find_element_by_id("button_login").click()
        self.selenium.implicitly_wait(1)
        self.selenium.find_element_by_id("colette").is_displayed()
        self.selenium.implicitly_wait(1)  # seconds
        self.selenium.find_element_by_id("logout").is_displayed()  # check if logout img is displayed

    def test_search(self):
        self.selenium.get('%s%s' % (self.live_server_url, "/"))
        self.selenium.implicitly_wait(1)
        self.selenium.find_element_by_id('logo').is_displayed()
        my_search = self.selenium.find_element_by_name("query")
        my_search.send_keys("eau")
        my_search.send_keys(Keys.RETURN)
        self.selenium.implicitly_wait(1)  # seconds
        self.selenium.find_element_by_id('product_pick').is_displayed()

    def test_redirection_login_to_saved_product(self):
        self.selenium.get('%s%s' % (self.live_server_url, "/"))
        self.selenium.implicitly_wait(1)
        self.selenium.find_element_by_id('logo').is_displayed()
        my_search = self.selenium.find_element_by_name("query")
        my_search.send_keys("coca")
        my_search.send_keys(Keys.RETURN)
        self.selenium.implicitly_wait(1)  # seconds
        self.selenium.find_element_by_name("button_id_2").click()
        self.selenium.find_element_by_id("login").is_displayed()

    def test_search_with_empty_query(self):
        self.selenium.get('%s%s' % (self.live_server_url, "/"))
        self.selenium.implicitly_wait(1)
        self.selenium.find_element_by_id('logo').is_displayed()
        my_search = self.selenium.find_element_by_name("query")
        my_search.send_keys("")
        my_search.send_keys(Keys.RETURN)
        self.selenium.implicitly_wait(1)  # seconds
        element_to_check = self.selenium.find_element_by_id("message_to_display")
        message = element_to_check.text
        assert "Votre saisie est vide !" in message

    def test_search_with_nonsense_query(self):
        self.selenium.get('%s%s' % (self.live_server_url, "/"))
        self.selenium.implicitly_wait(1)
        self.selenium.find_element_by_id('logo').is_displayed()
        my_search = self.selenium.find_element_by_name("query")
        my_search.send_keys("blablabla")
        my_search.send_keys(Keys.RETURN)
        self.selenium.implicitly_wait(1)  # seconds
        element_to_check = self.selenium.find_element_by_id("message_to_display")
        message = element_to_check.text
        assert "Votre produit n'existe pas dans notre base de donnée !" in message

    def test_change_password(self, username="test", password="Test1234"):
        self.selenium.get('%s%s' % (self.live_server_url, "/accounts/login/"))
        self.selenium.find_element_by_name("username").send_keys(username)
        self.selenium.find_element_by_name("password").send_keys(password)
        self.selenium.find_element_by_id("button_login").click()
        self.selenium.implicitly_wait(1)  # seconds
        self.selenium.find_element_by_id("link_to_user_account").click()
        self.selenium.implicitly_wait(1)  # seconds
        self.selenium.find_element_by_id("link_change_password").click()
        self.selenium.implicitly_wait(1)
        self.selenium.find_element_by_id("change_password_title").is_displayed()

    def test_add_then_delete_favorite(self, username="test", password="Test1234", product_in_db="coca"):
        self.selenium.get('%s%s' % (self.live_server_url, "/accounts/login/"))
        self.selenium.find_element_by_name("username").send_keys(username)
        self.selenium.find_element_by_name("password").send_keys(password)
        self.selenium.find_element_by_id("button_login").click()
        self.selenium.implicitly_wait(1)  # seconds
        self.selenium.find_element_by_name("query").send_keys(product_in_db)
        self.selenium.find_element_by_name("query").send_keys(Keys.RETURN)
        self.selenium.implicitly_wait(1)  # seconds
        self.selenium.find_element_by_name("button_id_2").click()
        self.selenium.implicitly_wait(1)  # seconds
        self.selenium.find_element_by_id("go_to_home").click()
        self.selenium.implicitly_wait(1)  # seconds
        self.selenium.find_element_by_id("link_to_favorites").click()
        self.selenium.implicitly_wait(1)  # seconds
        self.selenium.find_element_by_name("button_id_2")
        self.selenium.find_element_by_name("button_id_2").click()
        self.selenium.implicitly_wait(1)  # seconds
        self.selenium.find_element_by_id("link_to_favorites").click()
        self.selenium.implicitly_wait(1)  # seconds
        with self.assertRaises(NoSuchElementException):   # Test raise exception for find_element of button
            self.selenium.find_element_by_name("button_id_2")
