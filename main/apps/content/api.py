from ninja import Router
from .models import Category, Model

router = Router()

@router.get("categories")
def get_categories(request, contain: str = None):
    categories = Category.objects.all()
    
    if contain is not None:
        categories = categories.filter(name__icontains=contain)
    
    return {
        "categories": [c.to_json() for c in categories]
    }

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