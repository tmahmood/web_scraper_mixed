from lxml import html
import requests
import shutil


def get_dom(url, baseurl, session=None):
    """get dom from html

    """
    while True:
        try:
            resp = session.get(url)
            break
        except AttributeError:
            session = requests.Session()
            continue
    dom = html.fromstring(resp.content)
    return html.make_links_absolute(dom, baseurl)


def dom_from_file(filename):
    """get dom from file

    :filename: @todo
    :returns: @todo

    """
    with open(filename, 'r') as fptr:
        content = fptr.read()
        return html.fromstring(content)


def download_image(url):
    """downloads an image

    :url: @todo
    :returns: @todo
    """
    response = requests.get(url, stream=True)
    with open('img.jpg', 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)
    del response


def get_elm(dom, xpath, index=None):
    """returns element by xpath

    """
    elm = dom.xpath(xpath)
    if index != None:
        return elm[0]
    return elm


def get_text(dom, xpath, index):
    """returns text of element by index

    """
    elm = get_elm(dom, xpath, index)
    return elm.text_content().strip()
