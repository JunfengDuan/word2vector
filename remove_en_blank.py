# -*- coding: utf-8 -*-
import re
import logging
import os.path
import sys

"""
去除英文和空格 文档中还是有很多英文的，一般是文章的reference。
里面还有些日文,罗马文等，这些对模型影响效果可以忽略吧，只是简单的去除了空格和英文。
"""

if __name__ == '__main__':
    program = os.path.basename(sys.argv[0])
    logger = logging.getLogger(program) 
    logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s')
    logging.root.setLevel(level=logging.INFO)
    logger.info("running %s" % ' '.join(sys.argv))
 
    # check and process input arguments
    if len(sys.argv) < 3:
        print (globals()['__doc__'] % locals())
        sys.exit(1)
    inp, outp = sys.argv[1:3]
    i = 0
 
    output = open(outp, 'w')
    f = open(inp)
    line = f.readline()
    while line:                 
        line = f.readline()
        rule = re.compile(r'[ a-zA-z]')  # delete english char and blank
        result = rule.sub('', line)
        output.write(result + "\n")
        i += 1
        logger.info("Saved " + str(i) + " lines")
    f.close()  
    output.close()
    logger.info("Finished Saved " + str(i) + " lines")


