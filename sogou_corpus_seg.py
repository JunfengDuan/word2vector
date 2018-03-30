# -*- coding: utf-8 -*-
# word_segment.py用于语料分词

import logging
import os.path
import sys
import re
import jieba


# 先用正则将<content>和</content>去掉
def reTest(content):
    reContent = re.sub('<content>|</content>', '', content)
    return reContent


if __name__ == '__main__':
    program = os.path.basename(sys.argv[0])
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

    finput = open(inp)
    foutput = open(outp, 'w')

    for line in finput:
        line_seg = jieba.cut(reTest(line))
        foutput.write(space.join(line_seg))
        i = i + 1
        if (i % 1000 == 0):
            logger.info("Saved " + str(i) + " articles_seg")

    finput.close()
    foutput.close()
    logger.info("Finished Saved " + str(i) + " articles")
