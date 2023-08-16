import json

from django.test import Client, TestCase

# Create your tests here.
from django.urls import reverse

from .models import Task


class TaskViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.todo1 = Task.objects.create(title="Task 1")
        self.todo2 = Task.objects.create(title="Task 2")

    def test_list_todos(self):
        response = self.client.get(reverse("TodosListView"))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data), 2)  # Assuming there are 2 tasks in the database

    def test_create_todo(self):
        response = self.client.post(
            reverse("TodosListView"),
            data=json.dumps({"title": "New Task"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.content)
        self.assertEqual(data["title"], "New Task")

    def test_create_todo_invalid_title(self):
        response = self.client.post(
            reverse("TodosListView"),
            data=json.dumps({"title": 123}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)

    def test_create_todo_empty_title(self):
        response = self.client.post(
            reverse("TodosListView"),
            data=json.dumps({"title": ""}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)

    def test_retrieve_todo(self):
        response = self.client.get(reverse("TodosDetailsView", args=[self.todo1.pk]))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data["fields"]["title"], self.todo1.title)

    def test_retrieve_nonexistent_todo(self):
        response = self.client.get(
            reverse("TodosDetailsView", args=[1000])
        )  # Assuming 1000 doesn't exist in the database
        self.assertEqual(response.status_code, 404)

    def test_update_todo(self):
        response = self.client.put(
            reverse("TodosDetailsView", args=[self.todo1.pk]),
            data=json.dumps({"title": "Updated Task"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data["title"], "Updated Task")

    def test_update_todo_invalid_title(self):
        response = self.client.put(
            reverse("TodosDetailsView", args=[self.todo1.pk]),
            data=json.dumps({"title": 123}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)

    def test_update_todo_empty_title(self):
        response = self.client.put(
            reverse("TodosDetailsView", args=[self.todo1.pk]),
            data=json.dumps({"title": ""}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)

    def test_update_nonexistent_todo(self):
        response = self.client.put(
            reverse("TodosDetailsView", args=[1000]),
            data=json.dumps({"title": "Updated Task"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 404)

    def test_delete_todo(self):
        response = self.client.delete(reverse("TodosDetailsView", args=[self.todo1.pk]))
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Task.objects.filter(pk=self.todo1.pk).exists())

    def test_delete_nonexistent_todo(self):
        response = self.client.delete(reverse("TodosDetailsView", args=[1000]))
        self.assertEqual(response.status_code, 404)
