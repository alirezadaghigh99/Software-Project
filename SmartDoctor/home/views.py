from django.shortcuts import render


def home_page(request):
    """View function for home page of site."""

    # Render the HTML template home.html with the data in the context variable
    return render(request, 'home/home.html')
