import json

from django.core import serializers

# Create your views here.
from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from .models import Task
from .utils import validate_title


@method_decorator(csrf_exempt, name="dispatch")
class TodosListView(View):
    """class based view to handle list view of todos"""

    def get(self, request):
        """Handle get request to get all todos"""
        tasks = Task.objects.all()
        tasks_serialized = serializers.serialize("json", tasks)
        tasks_json = json.loads(tasks_serialized)
        return JsonResponse(tasks_json, safe=False, status=200)

    def post(self, request):
        """Handle post request to add todo"""
        try:
            # title = self.request.POST.get("title")
            request_data = json.loads(request.body)
            title = request_data.get("title")
            validation_error = validate_title(title)
            if validation_error:
                return JsonResponse(validation_error, status=400)
            else:
                task = Task.objects.create(title=title)
                return JsonResponse({"id": task.id, "title": task.title}, status=201)

        except Exception as e:
            return JsonResponse(
                {"Error": f"Invalid JSON data: {e}"}, status=400, safe=False
            )


@method_decorator(csrf_exempt, name="dispatch")
class TodosDetailsView(View):
    """class based view to handle details view of on todo"""

    def get(self, request, pk):
        """Handle get request to get one todo by ID"""
        try:
            task = get_object_or_404(Task, pk=pk)
            task_serialized = serializers.serialize("json", [task])
            task_json = json.loads(task_serialized)
            return JsonResponse(task_json, safe=False, status=200)
        except Http404:
            return JsonResponse({"error": "Invalid Task ID"}, status=404)

    def put(self, request, pk):
        """Handle put request to update one todo by ID"""
        try:
            # title = self.request.POST.get("title")
            request_data = json.loads(request.body)
            title = request_data.get("title")
            task = get_object_or_404(Task, pk=pk)
            validation_error = validate_title(title)
            if validation_error:
                return JsonResponse(validation_error, status=400)
            else:
                task.title = title
                task.save()
                return JsonResponse({"id": task.id, "title": task.title}, status=200)
        except Http404:
            return JsonResponse({"error": "Invalid Task ID"}, status=404)
        except Exception as e:
            return JsonResponse(
                {"Error": f"Invalid JSON data: {e}"}, status=400, safe=False
            )

    def delete(self, request, pk):
        """Handle delete request to remove one todo by ID'"""
        try:
            task = get_object_or_404(Task, pk=pk)
            task.delete()
            return JsonResponse({"message": "Task deleted successfully."}, status=204)
        except Http404:
            return JsonResponse({"error": "Invalid Task ID"}, status=404)
