from django.test import TestCase
from django.contrib.auth.models import User
from .models import Task
from django.utils import timezone

class TaskModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.task = Task.objects.create(
            user=self.user,
            content='Test task',
            category='Pessoal',
            priority='Média',
            due_date=timezone.now() + timezone.timedelta(days=1)
        )

    def test_task_creation(self):
        self.assertEqual(self.task.content, 'Test task')
        self.assertEqual(self.task.category, 'Pessoal')
        self.assertEqual(self.task.priority, 'Média')
        self.assertFalse(self.task.completed)

    def test_task_str_method(self):
        self.assertEqual(str(self.task), 'Test task')

from django.urls import reverse
from django.test import Client

class TaskViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')
        self.task = Task.objects.create(
            user=self.user,
            content='Test task',
            category='Pessoal',
            priority='Média',
            due_date=timezone.now() + timezone.timedelta(days=1)
        )

    def test_index_view(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test task')

    def test_add_task_view(self):
        response = self.client.post(reverse('add_task'), {
            'content': 'New test task',
            'category': 'Trabalho',
            'priority': 'Alta',
            'due_date': (timezone.now() + timezone.timedelta(days=2)).strftime('%Y-%m-%dT%H:%M')
        })
        self.assertEqual(response.status_code, 302)  # Redirecionamento após adicionar
        self.assertEqual(Task.objects.count(), 2)

    def test_edit_task_view(self):
        response = self.client.post(reverse('edit_task', args=[self.task.id]), {
            'content': 'Updated test task'
        })
        self.task.refresh_from_db()
        self.assertEqual(self.task.content, 'Updated test task')

    def test_complete_task_view(self):
        response = self.client.get(reverse('complete_task', args=[self.task.id]))
        self.task.refresh_from_db()
        self.assertTrue(self.task.completed)

    def test_delete_task_view(self):
        response = self.client.get(reverse('delete_task', args=[self.task.id]))
        self.assertEqual(response.status_code, 302)  # Redirecionamento após excluir
        self.assertEqual(Task.objects.count(), 0)
