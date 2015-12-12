# Extract contents from XML file to json file

import xml.etree.ElementTree as ET 
import json
import sys

if len(sys.argv) < 3:
    print 'Usage:\npython xml_parsing.py data/arxiv_cs_xml/arxiv_cs.xml data/arxiv_cs_json/arxiv_cs.json'
    sys.exit(0)
arxiv_xml = sys.argv[1]
arxiv_json = sys.argv[2]

def save_to_json(root):
    articles = []

    for article in root.findall('article'):
        id = article.find('id').text
        title = article.find('title').text
        author = article.find('author').text
        abstract = article.find('abstract').text
        venue = article.find('venue').text
        url = article.find('url').text
        articles.append((id, title, author, abstract, venue, url))

    articles_string = json.dumps(articles)
    with open(arxiv_json, 'w') as f:
        f.write(articles_string)

if __name__ == '__main__':
    tree = ET.parse(arxiv_xml)
    root = tree.getroot()
    save_to_json(root)

