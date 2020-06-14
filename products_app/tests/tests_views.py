from django.test import TestCase
from django.test import Client
from products_app.models import *


class ProductAppTest(TestCase):

    def setUp(self):
        self.category = Category.objects.create(name='boissons')
        self.julien = User.objects.create_user("julien", "julien@test.fr", "password")
        self.eau = Product.objects.create(id=1, name='eau', nutriscore='a', url='www.eau.com',
                                          image_url='www.linktojpg', category=self.category)
        self.eau.favorite_of.add(self.julien)
        self.category.save(), self.eau.save(), self.julien.save()

    def test_home_view(self):
        response = self.client.get('/')
        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

    def test_result_view(self):
        response = self.client.get('/products_app/result/?query=eau')
        self.assertEqual(response.status_code, 200)

    def test_product_page_view(self):
        response = self.client.get('/products_app/product_number/1/')
        self.assertEqual(response.status_code, 200)

    def test_product_saved_unauthenticated_user_view(self):
        response = self.client.get('/products_app/product_save/')
        self.assertEqual(response.status_code, 302)

    def test_home_authenticated_user(self):
        c = Client()
        c.login(username="julien", password="password")
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_home_unauthenticated_user(self):
        c = Client()
        c.login(username="julien", password="password")
        c.logout()
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_login(self):
        response = self.client.get('/accounts/login/')
        self.assertEqual(response.status_code, 200)

    def test_login_authenticated(self):
        self.client.login(username="julien", password="password")
        response = self.client.get('/accounts/login/')
        self.assertEqual(response.status_code, 200)

    def test_logout(self):
        self.client.login(username="julien", password="password")
        self.client.logout()
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_signup(self):
        response = self.client.get('/accounts/signup/')
        self.assertEqual(response.status_code, 200)

    def test_favorites(self):
        c = Client()
        c.login(username="julien", password="password")
        response = c.get('/products_app/favorites/', follow=True)
        print(response.redirect_chain)
        self.assertEqual(response.status_code, 200)

    def test_page_product(self):
        response = self.client.get('/products_app/product_number/1/')
        self.assertEqual(response.status_code, 200)

    def test_user_connection(self):
        c = Client()
        response = c.get('/accounts/login/')
        self.assertEqual(response.status_code, 200)
        self.client.login(username="julien", password="password")
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    """ test for news functionalities """

    def test_user_authenticated_change_password(self):
        c = Client()
        c.login(username="julien", password="password")
        response = self.client.get('/accounts/password_change/', follow=True)
        self.assertEqual(response.status_code, 200)

    def test_user_unauthenticated_change_password(self):
        response = self.client.get('/accounts/password_change/')
        self.assertEqual(response.status_code, 302)

    def test_favorite_button_del(self, nb_of_buttons=1):
        c = Client()
        c.login(username="julien", password="password")
        response = c.get('/products_app/favorites/', follow=True)
        print(response.redirect_chain)
        self.assertEqual(response.status_code, 200)
        print(response.content)
        self.assertContains(response, "Supprimer", count=nb_of_buttons)
