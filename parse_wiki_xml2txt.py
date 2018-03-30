# -*- coding: utf-8 -*-
import logging
import os.path
import sys
from gensim.corpora import WikiCorpus

"""
gensim解析bz2语料, xml格式转换为txt
生成 corpus.zhwiki.txt 
"""
if __name__ == '__main__':
    program = os.path.basename(sys.argv[0])  # 获取当前文件名-parse_wiki_xml2txt.py
    logger = logging.getLogger(program)

    logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s')
    logging.root.setLevel(level=logging.INFO)
    logger.info("running %s" % ' '.join(sys.argv))

    # check and process input arguments
    if len(sys.argv) < 3:
        print(globals()['__doc__'] % locals())
        sys.exit(1)
    inp, outp = sys.argv[1:3]
    space = " "
    i = 0

    output = open(outp, 'w')
    wiki = WikiCorpus(inp, lemmatize=False, dictionary={})
    for text in wiki.get_texts():
        output.write(space.join(text) + "\n")
        i += 1
        if i % 10000 == 0:
            logger.info("Saved " + str(i) + " articles")

    output.close()
    logger.info("Finished Saved " + str(i) + " articles")  # Finished Saved 311571 articles
