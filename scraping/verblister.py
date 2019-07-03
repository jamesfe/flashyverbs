from bs4 import BeautifulSoup


data = ''
with open('./verblist.html', 'r') as infile:
    data = infile.read()

soup = BeautifulSoup(data, 'html.parser')
a_links = soup.find_all('a', class='blue')


