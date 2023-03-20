import sys

from django.contrib.auth.decorators import login_required
# Create your views here.
from django.http import JsonResponse
from django.shortcuts import render

from .forms import FuzzyExtractorForm, FuzzyExtractorReproduceForm
from .fuzzy_extractor import FuzzyExtractor

extractor = FuzzyExtractor(16, 8)
helperList = []


@login_required(login_url='/account/login/')
def fuzzy_extractor(request):
    if request.method == 'POST' and request.POST.get('old_password'):
        form = FuzzyExtractorForm(request.POST)
        if form.is_valid():
            # process form data and update the database
            key, helper = extractor.generate('AABBCCDDEEFFGGHH')
            helperList.append(helper)
            data = {'field1': str(key), 'field2': str(helper)}
        return JsonResponse(data)
    elif request.method == 'POST' and request.POST.get('helper'):
        form = FuzzyExtractorReproduceForm(request.POST)
        if form.is_valid():
            r_key = extractor.reproduce('AABBCCDDEEFFGGHH', helperList[-1])
            data = {'field1': str(r_key)}
        return JsonResponse(data)
    else:
        form = FuzzyExtractorForm()
        reProduceFornm = FuzzyExtractorReproduceForm()
        context = {'form': form, 'reProduceFornm': reProduceFornm}
        return render(request, 'temp.html', context)
