# Put keywords with titles and abstracts together

import json

with open('arxiv_cs_keywords2.json', 'r') as f:
    keywords_all = json.loads(f.read())
with open('arxiv_cs.json', 'r') as f:
    papers = json.loads(f.read())

titles = [paper[1] for paper in papers]
abstracts = [paper[3] for paper in papers]

t_a_k = zip(titles, abstracts, keywords_all)

with open('arxiv_cs_t_a_k.json', 'w') as f:
    f.write(json.dumps(t_a_k))
