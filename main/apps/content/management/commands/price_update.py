from django.core.management.base import BaseCommand
from apps.content.models import Model, Category
from apps.content.serializers import ModelCreateSerializer, CategoryCreateSerializer
import json, csv
import os

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


class Command(BaseCommand):
    help = 'Apply a percentage price change to all products in a given category'

    def add_arguments(self, parser, *args, **kwargs):
        parser.add_argument('--category', type=str)
        parser.add_argument('--percent', type=float)

    def handle(self, *args, **kwargs):
        if kwargs['category']:
            models = Model.objects.filter(category__name=kwargs['category'])

        grouped={}
        for product in models:
            if product.category.name not in grouped:
                grouped[product.category.name] = []
            grouped[product.category.name].append({
                'name': product.name if product.name else None,
                'description': product.description if product.description else None,
                'price': float(product.price) * (1 + kwargs['percent'] / 100) if product.price else None,
                'category': product.category.name if product.category else None,
                'image': product.image.url if product.image else None,
                'id': product.id if product.id else None
            })

        with open('updated_price.json', 'w') as file:
            json.dump(grouped, file, indent=2)

        self.stdout.write(self.style.SUCCESS(f"Altered prices in {kwargs['category']} category by {kwargs['percent']}%"))
        
        


        
       