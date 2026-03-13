from typing import Optional
from ninja import Router, Schema
from .models import Category, Model
from main.apps.api.auth import TokenAuth

class CategoryIn(Schema):
    name: str
    description: str

class CategoryOut(Schema):
    id: int
    name: str
    description: str


class ModelIn(Schema):
    name: str
    description: str
    price: float
    category_name: str

class ModelOut(Schema):
    id: int
    name: str
    description: str
    price: float
    category_name: str
    category_id: int

category_router=Router(tags=["Categories"])
model_router=Router(tags=["Models"])

@category_router.get("/", response=list[CategoryOut], auth=TokenAuth())
def get_categories(request, contain: Optional[str] = None):
    categories=Category.objects.all()
    if contain:
        return categories.filter(name__icontains=contain)
    return categories

@category_router.post("/", response=CategoryOut, auth=TokenAuth())
def create_category(request, data: CategoryIn):
    return Category.objects.create(**data.dict())


@category_router.delete("/{category_id}", response=CategoryOut, auth=TokenAuth())
def delete_category(request, category_id: int):
    category = Category.objects.get(id=category_id)
    category.delete()
    return "Category has been deleted"

@model_router.get("/", response=list[ModelOut], auth=TokenAuth())
def get_models(request, min_price: Optional[int] = None, max_price: Optional[int] = None, category : Optional[str] = None):
    models=Model.objects.all()

    if min_price is not None:
        models = models.filter(price__gte=min_price)
    
    if max_price is not None:
        models = models.filter(price__lte=max_price)

    if category is not None:
        models = models.filter(category__name=category)

    return models

@model_router.post("/", response=ModelOut, auth=TokenAuth())
def create_model(request, data: ModelIn):
    category = Category.objects.get(name=data.category_name)
    return Model.objects.create(**data.dict(), category=category)

@model_router.delete("/{model_id}", response=ModelOut, auth=TokenAuth())
def delete_model(request, model_id: int):
    model = Model.objects.get(id=model_id)
    model.delete()
    return "Model has been deleted"




