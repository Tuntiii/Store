from django.core.management.base import BaseCommand
from apps.content.models import Model, Category
from apps.content.serializers import ModelCreateSerializer, CategoryCreateSerializer
from django.db.models import Count, Avg, Min, Max
import json, csv
import os

def _build_report(category_name, stats):
    report = f"Category: {category_name}\n"
    report += f"Number of products: {stats['total']}\n"
    report += f"Average price: {round(stats['avg_price'], 2)}\n"
    report += f"Minimum price: {round(stats['min_price'], 2)}\n"
    report += f"Maximum price: {round(stats['max_price'], 2)}\n"
    return report

class Command(BaseCommand):
    help = 'Write a catalog report'

    def add_arguments(self, parser, *args, **kwargs):
        
        parser.add_argument('--category', type=str)

    

    def handle(self, *args, **kwargs):
        if kwargs['category']:
            stats = Model.objects.filter(category__name=kwargs['category']).aggregate(
                total=Count('id'),
                avg_price=Avg('price'),
                min_price=Min('price'),
                max_price=Max('price'),
            )

            with open('catalog_report.txt', 'a') as file:
                file.write(_build_report(kwargs['category'], stats))

            self.stdout.write(self.style.SUCCESS(f"Wrote a summary report in catalog_report.txt"))
        else:
            for category in Category.objects.all():
                stats = Model.objects.filter(category=category).aggregate(
                    total=Count('id'),
                    avg_price=Avg('price'),
                    min_price=Min('price'),
                    max_price=Max('price'),
                )

                with open('catalog_report.txt', 'a') as file:
                    file.write(_build_report(category.name, stats))

            self.stdout.write(self.style.SUCCESS(f"Wrote a summary report in catalog_report.txt"))


            
        


        
        


        
       