## A key phrase extractor based on wiki miner.

Tested on 78129 arxiv computer science papers.

Input of the extractor:

    arxiv_cs.xml

Output of the extractor:

    arxiv_cs_t_a_k.json


# Usage:
- run python xml_parsing.py, which takes as input arxiv_cs.xml, and outputs arxiv_cs.json
- run python wiki_miner.py, which takes as input arxiv_cs.json, and outputs folder topics
- run python combine_topics.py, which takes as input the folder topics, and outputs arxiv_cs_keywords.json
- run python check_empty.py, which takes as input arxiv_cs_keywords.json, and outputs arxiv_cs_keywords2.json
- run python combine_t_a_k.py, which takes as input arxiv_cs.json and arxiv_cs_keywords2.json, and outputs arxiv_cs_t_a_k.json
