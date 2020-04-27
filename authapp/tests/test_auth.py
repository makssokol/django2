from django.test import TestCase
from django.test.client import Client
from mainapp.models import ArtObject, ArtCategory
from django.core.management import call_command
from django.urls import reverse
from authapp.models import ArtShopUser
from django.contrib.auth import get_user_model
from artshop import settings


class TestUserManagement(TestCase):

    fixtures = ['mainapp.json', 'authapp.json']

    # @classmethod
    # def setUpClass(cls):
    #     cls.user_model = get_user_model()

    def setUp(self):
        self.client = Client()
        self.user_model = get_user_model()
        self.superuser = self.user_model.objects.create_superuser(
            'django2', 'django2@geekshop.local', 'geekbrains'
        )

        self.user = self.user_model.objects.create_user(
            'tarantino', 'tarantino@geekshop.local', 'geekbrains'
        )

        self.user_with__first_name = self.user_model.objects.create_user(
            'umaturman', 'umaturman@geekshop.local', 'geekbrains', first_name='Ума'
        )

    def test_user_not_logged(self):
        # главная без логина
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_anonymous)
        self.assertEqual(response.context['title'], 'Art Gallery Flame Art')
        self.assertNotContains(response, 'User', status_code=200)
        # self.assertNotIn('Пользователь', response.content.decode())

    def test_user_login(self):
        # данные пользователя
        self.client.login(username='tarantino', password='geekbrains')

        # логинимся
        response = self.client.get('/auth/login/')
        self.assertFalse(response.context['user'].is_anonymous)
        self.assertEqual(response.context['user'], self.user)

        # главная после логина
        response = self.client.get('/')
        self.assertContains(response, 'User', status_code=200)
        self.assertEqual(response.context['user'], self.user)
        # self.assertIn('Пользователь', response.content.decode())

    # @classmethod
    # def tearDownClass(cls):
    #     return super().tearDownClass()

    def test_basket_login_redirect(self):
        # без логина должен переадресовать
        response = self.client.get('/basket/')
        self.assertEqual(response.url, '/auth/login/?next=/basket/')
        self.assertEqual(response.status_code, 302)

        # с логином все должно быть хорошо
        self.client.login(username='tarantino', password='geekbrains')

        response = self.client.get('/basket/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context['basket']), [])
        self.assertEqual(response.request['PATH_INFO'], '/basket/')
        self.assertIn('Your basket, User', response.content.decode())

    def test_user_register(self):
        # логин без данных пользователя
        response = self.client.get('/auth/register/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['title'], 'registration')
        self.assertTrue(response.context['user'].is_anonymous)

        new_user_data = { 
            'username': 'samuel',
            'first_name': 'Сэмюэл',
            'last_name': 'Джексон',
            'password1': 'geekbrains',
            'password2': 'geekbrains',
            'email': 'sumuel@geekshop.local',
            'age': '21'}
 
        response = self.client.post('/auth/register/', data=new_user_data)
        self.assertEqual(response.status_code, 302)

        new_user = self.user_model.objects.get(username=new_user_data['username'])

        activation_url = f"{settings.DOMAIN_NAME}/auth/verify/{new_user_data['email']}/{new_user.activation_key}/"

        response = self.client.get(activation_url)
        self.assertEqual(response.status_code, 200)

        # данные нового пользователя
        self.client.login(username=new_user_data['username'], 
                          password=new_user_data['password1'])

        # логинимся
        response = self.client.get('/auth/login/')
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['user'].is_anonymous)

       # проверяем главную страницу
        response = self.client.get('/')
        self.assertContains(response, text=new_user_data['first_name'],
                           status_code=200)

    def test_user_wrong_register(self):
        new_user_data = {
            'username': 'teen',
            'first_name': 'Мэри',
            'last_name': 'Поппинс',
            'password1': 'geekbrains',
            'password2': 'geekbrains',
            'email': 'merypoppins@geekshop.local',
            'age': '17'}

        response = self.client.post('/auth/register/', data=new_user_data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'register_form', 'age', 
                             'Too young for such purchases')

    
