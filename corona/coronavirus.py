from bs4 import BeautifulSoup
from requests import get

url = "https://www.worldometers.info/coronavirus/"
response = get(url)


class CoronaVirusCases:
    def __init__(self):
        self.soup = BeautifulSoup(response.text, 'html.parser')
        self.corona_info_div = self.soup.find_all('div', attrs={'class': 'maincounter-number'})
        self.corona_countries = self.soup.find('table', attrs={'id': 'main_table_countries_today'})

    def get_total_cases(self):
        total_cases = self.corona_info_div[0].span.text
        return total_cases

    def get_total_deaths(self):
        total_deaths = self.corona_info_div[1].span.text
        return total_deaths

    def get_total_recovered(self):
        total_recovered = self.corona_info_div[2].span.text
        return total_recovered

    def get_country_cases(self, country):
        country_data = None
        for tr in self.corona_countries.find_all('tr'):
            for text in [country.title(), country.upper()]:
                if tr.find('td', text=text) is not None:
                    country_data = tr.find('td', text=text)
                    break
            if country_data is not None:
                data = []
                for td in country_data.find_next_siblings("td"):
                    data.append(td.text)

                return {
                    "total_cases": data[0],
                    "new_cases": data[1],
                    "total_deaths": data[2],
                    "new_deaths": data[3],
                    "total_recovered": data[4]
                }
