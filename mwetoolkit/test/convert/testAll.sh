#! /bin/bash
HERE="$(cd "$(dirname "$0")" && pwd)"

source "$HERE/../testlib.sh"

usage_exit() { {
    echo "Usage: $(basename "$0") [-h]"
    echo "Test MWE annotation."
    exit 1
} 1>&2;
}

test "$#" -ne 0  && usage_exit


########################################


# test_bidir <filetype> <input-file>
#   Converts <input-file> to XML and compare to reference.
#   Then convert it back and compare with <input-file>.
test_bidir() {
    local filetype="$1"; shift
    local filename="$1"; shift
    local input1="$t_OUTDIR/$filename"
    local output="$t_OUTDIR/${filename}.xml"

    t_run "$t_BIN/transform.py -v --from=$filetype --to=XML $input1 >$output"
    t_compare_with_ref "${filename}.xml"

    local input2="$output"
    local output="${output}.${input1##*.}"
    t_run "$t_BIN/transform.py -v --from=XML --to=$filetype $input2 >$output"
    if test -f "$t_REFDIR/$filename"; then
        t_compare_with_ref "$filename"
    else
        t_compare "$output" "$input1" "Comparing \"$filename\" vs original"
    fi
}

# test_outputOnly <filetype> <input-xml-file> <suffix-output>
#   Converts <input-xml-file> to <filetype> and compare against original.
test_outputOnly() {
    local filetype="$1"; shift
    local basename="$1"; shift
    local suffix_output="$1"; shift
    local input="$t_OUTDIR/$basename"
    local output="$t_OUTDIR/${basename}${suffix_output}"

    local reference="${input%.xml}"
    t_run "$t_BIN/transform.py -v --to=$filetype $input >$output"
    t_compare_with_ref "${basename}${suffix_output}"
}


# Create copy into $t_OUTDIR to simplify the code below
ln -s "$t_LOCAL_INPUT"/* "$t_OUTDIR"/
ln -s "$t_INPUT/tedNN.xml" "$t_OUTDIR/corpus.xml"


###########################################################
# Testing input/output files

t_testname "Check CONLL format"
test_bidir CONLL "corpus.conll"

t_testname "Check Moses format"
test_bidir Moses "corpus.moses"

t_testname "Check PlainCorpus format"
test_bidir PlainCorpus "corpus.PlainCorpus"

t_testname "Check pWaC format"
# TODO add a source_url directive so that the whole conversion works
test_bidir pWaC "corpus.pwac"

t_testname "Check PlainCandidates format"
test_bidir PlainCandidates "candidates.PlainCandidates"

t_testname "Check TreeTagger format"
test_bidir TreeTagger "corpus.treetagger"

t_testname "Check TaggedPlainCorpus format"
test_bidir TaggedPlainCorpus "corpus.TaggedPlainCorpus"


# (For XML, test_outputOnly will end up automatically testing
# both parser and printer, because we use XML itself as input):
t_testname "Check XML format (corpus)"
test_outputOnly  XML "corpus.xml" ".xml"
t_testname "Check XML format (candidates)"
test_outputOnly  XML "candidates.xml" ".xml"
t_testname "Check XML format (patterns)"
test_outputOnly  XML "patterns.xml" ".xml"
test_outputOnly  XML "patterns_deprecated.xml" ".xml"
test_outputOnly  XML "patterns_deprecated2.xml" ".xml"



# TODO
# Implement parser/printer: corpus.palavras
# Implement parser/printer: corpus.treetagger



###########################################################
# Testing output-only formats

t_testname "Check ARFF format"
test_outputOnly ARFF "candidates.xml" ".arff"

t_testname "Check CSV format"
test_outputOnly CSV "candidates.xml" ".csv"

t_testname "Check HTML format"
test_outputOnly HTML "corpus.xml" ".html"

t_testname "Check UCS format"
test_outputOnly UCS "candidates2.xml" ".ucs"



###########################################################
# Testing compressed files

t_testname "Check Gzip uncompression"
t_run "$t_BIN/transform.py -v $t_LOCAL_INPUT/uncompress/corpus.gz >$t_OUTDIR/corpus.gz.PlainCorpus"
t_compare "$t_OUTDIR/corpus.gz.PlainCorpus" "$t_REFDIR/uncompress/corpus.PlainCorpus"

#(This test fails before Python 3.3)
#t_testname "Check Bzip2 uncompression"
#t_run "$t_BIN/transform.py -v $t_LOCAL_INPUT/uncompress/corpus.bz2 >$t_OUTDIR/corpus.bz2.PlainCorpus"
#t_compare "$t_OUTDIR/corpus.bz2.PlainCorpus" "$t_REFDIR/uncompress/corpus.PlainCorpus"

t_testname "Check Zip uncompression"
t_run "$t_BIN/transform.py -v $t_LOCAL_INPUT/uncompress/corpus.zip >$t_OUTDIR/corpus.zip.PlainCorpus"
t_compare "$t_OUTDIR/corpus.zip.PlainCorpus" "$t_REFDIR/uncompress/corpus.PlainCorpus"
