from bs4 import BeautifulSoup
import requests

def main():
    url = 'https://en.wikipedia.org/wiki/Nasdaq-100'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find(id='constituents')
    tr_tags = table.find_all('tr') if table else []
    for tr in tr_tags:
        td_tags = tr.find_all('td') if tr else []
        for td in td_tags:
            symbol = td.get_text().replace('\n', '')
            print(f"{symbol}")
            break

if __name__ == "__main__":
    main()
