from django.shortcuts import render

# Create your views here.
from . import agent
from .forms import Question_and_answer
import requests

agent = agent.Agent


def jaka_pogoda(request):

    if request.method == 'POST':

        form = Question_and_answer(request.POST)

        if form.is_valid():

            cd = form.cleaned_data

            question = cd['pytanie']
            
        answer = agent.run(requests, question)

        form = Question_and_answer()

        return render(request, 'zapytania.html', {'odpowiedz': answer, 'form': form})

    else:

        form = Question_and_answer()

    return render(request, 'zapytania.html', {'form': form})




