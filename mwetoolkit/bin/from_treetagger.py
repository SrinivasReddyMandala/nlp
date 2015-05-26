#!/usr/bin/python
# -*- coding:UTF-8 -*-

# ###############################################################################
#
# Copyright 2010-2014 Carlos Ramisch, Vitor De Araujo, Silvio Ricardo Cordeiro,
# Sandra Castellanos
#
# treetagger2xml.py is part of mwetoolkit
#
# mwetoolkit is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# mwetoolkit is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with mwetoolkit.  If not, see <http://www.gnu.org/licenses/>.
#
################################################################################
"""
    This script transforms the output format of TreeTagger to the XML format of
    a corpus, as required by the mwetoolkit scripts. The script is language
    independent as it does not transform the information. You can chose either
    to use sentence splitting of the treetagger (default) or to keep the 
    original sentence splitting. In the latter case, you should add a sentence
    delimiter </s> at the end of each sentence before tagging the text. Only
    UTF-8 text is accepted.
    
    For more information, call the script with no parameter and read the
    usage instructions.
"""

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import

from libs.util import read_options, treat_options_simplest, warn
from libs.base.word import Word
from libs.base.sentence import Sentence
from libs.filetype import ft_treetagger
from libs import filetype


################################################################################     
# GLOBALS     

usage_string = """Usage: 
    
python {program} OPTIONS <corpus.TreeTagger>

The TreeTagger input must have a "</s>" line at the end of each
sentence. This tag will be used to discover the original sentence splitting. 
This behavior is particularly useful when dealing with parallel corpora in 
which the sentence alignment cannot be messed up by the tagger.

IMPORTANT: If you do not have a "</s>"-delimited input file, you must
use the `--sentence` option to select the POS-tag that indicates the
sentence splitting character, otherwise, the result may look like a
corpus with a single (very long) line.


OPTIONS may be:

-s <sent> OR --sentence <sent>
    Name of the POS tag that the TreeTagger uses to separate sentences. Please,
    specify this if you're not using the "</s>" segmentation. For example,
    when parsing English texts, one should indicate `--sentence="SENT"`. The 
    default behaviour is to consider sentences separated by "</s>" tag.

--to <output-filetype-ext>
    Convert input to given filetype extension.
    (By default, converts input to "XML" format):
    {descriptions.output[corpus]}

{common_options}
"""
sent_split = None
output_filetype_ext = "XML"


################################################################################

def treat_options(opts, arg, n_arg, usage_string):
    """Callback function that handles the command line options of this script.
    @param opts The options parsed by getopts. Ignored.
    @param arg The argument list parsed by getopts.
    @param n_arg The number of arguments expected for this script.
    @param usage_string Instructions that appear if you run the program with
    the wrong parameters or options.
    """
    global sent_split
    global output_filetype_ext

    treat_options_simplest(opts, arg, n_arg, usage_string)

    for ( o, a ) in opts:
        if o in ("-s", "--sentence"):
            sent_split = a
        elif o == "--to":
            output_filetype_ext = a
        else:
            raise Exception("Bad arg: " + o)



################################################################################     
# MAIN SCRIPT

longopts = ["sentence=", "to="]
args = read_options("s:", longopts, treat_options, -1, usage_string)
handler = filetype.AutomaticPrinterHandler(output_filetype_ext)
parser = ft_treetagger.TreeTaggerParser("utf-8", sent_split)
filetype.parse(args, handler, parser=parser)
