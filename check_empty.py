# Lower the probability threshold for the papers without getting keywords at the first step
# Note that errors are likely to happen because the wiki miner server is unstable
# If an error happens, just try to run the data in separate batches 

import json
import requests
import xml.etree.ElementTree as ET
import re

with open('arxiv_cs_keywords.json', 'r') as f:
    keywords_all = json.loads(f.read())

# if a paper is withdraw, make its keyword as WITHDRAW
with open('arxiv_cs.json', 'r') as f:
    papers = json.loads(f.read())
papers = [paper[1]+'. '+paper[3] for paper in papers]
papers = [re.sub(r'[@#$%^&*()<>]', ' ', paper) for paper in papers]
for i,paper in enumerate(papers):
    if 'withdrawn' in paper or 'Withdrawn' in paper:
        keywords_all[i] = ['WITHDRAWN']

# record those papers with no keywords
empty_indices = [int(index) for index,k in enumerate(keywords_all) if len(k)==0]

# use wiki miner to detect keywords for papers without keywords
# this time lower the minimum probability to 0
def detect_topic(text):
    url_base = 'http://wikipedia-miner.cms.waikato.ac.nz/services/wikify?source='
    url_threshold = '&minProbability=0'
    r = requests.get(url_base+text+url_threshold)
    root = ET.fromstring(r.content)
    topics = [topic.attrib['title'] for topic in root.iter('detectedTopic')]
    return topics

for index in empty_indices:
    keywords_all[index] = detect_topic(papers[index])

# some paper still has no keywords, then manully add it
keywords_all[15011].append('WITHDRAWN')
keywords_all[26068].append('Mamdani')
keywords_all[61141].append('Synthesis')
keywords_all[70221].append('CoRR')

with open('arxiv_cs_keywords2.json', 'w') as f:
    f.write(json.dumps(keywords_all))
