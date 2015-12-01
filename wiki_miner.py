# Use wiki miner to get keywords for the arxiv papers
# Since the server is not stable, the data is splitted to many groups

import json
import requests
import xml.etree.ElementTree as ET
import re

# load json file of the papers
with open('arxiv_cs.json', 'r') as f:
    papers = json.loads(f.read())
# the content includes the title and the abstract
texts = [paper[1]+'. '+paper[3] for paper in papers]
# only use 1000 papers each time, manully change the slice interval
texts = texts[:1000]

# remove meaningless character
texts = [re.sub(r'[@#$%^&*()<>]', ' ', text) for text in texts]

def detect_topic(i,text):
    if i%100==0:
        print i
    url_base = 'http://wikipedia-miner.cms.waikato.ac.nz/services/wikify?source='
    r = requests.get(url_base+text)
    root = ET.fromstring(r.content)
    topics = [topic.attrib['title'] for topic in root.iter('detectedTopic')]
    return topics

topics = [detect_topic(i,text) for i,text in enumerate(texts)]

with open('topics/arxiv_cs_topics_0_1000.json', 'w') as f:
    f.write(json.dumps(topics))
