from datetime import date, datetime, timedelta

from django.contrib.auth import get_user_model
from django.conf import settings
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from main.models import Category, Task

User = get_user_model()


class TestTask(APITestCase):
    """ Test task. """

    URL = '/api/v1/tasks/'
    OBJECT_URL = '/api/v1/tasks/{0}/'

    @classmethod
    def setUpClass(cls) -> None:
        super(TestTask, cls).setUpClass()
        cls.first_user = User.objects.create_user(
            username='first_test_user',
        )
        cls.second_user = User.objects.create_user(
            username='second_test_user',
        )
        cls.first_category = Category.objects.create(
            name='Первая категория',
        )
        cls.second_category = Category.objects.create(
            name='Вторая категория',
        )
        cls.first_task = Task.objects.create(
            title='API',
            description='Нужно написать сериализаторы для api.',
            due_date=date.today(),
            category=cls.first_category,
            user=cls.first_user,
        )
        cls.second_task = Task.objects.create(
            title='Тесты',
            description='Нужно написать тесты для проверки работы тасков.',
            due_date=date.today(),
            category=cls.second_category,
            user=cls.first_user,
        )
        cls.third_task = Task.objects.create(
            title='Модели',
            description='Закончить писать модель Task.',
            due_date=date.today(),
            category=cls.first_category,
            user=cls.second_user,
        )

    def setUp(self) -> None:
        self.guest_client = APIClient()

        self.authorized_client = APIClient()
        token = RefreshToken.for_user(self.first_user)
        self.authorized_client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {str(token.access_token)}'
        )

    def test_get_tasks_list_by_guest(self):
        response = self.guest_client.get(self.URL)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_tasks_list_by_authorized(self):
        tasks_count = Task.objects.filter(user=self.first_user).count()
        response = self.authorized_client.get(self.URL)
        expected_keys = ['count', 'next', 'previous', 'results']

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(list(response.json().keys()), expected_keys)
        self.assertEqual(response.json()['count'], tasks_count)

    def test_put_patch_delete_task_by_guest(self):
        methods = ['put', 'patch', 'delete']

        for method in methods:
            met = getattr(self.guest_client, method)
            response = met(self.OBJECT_URL.format(self.first_task.id))

            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_put_patch_delete_task_by_another_client(self):
        methods = ['put', 'patch', 'delete']

        for method in methods:
            met = getattr(self.authorized_client, method)
            response = met(self.OBJECT_URL.format(self.third_task.id))

            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_put_patch_task_by_user(self):
        target_date = date.today() + timedelta(days=1)
        method_data = {
            'put': {
                'title': 'TEST',
                'description': 'Test description',
                'due_date': target_date,
                'category': self.second_category.id,
            },
            'patch': {
                'title': 'New title',
            }
        }

        for method, data in method_data.items():
            met = getattr(self.authorized_client, method)
            response = met(
                self.OBJECT_URL.format(self.first_task.id),
                data=data,
            )
            task = Task.objects.get(id=self.first_task.id)
            response_json = response.json()

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEquals(
                [
                    task.id,
                    task.title,
                    task.description,
                    str(task.created_at),
                    str(task.due_date),
                    task.category.id,
                ],
                [
                    response_json['id'],
                    response_json['title'],
                    response_json['description'],
                    response_json['created_at'],
                    response_json['due_date'],
                    response_json['category']['id'],
                ]
            )

    def test_validate_due_date(self):
        task_count = Task.objects.filter(user=self.first_user).count()
        target_date = date.today() - timedelta(days=1)
        data = {
            'title': 'New task',
            'description': 'New task description',
            'due_date': target_date,
            'category': self.second_category.id,
        }
        response = self.authorized_client.post(self.URL, data=data)
        expected_error = {
            'due_date': ['Дата окончания задачи не может быть меньше текущей.']
        }

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), expected_error)
        self.assertEqual(
            Task.objects.filter(user=self.first_user).count(),
            task_count
        )

    def test_upload_file(self):
        file_path = 'api/tests/file.txt'
        full_path = settings.BASE_DIR / file_path
        target_date = date.today() + timedelta(days=1)
        with open(full_path, 'r') as file:
            data = {
                'title': 'New task',
                'description': 'New task description',
                'due_date': target_date,
                'category': self.second_category.id,
                'file': file
            }
            response = self.authorized_client.post(self.URL, data=data)
            response_json = response.json()
            task = Task.objects.filter(
                id=response_json['id'],
                title=response_json['title'],
                description=response_json['description'],
                created_at=response_json['created_at'],
                due_date=response_json['due_date'],
                category__id=response_json['category']['id'],
            )

            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertTrue(task.exists())
            self.assertTrue(task.first().file)
