import re
from django.shortcuts import render
from django.views.generic import View, TemplateView
from .models import Article, portals
from bs4 import BeautifulSoup
import requests

TALENT_URL = 'https://www.talentrack.in/'
IIMJOBS_URL = 'https://www.iimjobs.com/search/django-0-0-0-1.html'
Internshala_URL = 'https://internshala.com/internships/python%2Fdjango-internship'
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
    def get_context_data(self,*args, **kwargs):
        context = super(HomeView, self).get_context_data(*args,**kwargs)
        context['article'] = Article.objects.all()
        return context


class Talentrack(View):
    def get(self, *args, **kwargs):
        soup = parse_a_website(TALENT_URL)

        # Getting data from soup
        data = []
        divs = soup.find_all('div', attrs={'class': 'col-xs-4'})
        # divs1 = soup.find_all('div', attrs={'class': 'col-lg-3 col-md-3 col-sm-4 pdlr0 mtb2 hidden-xs'})

        for div in divs:
            x = ''
            if div == divs[0]:
                continue
            url = f"https://www.talentrack.in{div.find('a')['href']}"
            for a in div.find_all('span'):
                x += a.text + " || "
            title = x
            # img = "https://s.talentrack.in/images/application/modules/desktop/new-logo-tt.png"
            img = f"https://www.talentrack.in{parse_a_website(url).find('div', {'class': 'lft-testi'}).find('img', {'class':'iblock'})['src']}"

            data.append((url, title, img))

        # Creating Article
        Article.check_if_article_already_exist(data, portals[5][1])

        if len(data) == 0:
            context = {'data': [('#', 'No data to view. Contact with administrator.')]}
            return render(self.request, 'talentrack.html', context)

        context = {
            'data': data[:10],
        }
        return render(self.request, 'talentrack.html', context, )


class Iimjobs(View):
    def get(self, *args, **kwargs):
        soup = parse_a_website(IIMJOBS_URL)

        # Getting data from soup
        data = []
        divs = soup.find_all('a', attrs={'class': 'mrmob5 hidden-xs'})
        divs1 = soup.find_all('div', attrs={'class': 'col-lg-3 col-md-3 col-sm-4 pdlr0 mtb2 hidden-xs'})

        for div, div1 in zip(divs, divs1):
            url = f"{div['href']}"
            title = div.text + div1.find("span").text + " ||posted on " + div1.find('span', {
                'class': 'gry_txt txt12 original'}).text
            # img = "https://d3qr48lsanmyop.cloudfront.net/1626339605082.jpeg"
            img = parse_a_website(url).find('img', {'class': 'recruiterimg'})['cdnlink']

            data.append((url, title, img))

        # Creating Article
        Article.check_if_article_already_exist(data, portals[4][1])

        if len(data) == 0:
            context = {'data': [('#', 'No data to view. Contact with administrator.')]}
            return render(self.request, 'iimjobs.html', context)

        context = {
            'data': data,
        }
        return render(self.request, 'iimjobs.html', context, )


class Internshala(View):
    def get(self, *args, **kwargs):
        soup = parse_a_website(Internshala_URL)

        # Getting data from soup
        data = []
        divs = soup.find_all('div', {'class': 'internship_meta'})

        for div in divs:
            x = ""
            url = f"https://internshala.com{div.find('div', {'class': 'individual_internship_header'}).find('div', {'class': 'company'}).find('div', {'class': 'profile'}).find('a')['href']}"
            for a in div.find('div', {'class': 'individual_internship_details'}).find_all('div',
                                                                                          {'class': 'item_body'}):
                x += a.text + " || "
            title = div.find('div', {'class': 'individual_internship_header'}).find('a').text + " || " + div.find('div',
                                                                                                                  {
                                                                                                                      'class': 'individual_internship_header'}).find(
                'div', {'class': 'company'}).find('div', {'class': 'heading_6 company_name'}).find(
                'a').text + " || " + div.find('div', {'id': 'location_names'}).find('span').text + " || " + x
            img = "https://weblog.wur.eu/international-students/wp-content/uploads/sites/7/2020/01/internship-programs-1024x538-1-1024x480.jpg"
            # img = f"https://internshala.com{div.find('div', {'class': 'internship_logo'}).find('img')['src']}"
            # img = "https://internshala.com" + parse_a_website(url).find('div', {'class': 'internship_logo'}).find('img')['src']
            data.append((url, title, img))

        # Creating Article
        Article.check_if_article_already_exist(data, portals[3][1])

        if len(data) == 0:
            context = {'data': [('#', 'No data to view. Contact with administrator.')]}
            return render(self.request, 'internshala.html', context)

        context = {
            'data': data,
        }
        return render(self.request, 'internshala.html', context, )


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
                data.append((url, title,[]))

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
                img = 'https://aryqtv.tv/wp-content/uploads/2021/04/ary-qtv-logo.png'
                data.append((url, title, img))

        # Creating Article
        Article.check_if_article_already_exist(data, portals[1][1])

        if len(data) == 0:
            context = {'data': [('#', 'No data to view. Contact with administrator.')]}
            return render(self.request, 'qtv.html', context)

        context = {
            'data': data,
        }
        return render(self.request, 'qtv.html', context, )
