from django.core.management.base import BaseCommand
from apps.content.models import Model
from apps.content.serializers import ModelCreateSerializer
import json
import os

FILE_PATH = os.path.join(os.path.dirname(__file__), "data", "model.jsonl")

def _parse_jsonl(path):
    data = []
    with open(path, 'r') as file:
        for line in file:
            try:
                data.append(json.loads(line))
            except json.JSONDecodeError as e:
                print(f"error parsing jsonl: {str(e)}")
    return data

class Command(BaseCommand):
    help = "This command will populate database with Models"

    def add_arguments(self, parser):
        parser.add_argument("--seed", action="store_true")
        parser.add_argument("--delete", action="store_true")

    def handle(self, *args, **kwargs):

        if kwargs['delete']:
            Model.objects.all().delete()
            return

        models_data = _parse_jsonl(FILE_PATH)

        serializer = ModelCreateSerializer(data=models_data, many=True)
        if not serializer.is_valid():
            self.stderr.write(str(serializer.errors))
            return

        Model.objects.bulk_create([
            Model(**item) for item in serializer.validated_data
        ])

        self.stdout.write(self.style.SUCCESS(f"Created {len(serializer.validated_data)} Models"))