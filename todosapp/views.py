import json

# Create your views here.
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

# from .utils import
from .models import Task


@method_decorator(csrf_exempt, name="dispatch")
class TodosListView(View):
    """class based view to handle list view of todos"""

    def get(self, request):
        """Handle get request to get all todos"""
        tasks = Task.objects.all()
        tasksList = [
            {
                "id": task.id,
                "title": task.title,
                "created_at": task.created_at.isoformat(),
                "updated_at": task.updated_at.isoformat(),
            }
            for task in tasks
        ]
        return JsonResponse(tasksList, safe=False, status=200)

    def post(self, request):
        """Handle post request to add todo"""
        try:
            # title = self.request.POST.get("title")
            request_data = json.loads(request.body)
            title = request_data.get("title")
            if title is None:
                return JsonResponse({"Error": "title is required"}, status=400)
            elif isinstance(title, str) is False:
                return JsonResponse(
                    {"Error": f"title must be of type string."},
                    status=400,
                )
            elif len(title) == 0:
                return JsonResponse(
                    {"Error": "title can't be empty string"}, status=400
                )
            else:
                task = Task.objects.create(title=title)
                return JsonResponse({"id": task.id, "title": task.title}, status=201)

        except Exception as e:
            return JsonResponse(f"Invalid JSON data: {e}.", status=400, safe=False)


@method_decorator(csrf_exempt, name="dispatch")
class TodosDetailsView(View):
    """class based view to handle details view of on todo"""

    def get(self, request, pk):
        """Handle get request to get one todo by ID"""
        task = get_object_or_404(Task, pk=pk)
        return JsonResponse(
            {
                "id": task.id,
                "title": task.title,
                "created_at": task.created_at.isoformat(),
                "updated_at": task.updated_at.isoformat(),
            },
            status=200,
        )

    def put(self, request, pk):
        """Handle put request to update one todo by ID"""
        try:
            # title = self.request.POST.get("title")
            request_data = json.loads(request.body)
            title = request_data.get("title")
            task = get_object_or_404(Task, pk=pk)
            if title is None:
                return JsonResponse({"Error": "title is required"}, status=400)
            elif isinstance(title, str) is False:
                return JsonResponse(
                    {"Error": "title must be of type string"}, status=400
                )
            elif title and len(title) == 0:
                return JsonResponse(
                    {"Error": "title can't be empty string"}, status=400
                )
            else:
                task.title = title
                task.save()
                return JsonResponse({"id": task.id, "title": task.title}, status=200)
        except Exception as e:
            return JsonResponse(f"Invalid JSON data: {e}.", status=400, safe=False)

    def delete(self, request, pk):
        """Handle delete request to remove one todo by ID'"""
        task = get_object_or_404(Task, pk=pk)
        task.delete()
        return JsonResponse({"message": "Task deleted successfully."}, status=204)
