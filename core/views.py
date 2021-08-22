import re
from django.shortcuts import render
from django.views.generic import View, TemplateView
from .models import Article, portals
from bs4 import BeautifulSoup
import requests

QTV_URL = 'https://soundcloud.com/aryqtv/'
NDTV_URL = 'https://www.ndtv.com/entertainment/'
Amazon_URL = 'https://www.amazon.in/s?bbn=976419031&rh=n%3A976419031%2Cp_89%3Arealme&dc&qid=1624216249&rnid=3837712031&ref=lp_976420031_nr_p_89_3'


def parse_a_website(url) -> BeautifulSoup:
    response = requests.get(url)
    data = response.text
    soup = BeautifulSoup(data, 'html.parser')
    return soup


class HomeView(TemplateView):
    template_name = 'homepage.html'


class AmazonView(View):
    def get(self, *args, **kwargs):
        soup = parse_a_website(Amazon_URL)

        # Getting data from soup
        data = []
        divs = soup.find_all('span')


        for div in divs:
            div1 = div.find_all('a', attrs={'class': 'a-link-normal a-text-normal'})
            for div2 in div1:
                h = div2["href"]
                title = url = f"https://www.amazon.in{h}"
                # # title = div.find('span')
                # img = div.find('img', {'class': 's-image'})['src']
                data.append((url, title))

        # Creating Article
        Article.check_if_article_already_exist(data, portals[2][1])

        if len(data) == 0:
            context = {'data': [('#', 'No data to view. Contact with administrator.')]}
            return render(self.request, 'amazon.html', context)

        context = {
            'data': data,
        }
        return render(self.request, 'amazon.html', context, )


class NdtvView(View):
    def get(self, *args, **kwargs):
        soup = parse_a_website(NDTV_URL)

        # Getting data from soup
        data = []
        divs = soup.find_all('div', attrs={'class': 'listItm'})

        for div in divs:
            global img
            url = f"{div.find('a')['href']}"
            title = div.find('a')['title']
            img = parse_a_website(url).find('img', {'id': 'story_image_main'})['src']
            data.append((url, title, img))

        # Creating Article
        Article.check_if_article_already_exist(data, portals[0][1])

        if len(data) == 0:
            context = {'data': [('#', 'No data to view. Contact with administrator.')]}
            return render(self.request, 'ndtv_news.html', context)

        context = {
            'data': data,
        }
        return render(self.request, 'ndtv_news.html', context, )


class QtvView(View):
    def get(self, *args, **kwargs):
        soup = parse_a_website(QTV_URL)

        # Getting data from soup
        data = []
        divs = soup.find_all('a')
        for div in divs:
            h = div['href']
            i = re.findall('/aryqtv/', h)
            if i and h != "/aryqtv/likes" and h != "/aryqtv/sets" and h != "/aryqtv/comments" and h != "/aryqtv/tracks":
                title = h.replace("/aryqtv/", "").replace("_", " ")
                url = f"https://soundcloud.com{h}"
                # img = div.find('img')['src']
                data.append((url, title))

        # Creating Article
        Article.check_if_article_already_exist(data, portals[1][1])

        if len(data) == 0:
            context = {'data': [('#', 'No data to view. Contact with administrator.')]}
            return render(self.request, 'qtv.html', context)

        context = {
            'data': data,
        }
        return render(self.request, 'qtv.html', context, )
