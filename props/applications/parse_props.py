"""
Usage:
  parse_props.py [FILE] (-g|-t) (-l|-c) [--original] [--oie] [--dep] [--tokenized] [--dontfilter|--corenlp-json-input]
  parse_props.py (-h|--help)

Parse sentences into the PropS representation scheme

Arguments:
  FILE   input file composed of one sentence per line. if not specified, will use stdin instead

Options:
  -h                      Display this help
  -t                      Print textual PropS representation
  -g                      Print graphical representation (in svg format)
  -l                      Print logical form
  -c                      Print compact logical form
  --original              Print original sentence
  --oie                   Pint open-ie like extractions
  --dep                   Print the intermediate dependency representation 
  --tokenized             Specifies that the input file is tokenized
  --dontfilter            Skip pre-filtering the input file to only printable characters
  --corenlp-json-input    Take Stanford's output json as input (either from STDIN or from file).
"""

#!/usr/bin/env python
#coding:utf8

import os, sys, string
HOME_DIR = os.environ.get("PROPEXTRACTION_HOME_DIR", './')+"/"

import run
import json
from props.webinterface import bottle
from props.applications.viz_tree import DepTreeVisualizer
from props.applications.run import load_berkeley
import fileinput
bottle.debug(True)
import os.path
import codecs
from cStringIO import StringIO
import sys,time,datetime
from subprocess import call
from docopt import docopt
from props.applications.run import parseSentences

from pprint import pprint
import sys
from props.utils.lf_utils import lf_clean
from props.utils.lf_utils import to_de_bruijn

import logging


def main(arguments):
    if not(arguments["--corenlp-json-input"]):
        #Initialize Berekeley parser when using raw input 
        load_berkeley(not arguments["--tokenized"])

    outputType = 'html'
    sep = "<br>"
    if arguments['-t']:
        outputType = 'pdf'
        sep = "\n"
        
    graphical = (outputType=='html')

    # Parse according to source input
    if arguments["--corenlp-json-input"]:
        # Parse accroding to input method
        sents = (json.loads("".join(arguments["FILE"])) \
                 if isinstance(arguments["FILE"], list) \
                 else json.load(arguments["FILE"]))["sentences"]

    elif arguments["--dontfilter"]:
        sents = [x for x in arguments["FILE"]]
    else:
        sents = [filter(lambda x: x in string.printable, s) for s in arguments["FILE"]] 


    numSent = 0
    for sent in sents:
        # be kind to the downstream chain -- do not send blank lines!
        if isinstance(sent, basestring) and sent.strip() == '':
            continue
        numSent=numSent+1
        # print sentence (only if in graphical mode)
        if (arguments["--original"]):
            print(sent)

        gs = parseSentences(sent,
                            HOME_DIR,
                            stanford_json_sent = arguments["--corenlp-json-input"])

        g,tree = gs[0]
        dot = g.drawToFile("","svg")   
        
        # deptree to svg file
        d = DepTreeVisualizer.from_conll_str(tree)
        
            
        #print dependency tree
        if (arguments['--dep']):
            if graphical:
                print(d.as_svg(compact=True,flat=True)+sep)
            else:
                print(tree)
        if (arguments['-t']):
            print(dot.create(format='svg')+sep if graphical else g)

        if arguments['-l'] or arguments['-c']:
            lf = g.toLogicForm() # to_de_bruijn(g.toLogicForm())
            if arguments['-l']:
                pprint(lf)
            if arguments['-c']:
                lf = lf_clean(lf)
                pprint(lf)
        
        #print open ie like extractions
        if (arguments["--oie"]):
            print(sep.join([str(prop) for prop in g.getPropositions(outputType)]))
    #end for loop
    print('Processed {0} sentences.'.format(numSent))
            
    

if __name__ == "__main__":
    logging.basicConfig(level = logging.INFO)
    arguments = docopt(__doc__)
    logging.debug(arguments)
    if arguments["FILE"]:
        arguments["FILE"] = open(arguments["FILE"])
    else:
        arguments["FILE"] = [s for s in sys.stdin]

    main(arguments)


