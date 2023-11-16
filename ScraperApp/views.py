from django.shortcuts import render


# Create your views here.


def get_html_content(request):
    import requests
    city = request.GET.get('city')
    city = city.replace(" ", "+")
    USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
    LANGUAGE = "en-US,en;q=0.5"
    session = requests.Session()
    session.headers['User-Agent'] = USER_AGENT
    session.headers['Accept-Language'] = LANGUAGE
    session.headers['Content-Language'] = LANGUAGE
    html_content = session.get(f'https://www.google.com/search?q=weather+{city}').text
    return html_content


def home(request):
    weather_info = None
    if 'city' in request.GET:
        html_content = get_html_content(request)
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')
        weather_info = dict()
        weather_info ['region'] = soup.find("span", attrs={"class": "BNeawe tAd8D AP7Wnd"}).text
        weather_info ['dayhour'], weather_info['weather_now'] = soup.find("div", attrs={"class": "BNeawe tAd8D AP7Wnd"}).text.split('\n')
        weather_info['temp_now'] = soup.find("div", attrs={"class": "BNeawe iBp4i AP7Wnd"}).text
        
    return render(request, 'home.html', {'weather': weather_info})
