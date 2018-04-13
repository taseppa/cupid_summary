import mechanize
from bs4 import BeautifulSoup
import io
import codecs
from jinja2 import Environment, FileSystemLoader, select_autoescape
import os
import argparse

THIS_DIR = os.path.dirname(os.path.abspath(__file__))

env = Environment(
    loader=FileSystemLoader(THIS_DIR))


def generate_page(email, password, number_of_pages, search_id, base_url):
    """Generate a HTML page containing summary of profiles.

    Parameters
    ----------
    email : string
        Email address used for logging.
    password : string
        Password used fo logging.
    number_of_pages : int
        How many pages is included in the summary.
    search_id : int
        The search id for the cupid site.
    base_url : type
        Base url address of the cupid site.

    Returns
    -------
    None

    """
    print "Logging in..."
    br = mechanize.Browser()
    br.open(base_url + "/en/auth/login")
    br.select_form(nr=0)

    br.form["Email"] = email
    br.form["password"] = password
    response = br.submit()
    profiles = []

    for i in range(1, number_of_pages + 1):
        profiles.extend(find_profiles(br, i, search_id, base_url))

    template = env.get_template('template.html')
    html = template.render(base_url=base_url, profiles=profiles)
    write_file("index.html", html)


def find_profiles(br, page_num, searchno, base_url):
    profiles = []
    print "Getting profiles pagenum = %d" % (page_num)
    response = br.open("%s/en/results/search?searchtype=1&savedsearch=%d&pageno=%d" %
                       (base_url, searchno, page_num))
    response_data = response.read()
    soup = BeautifulSoup(response_data, 'html.parser')
    spans = soup.find_all("span", class_="memberpic")

    for span in spans:
        link = span.find("a")["href"]
        name = span.find("a")["name"]
        img = span.find("img")["src"]
        # print img, link, name
        profiles.append({"link": link, "img": img, "name": name})

    return profiles


def write_file(name, contents):
    with codecs.open(name, mode="w", encoding='utf-8') as f:
        f.write(contents)


def main():

    parser = argparse.ArgumentParser(description='Scrape profiles')
    parser.add_argument('pages', type=int, default=1,
                        help='Number of pages to process')
    parser.add_argument('email', type=str,
                        help='Email')
    parser.add_argument('password', type=str,
                        help='Password')
    parser.add_argument('searchno', type=int,
                        help='Search number')
    parser.add_argument('baseurl', type=string,
                        help='Base url', default="https://www.thaicupid.com")
    args = parser.parse_args()
    generate_page(email=args.email, password=args.password, number_of_pages=args.pages, search_id=args.searchno, base_url=args.base_url)


if __name__ == "__main__":
    main()
