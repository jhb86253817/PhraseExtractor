# Use wiki miner to get keywords for the arxiv papers
# Since the server is not stable, the data is splitted to many groups

import sys
import json
import requests
import xml.etree.ElementTree as ET
import re
import os.path

if len(sys.argv) < 3:
    print 'Usage:\npython wiki_miner.py ARXIV_FILE MODE PROBABILITY\n'
    print 'ARXIV_FILE: file name of the input json file, without suffix'
    print 'MODE = [common | fill]'
    print 'PROBABILITY range: [0, 1]'
    print 'default probability of common mode: 0.5'
    print 'default probability of fill mode: 0'
    sys.exit(0)

# get the file name of arxiv corpus without suffix
arxiv_file = sys.argv[1]
# use the extractor in a common way or to fill up the empty phrase lists
mode = sys.argv[2]
if mode != 'common' and mode != 'fill':
    print 'Please check the mode!'
    sys.exit(0)
# the probability threshold for phrase extraction
if len(sys.argv) == 4:
    prob = sys.argv[3]
    if float(prob) < 0 or float(prob) > 1:
        print 'The range of probability threshold is [0,1]'
        sys.exit(0)
# default threshold of common mode is 0.5 and 0.1 for fill mode
else:
    if mode == 'common':
        prob = '0.5'
    else:
        prob = '0'

# load json file of the papers
with open(arxiv_file+'.json', 'r') as f:
    papers = json.loads(f.read())
# the content includes the title and the abstract
texts = [paper[1]+'. '+paper[3] for paper in papers]

# remove meaningless character
texts = [re.sub(r'[@#$%^&*()<>]', ' ', text) for text in texts]

# takes as input the text content, and send request to wiki miner server
def extract_phrase(text):
    url_base = 'http://wikipedia-miner.cms.waikato.ac.nz/services/wikify?source='
    url_threshold = '&minProbability=' + prob
    r = requests.get(url_base+text+url_threshold)
    root = ET.fromstring(r.content)
    phrases = [topic.attrib['title'] for topic in root.iter('detectedTopic')]
    return phrases

if os.path.isfile(arxiv_file+'_phrases.json') and os.path.isfile(arxiv_file+'.info'):
    with open(arxiv_file+'_phrases.json', 'r') as f:
        phrases_all = json.loads(f.read())
    with open(arxiv_file+'.info', 'r') as f:
        info = f.read().split('\n')
    if mode == 'common':
        if len(phrases_all) == len(texts):
            print 'All the documents are finished with the common mode!\nYou may use the fill mode now.'
            sys.exit(0)
        else:
            print 'Starting from %dth document' % (len(phrases_all)+1)
            texts = texts[len(phrases_all):]
            common_docs = int(info[1].split()[1])
    else:
        common_index = int(info[0].split()[1])
        common_docs = int(info[1].split()[1])
        if len(info) == 4:
            fill_index = int(info[2].split()[1])
            fill_docs = int(info[3].split()[1])
            if fill_index >= len(texts):
                print 'All the documents are finished with the fill mode.'
                sys.exit(0)
            print 'Starting from %dth document' % (fill_index+1)
        else:
            fill_index = 0
            fill_docs = 0
else:
    if mode == 'common':
        phrases_all = []
        common_docs = 0
    else:
        print 'No extracted phrases! Please run common mode first!'
        sys.exit(0)

if mode == 'common':
    for text in texts:
        try:
            phrases = extract_phrase(text)
        except KeyboardInterrupt:
            print '\nAn interrupt from keyboard!'
            print 'Saving the extracted phrases...'
            with open(arxiv_file+'_phrases.json', 'w') as f:
                f.write(json.dumps(phrases_all))
            with open(arxiv_file+'.info', 'w') as f:
                f.write('last_processed_doc_with_common_mode: %d\n' % len(phrases_all))
                f.write('current_effective_docs_with_common_mode: %d' % int(common_docs))
            print '%d documents finished' % len(phrases_all)
            sys.exit(0)
        except:
            print 'An error occurs!'
            print 'Saving the extracted phrases...'
            with open(arxiv_file+'_phrases.json', 'w') as f:
                f.write(json.dumps(phrases_all))
            with open(arxiv_file+'.info', 'w') as f:
                f.write('last_processed_doc_with_common_mode: %d\n' % len(phrases_all))
                f.write('current_effective_docs_with_common_mode: %d' % int(common_docs))
            print '%d documents finished' % len(phrases_all)
            sys.exit(0)
        phrases_all.append(phrases)
        if len(phrases) > 0:
            common_docs += 1
        if len(phrases_all)%100 == 0:
            print '%d documents finished' % len(phrases_all)
    with open(arxiv_file+'_phrases.json', 'w') as f:
        f.write(json.dumps(phrases_all))
    with open(arxiv_file+'.info', 'w') as f:
        f.write('last_processed_doc_with_common_mode: %d\n' % len(phrases_all))
        f.write('current_effective_docs_with_common_mode: %d' % int(common_docs))
else:
    for i in range(fill_index, len(texts)):
        if len(phrases_all[i]) == 0:
            try:
                phrases = extract_phrase(texts[i])
            except KeyboardInterrupt:
                print '\nAn interrupt from keyboard!'
                print 'Saving the extracted phrases...'
                with open(arxiv_file+'_phrases.json', 'w') as f:
                    f.write(json.dumps(phrases_all))
                with open(arxiv_file+'.info', 'w') as f:
                    f.write('last_processed_doc_with_common_mode: %d\n' % int(common_index))
                    f.write('current_effective_docs_with_common_mode: %d\n' % int(common_docs))
                    f.write('last_processed_doc_with_fill_mode: %d\n' % i)
                    f.write('added_effective_docs_by_fill_mode: %d' % fill_docs)
                print '%d documents finished' % i
                sys.exit(0)
            except:
                print 'An error occurs!'
                print 'Saving the extracted phrases...'
                with open(arxiv_file+'_phrases.json', 'w') as f:
                    f.write(json.dumps(phrases_all))
                with open(arxiv_file+'.info', 'w') as f:
                    f.write('last_processed_doc_with_common_mode: %d\n' % int(common_index))
                    f.write('current_effective_docs_with_common_mode: %d\n' % int(common_docs))
                    f.write('last_processed_doc_with_fill_mode: %d\n' % i)
                    f.write('added_effective_docs_by_fill_mode: %d' % fill_docs)
                print '%d documents finished' % i
                sys.exit(0)
            phrases_all[i] = phrases
            if len(phrases) > 0:
                fill_docs += 1
        if (i+1)%100 == 0:
            print '%d documents finished' % (i+1)
    with open(arxiv_file+'_phrases.json', 'w') as f:
        f.write(json.dumps(phrases_all))
    with open(arxiv_file+'.info', 'w') as f:
        f.write('last_processed_doc_with_common_mode: %d\n' % int(common_index))
        f.write('current_effective_docs_with_common_mode: %d\n' % int(common_docs))
        f.write('last_processed_doc_with_fill_mode: %d\n' % (i+1))
        f.write('added_effective_docs_by_fill_mode: %d' % fill_docs)

print 'All the documents finished with the %s mode!' % mode
