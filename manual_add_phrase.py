# Show the contents of the docs with empty phrase list
# Manually add key phrases for these docs

import json
import sys

if len(sys.argv) < 2:
    print 'Usage:\npython manual_add_phrase.py ARXIV_FILE_PREFIX'
    print 'ARXIV_FILE_PREFIX: e.g. data/arxiv_cs_json/arxiv_cs'
    sys.exit(0)

file_prefix = sys.argv[1]

with open(file_prefix+'.json', 'r') as f:
    papers = json.loads(f.read())
with open(file_prefix+'_phrases.json', 'r') as f:
    phrases = json.loads(f.read())
with open(file_prefix+'.info', 'r') as f:
    info = f.read().split('\n')

effective_num = int(info[1].split()[1]) + int(info[3].split()[1])
if effective_num == len(papers):
    print 'All the documents have key phrases!'
    sys.exit(0)
else:
    print '%d documents left for manual adding.\n' % (len(papers)-effective_num)

for i in range(len(papers)):
    if len(phrases[i]) == 0:
        print 'ID: %d' % (i+1)
        print 'Title: %s' % papers[i][1]
        print 'Abstract: %s\n' % papers[i][3]
        while(True):
            p = raw_input('Input a key phrase: ')
            phrases[i].append(p)
            c = raw_input('continue? y/n: ')
            if c != 'y':
                break
        print ''

print 'All the documents have phrases now, saving it...'
with open(file_prefix+'_phrases.json', 'w') as f:
    f.write(json.dumps(phrases))
with open(file_prefix+'.info', 'a+') as f:
    f.write('\nmanually_added_docs: %d' % (len(papers)-effective_num))
