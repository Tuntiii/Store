from django.core.management.base import BaseCommand
from apps.content.models import Model, Category
from apps.content.serializers import ModelCreateSerializer, CategoryCreateSerializer
import json, csv
import os

MODEL_PATH = os.path.join(os.path.dirname(__file__), "data", "model.jsonl")
CATEGORY_PATH = os.path.join(os.path.dirname(__file__), "data", "category.jsonl")

def _parse_jsonl(path):
    data = []
    with open(path, 'r') as file:
        for line in file:
            try:
                data.append(json.loads(line))
            except json.JSONDecodeError as e:
                print(f"error parsing jsonl: {str(e)}")
    return data

def _parse_csv(path):
    data = []
    with open(path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(row)
    return data

class Command(BaseCommand):
    help = 'Export data to json/csv files'

    def add_arguments(self, parser, *args, **kwargs):
        
        parser.add_argument('--format', choices=['json', 'csv'], default='json')
        parser.add_argument('--output', type=str, default='output.json')
        parser.add_argument('--category', type=str)

    def handle(self, *args, **kwargs):
        if kwargs['category']:
            models = Model.objects.filter(category__name=kwargs['category'])
        else:
            models = Model.objects.all()

        grouped={}
        for product in models:
            if product.category.name not in grouped:
                grouped[product.category.name] = []
            grouped[product.category.name].append({
                'name': product.name if product.name else None,
                'description': product.description if product.description else None,
                'price': float(product.price) if product.price else None,
                'category': product.category.name if product.category else None,
                'image': product.image.url if product.image else None,
                'id': product.id if product.id else None
            })

        if kwargs['format'] == 'json':
            with open(kwargs['output'], 'w') as file:
                json.dump(grouped, file, indent=2)
        elif kwargs['format'] == 'csv':
            with open(kwargs['output'], 'w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=['category', 'name', 'description', 'price', 'image', 'id'])
                writer.writeheader()
                for category_name, products in grouped.items():
                    for product in products:
                        writer.writerow({
                            'category': category_name,
                            **product
                        })

        self.stdout.write(self.style.SUCCESS(f"Data exported to {kwargs['output']}"))
        
        


        
       