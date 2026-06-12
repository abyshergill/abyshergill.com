from .models import Category

def navigation_categories(request):
    return {
        'nav_categories': Category.objects.prefetch_related('subjects').all()
    }
