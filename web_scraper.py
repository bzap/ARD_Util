import bs4 as bs
import mechanize
import sys
import ssl

# Scrapes the amazon webpage and returns the title based on the ASIN
def web_scraper(asin):
    # Add an ssl bypass so that service is not denied 
    ssl._create_default_https_context = ssl._create_unverified_context
    url = 'https://www.amazon.com/gp/product/' + asin
    # It uses mechanize because requests and urllib get denied service after a few attempts 
    page = mechanize.Browser()
    page.set_handle_robots(False)
    headers = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    page.addheaders = [('User-agent', headers)]
    page.open(url)
    soup = bs.BeautifulSoup(page.response().read(), features = "lxml")
    title = soup.title.string.rsplit(':')[0]
    return(title)

#web_scraper('0001050230')

