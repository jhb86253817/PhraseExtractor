## A key phrase extractor based on wikipedia miner.

Tested under python 2.7.6, no extra libraries needed.

The server we use is the wikify service under [wikipedia miner](http://wikipedia-miner.cms.waikato.ac.nz/services/). Because the phrase extraction algorithm of wikipedia miner is able to process each document separately, we send a http request for each paper sequentially. Please see the [paper](http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.178.2266&rep=rep1&type=pdf) for more algorithm details.

### Data:
 - *`data/arxiv_cs_xml/arxiv_cs.xml`*: original XML file of 78129 arxiv computer science papers.
 - *`data/arxiv_cs_json/arxiv_cs.json`*: extracted contents from the XML file by the script *`xml_parsing.py`*.
 - *`data/arxiv_cs_json_1000/arxiv_cs_1000.json`*: first 1000 papers of the whole data, for testing.

### Scripts:
 - *`xml_parsing.py`*
 - *`wiki_miner.py`*
 - *`manual_add_phrase.py`*
 - *`combine_t_a_k.py`*

### General pipline:
1. use *`xml_parsing.py`* to parse XML file, and save the contents in a json file. If the json file already exists, this can be skipped.
1. use *`wiki_miner.py`* to extract phrases with a specific probability threshold (0.5 by default) under the `common` mode.
2. use *`wiki_miner.py`* to extract phrases with a lower probability threshold (0 by default) under the `fill` mode, for those documents with empty phrase list from the previous step.
3. use *`manual_add_phrase.py`* to manually add key phrases for the documents still without any key phrases by now.
4. use *`combine_t_a_k.py`* to combine the extracted phrases with the corresponding titles and abstracts.

Note that an error may occur when running *`wiki_miner.py`* due to the instability of the server. The script will save the extracted phrases if an error occurs. Just run the command again to extract the remaining papers. If there is keyboard interrupt, the extracted phrases will also be saved.

### A running example:
1. run 

    ``python wiki_miner.py data/arxiv_cs_json/arxiv_cs common 0.5``

2. run

    ``python wiki_miner.py data/arxiv_cs_json/arxiv_cs fill 0``

3. run

    ``python manual_add_phrase.py data/arxiv_cs_json/arxiv_cs``

4. run

    ``python combine_t_a_k.py data/arxiv_cs_json/arxiv_cs``

Finally, the target file will be generated as *`data/arxiv_cs_json/arxiv_cs_t_a_k.json`*, containing title, abstract and extracted key pharses of the papers.

