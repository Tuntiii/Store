from ninja import Router, Schema
from .models import Category, Model

router = Router()


class CategoryOut(Schema):
    id: int
    name: str
    description: str
    icon: str | None = None

@router.get("categories", response=list[CategoryOut])
def get_categories(request, contain: str = None):
    categories = Category.objects.all()

    if contain is not None:
        categories = categories.filter(name__icontains=contain)

    return categories

@router.get("models")
def get_models(request, min_price: int = None, max_price: int = None, category : str = None):
    models = Model.objects.all()
    
    if min_price is not None:
        models = models.filter(price__gte=min_price)
    
    if max_price is not None:
        models = models.filter(price__lte=max_price)

    if category is not None:
        models = models.filter(category__name=category)

    return {
        "models": [m.to_json() for m in models]
    }

@router.post("create_category")
def create_category(request, name: str = None, description: str = None, icon: str = None):
    category = Category.objects.create(name=name, description=description, icon=icon)
    return category.to_json()

@router.post("create_model")
def create_model(request, name: str = None, description: str = None, price: float = None, category: str = None, image: str = None):
    model = Model.objects.create(name=name, description=description, price=price, category=Category.objects.get(name=category), image=image)
    return model.to_json()
