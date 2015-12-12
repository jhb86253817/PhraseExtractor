# Combine the extracted phrases with their titles and abstracts

import json
import sys

if len(sys.argv) < 2:
    print 'Usage:\npython combine_t_a_k.py ARXIV_FILE_PREFIX'
    print 'ARXIV_FILE_PREFIX: e.g. data/arxiv_cs_json/arxiv_cs'
    sys.exit(0)

file_prefix = sys.argv[1]

with open(file_prefix+'.json', 'r') as f:
    papers = json.loads(f.read())
with open(file_prefix+'_phrases.json', 'r') as f:
    phrases = json.loads(f.read())

titles = [paper[1] for paper in papers]
abstracts = [paper[3] for paper in papers]
t_a_k = zip(titles, abstracts, phrases)

print len(t_a_k)
print t_a_k[0]
print t_a_k[1]
    
with open(file_prefix+'_t_a_k.json', 'w') as f:
    f.write(json.dumps(t_a_k))
