import json

from django.core import serializers

from .models import Task


def validate_title(title):
    """Validate title"""
    if title is None:
        return {"Error": "title is required"}
    elif not isinstance(title, str):
        return {"Error": "title must be of type string"}
    elif len(title) == 0:
        return {"Error": "title can't be an empty string"}
    return None


def task_serializer(tasks):
    """Serialize tasks to json
    argument : tasks must be iterable, ideally a list
    """
    serialized_data = serializers.serialize("json", tasks)
    return json.loads(serialized_data)


# Manual serializer using django core
# class TaskSerializer(serializers.BaseSerializer):

#     def to_representation(self, instance):
#         if isinstance(instance, list):
#             serialized_data = []
#             for item in instance:
#                 serialized_data.append(self.serialize_task(item))
#             return serialized_data
#         else:
#             return self.serialize_task(instance)

#     def serialize_task(self, task):
#         return {
#             "id": task.id,
#             "title": task.title,
#             "created_at": task.created_at.isoformat(),
#             "updated_at": task.updated_at.isoformat(),
#         }
