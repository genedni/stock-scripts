from bs4 import BeautifulSoup
import requests

def main():
    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    tbody = soup.find('tbody')
    tr_tags = tbody.find_all('tr') if tbody else []
    for tr in tr_tags:
        td_tags = tr.find_all('td') if tr else []
        for td in td_tags:
            symbol = td.get_text().replace('\n', '')
            print(f"{symbol}")
            break

if __name__ == "__main__":
    main()
