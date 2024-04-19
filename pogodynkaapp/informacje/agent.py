

import requests
from openai import OpenAI
import os


client = OpenAI()

# w linii poniżej  pobierany jest klucz ze zmiennej środowiskowej o nazwie OPENAI_API_KEY którą trzeba utworzyć i przypisać jej secret key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"),)


# w tej zmiennej utrzymywany jest kontekst zapytań (model ma dostęp do wcześniejszych zapytań)
context = ""


def is_weather_question(query):

    weather_keywords = ["pogoda", "temperatura", "prognoza", "deszcz", "wiatr"]

    for keyword in weather_keywords:

        if keyword in query.lower():

            return True

    return False


def process_query(query):

    # Sprawdzenie, czy pytanie dotyczy pogody

    if is_weather_question(query):

        return "tak"

    else:
        return "nie"


# ta funkcja sprawdza czy pytanie dotyczy konkretnego miasta (jeśli dotyczy conajmniej dwóch miast zwraca nie )
def is_question_about_one_concrete_city(text):

    text_add = text+" Czy w ostatnim pytaniu  tego tekstu występuje  tylko jedna nazwa miasta, jeśli występuje odpowiedz jednym wyrazem małymi literami tak w przeciwnym wypadku odpowiedz nie"

    response = client.chat.completions.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": text_add}], temperature=0)

    return response.choices[0].message.content


#ta funkcja sprawdza czy zapytanie dotyczy prognozy na przyszły czas, czy aktualnej temperatury
def current_or_forecast(text):

    add_to_text = "Czy w tekście: "+text+" w  jego ostatnim zdaniu informacja dotyczy pogody jutra czy dzisiaj. odpowiedz jednym wyrazem małymi literami albo dzisiaj albo jutro"

    response = client.chat.completions.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": add_to_text}], temperature=0)

    return response.choices[0].message.content


def is_question_about_concrete_city(text):

    add_to_text = " w tekście : "+text+" w jego ostatnim pytaniu  można znaleźć informację  o mieście  której dotyczy ,i ją zwróć w jednym wyrazie w mianowniku "

    response = client.chat.completions.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": add_to_text}], temperature=0)

    return response.choices[0].message.content

#ta funkcja odpowiada za zwrócenie odpowiedzi na pytanie
def process_query2(query):

    global context

    concrete_city = is_question_about_one_concrete_city(query)

    if concrete_city == 'tak':

        current_or_forecast_answer = current_or_forecast(query)

        if current_or_forecast_answer == 'dzisiaj':

            response2 = is_question_about_concrete_city(query)

            result = weather(requests, response2, 'dzisiaj')

            return "Dzisiaj w mieście "+response2+" jest temperatura " + str(result['main']['temp'])+" celcjusza."
        else:

            response3 = is_question_about_concrete_city(query)

            result = weather(requests, response3, 'jutro')

            return "Jutro w mieście "+response3+" będzie  temperatura "+str(result['list'][0]['main']['temp'])+" celcjusza."
    else:

        response = client.chat.completions.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": query}])

        return response.choices[0].message.content


class Agent():

    def run(requests, text):

        is_information_about_weather = process_query(text)

        if is_information_about_weather == 'tak':

            global context

            context += text

            answer = process_query2(context)

            context += answer

            return answer
        else:

            return "niewiem"


def weather(requests, city, day):

    # do zmiennej api_key trzeba przypisać klucz, który można wygenerować  zakładając bezpłatne konto na stronie https://openweathermap.org/api
    api_key ='fe997cb160ae5130aeb2cda56b4538fd'

    if day == 'dzisiaj':

        api_key='fe997cb160ae5130aeb2cda56b4538fd'

        api_url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={api_key}'

        response = requests.get(api_url)

        result = response.json()

        return result
    else:

        api_url = f'https://api.openweathermap.org/data/2.5/forecast?q={city}&units=metric&appid={api_key}'

        response = requests.get(api_url)

        result = response.json()

        return result







