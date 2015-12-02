## A key phrase extractor based on wiki miner.

Tested on 78129 arxiv computer science papers.

Input of the extractor:

    arxiv_cs.xml

Output of the extractor:

    arxiv_cs_t_a_k.json


### Usage:
1. run **xml_parsing.py**, which takes as input **arxiv_cs.xml**, and outputs **arxiv_cs.json**
2. run **wiki_miner.py**, which takes as input **arxiv_cs.json**, and outputs folder **topics**
3. run **combine_topics.py**, which takes as input the folder **topics**, and outputs **arxiv_cs_keywords.json**
4. run **check_empty.py**, which takes as input **arxiv_cs_keywords.json**, and outputs **arxiv_cs_keywords2.json**
5. run **combine_t_a_k.py**, which takes as input **arxiv_cs.json** and **arxiv_cs_keywords2.json**, and outputs **arxiv_cs_t_a_k.json**
