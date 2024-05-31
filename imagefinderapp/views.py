from django.shortcuts import render
from .models import PexelsImage
from .forms import PexelsSearchForm

def search(request):
    if request.method == 'POST':
        form = PexelsSearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']
            images = PexelsImage.search(query)
    else:
        form = PexelsSearchForm()
        images = []

    context = {'form': form, 'images': images}
    return render(request, 'imagefinder/search.html', context)