#!/usr/bin/python
# -*- coding:UTF-8 -*-

################################################################################
#
# Copyright 2010-2014 Carlos Ramisch, Vitor De Araujo, Silvio Ricardo Cordeiro,
# Sandra Castellanos
#
# ngram.py is part of mwetoolkit
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
    This module provides the `Ngram` class. This class represents an ngram, i.e.
    a sequence of words as they occur in the corpus. A ngram is any sequence of
    n words, not necessarily a linguistically motivated phrase.
"""

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import

from .feature import FeatureSet
from .word import Word
from .frequency import Frequency
from .__common import SEPARATOR, WILDCARD, WORD_SEPARATOR

################################################################################        

class Ngram (object):
    """
        A `Ngram` is a sequence of n adjacent words. For example, an ngram with 
        2 adjacent words is called bigram and has n=2. An ngram with 3 words is 
        called trigram and has n=3. Besides the list of words composing the 
        ngram, the class also has a list of frequencies that correspond to the
        number of occurrences of the ngram in a corpus.
    """

################################################################################

    def __init__( self, word_list=None, freqs=None, sources=None ) :
        """
            Instanciates the `Ngram` with the list of words that compose it and
            the list of frequencies associated to the ngram. 
            
            @param word_list A list of `Word`s corresponding to the sequence of
            adjacent tokens found in the corpus. The size of the list will
            determine the value of n, no verification is made in order to 
            constraint the size of the list, i.e. you can define an empty ngram,
            a 1-gram (ngram with a single word) or even 400-grams if you want.
            
            @param freqs A list of `Frequency`ies corresponding to counts of 
            occurrences of this ngram in a certain corpus. Please notice that
            the frequencies correspond to occurrences of ALL the words of the
            ngram in a corpus. Individual word frequencies are attached to the
            corresponding `Word` object in the `word_list`. 

            @param sources A list of the ids of the sentences where the
            ngram occurs.
            
            @return A new instance of a `Ngram`.
        """
        self.word_list = word_list or []
        assert freqs is None or isinstance(freqs, FeatureSet), freqs
        self.freqs = freqs or FeatureSet("freq", lambda x,y: x+y)
        self.sources = list(sources) if sources else []


###############################################################################

    def merge_from(self, other):
        r"""Merge `other` into `self`."""
        self.freqs.merge_from(other.freqs)
        self.sources.extend(other.sources)


################################################################################
    
    def append( self, word ) :
        """
            Append a `Word` to the end of the list of words of the ngram.
            
            @param word `Word` that corresponds to an adjacent token of this 
            ngram in a corpus. Should contain at least one of the three 
            components of a word (surface form, lemma or POS tag), unless you 
            want to explicitely concatenate an empty word to the end of the 
            ngram. No test is performed in order to verify whether this is a 
            repeated word in the list or whether the ngram is linguistically 
            well-formed. This means that if you concatenate words that do not 
            make sense together (e.g. "the of going never"), it is basically 
            your problem.
        """
        self.word_list.append( word )
        
################################################################################
        
    def add_frequency( self, freq ) :
        """
            Add a `Frequency` to the list of frequencies of the ngram.
            
            @param freq `Frequency` that corresponds to a count of this ngram in 
            a corpus. No test is performed in order to verify whether this is a 
            repeated frequency in the list.
        """
        self.freqs.add( freq.name, freq.value )

################################################################################
        
    def add_sources(self, sources):
        r"""Add source information.
        Example: ["1:3,4,5", "7:3,2"].
        Meaning: ID 1 (words 3, 4 and 5) and ID 7 (words 3 and 2).
        """
        self.sources.extend(sources)

################################################################################
    
    def to_string( self ) :
        """
            Converts this ngram to an internal string representation where each
            word is separated from each other by a `WORD_SEPARATOR` and each
            part of the word is separated with a special `SEPARATOR`. This is 
            only used internally by the scripts and is of little use to the
            user because of reduced legibility. Deconversion is made by the 
            function `from_string`.
            
            @return A string with a special internal representation of the 
            ngram.
        """
        return WORD_SEPARATOR.join(w.to_string() for w in self)

################################################################################
        
    def from_string( self, the_string ) :
        """ 
            Instanciates the current ngram by converting to an object 
            an internal string representation where each word is separated from 
            each other by a `WORD_SEPARATOR` and each part of the word is 
            separated with a special `SEPARATOR`. This is only used internally 
            by the scripts and is of little use to the user because of reduced 
            legibility. Deconversion is made by the function `to_string`.
            
            @param the_string A string with a special internal representation of 
            the ngram, as generated by the function `to_string`
        """
        words_string = the_string.split( WORD_SEPARATOR )
        for word_string in words_string :           
            a_word = Word()
            a_word.from_string( word_string )
            self.append( a_word )
       
################################################################################

    def to_xml(self):
        """Provides an XML string representation of the
        current object, including internal variables.
            
        @return A string containing the XML element <ngram> with its 
        internal structure, according to mwetoolkit-candidates.dtd.
        """
        ret = ["<ngram>"]
        self._to_xml_into(ret)
        ret.append("</ngram>")
        return "".join(ret)


    def _to_xml_into( self, output ) :
        r"""Output stuff into `output`, to be "".join()'ed
        inside the `to_xml` caller function.
        """
        for word in self :
            word._to_xml_into(output)
            output.append(" ")

        self.freqs._to_xml_into(output)

        if len(self.sources) > 0:
            sources_string = ';'.join(unicode(s) for s in self.sources)
            output.append('<sources ids="%s"/>' % sources_string)
        

################################################################################    
    
    def __iter__( self ) :
        return iter(self.word_list)

################################################################################            
    
    def __len__( self ) :
        """
            Returns the size of the ngram in number of words, i.e. the value of 
            n. An ngram with 2 words is called bigram and has n=2. An ngram with
            3 words is called trigram and has n=3.
            
            @return The number of words contained in the ngram.
        """ 
        return len( self.word_list )  
        
################################################################################

    def __getitem__( self, i ) :
        """
            Returns a `Word` corresponding to the index `i` in the ngram. If the
            index i does not exist, will generate a `IndexError`.
            
            @param i The index i corresponding to the position of the searched
            word. If i=2, for instance, will return the 3rd word (indices start
            at zero) of the ngram.
            
            @return A `Word` at the i-th position of the ngram, or generates 
            IndexError if the position i is larger than the ngram size.
        """ 
        return self.word_list[ i ]

################################################################################

    def __cmp__( self, other ) :
        return cmp(self.word_list, other.word_list)

################################################################################

    def __eq__( self, other ) :
        return self.word_list == other.word_list

################################################################################

    def __hash__( self ) :
        # XXX TODO implement freeze() method and refuse to hash when unfrozen
        return hash(self.to_string())

################################################################################

    def get_pos_pattern( self ) :
        """
            Returns the sequence of Part Of Speech tags of this ngram 
            concatenated with an intervening `SEPARATOR`. For example, if the
            ngram is a sequence of one adjective (A) and two nouns (N), will 
            probably return something like "A#S#N#S#N", where "#S#" is the 
            separator.
            
            @return A string that corresponds to the sequence of POS tags of the
            ngram's words. The POS tags are joined with a special `SEPARATOR`
            defined in `__common.py`. Please pay attention that no POS tag 
            should be similar to the separator, to avoid ambiguities.
        """
        result = ""
        for word in self :
            result = result  + word.pos + SEPARATOR
        return result[ 0:len( result ) - len(SEPARATOR) ]        
        
        
################################################################################

    def set_all( self, surface=None, lemma=None, pos=None ) :
        """
            Sets the same value for all the words in the ngram. This is useful,
            for instance, if one wants to set all POS tags of the words to a
            `WILDCARD`, so that POS tag is ingored in candidate extraction.
            
            @param surface The new value of the surface of the ngram's words. If
            this parameter is None, the surface forms of the words remain 
            unchanged. Defaults to None.
            
            @param lemma The new value of the lemma of the ngram's words. If
            this parameter is None, the lemmas of the words remain unchanged. 
            Defaults to None.
            
            @param pos The new value of the POS tag of the ngram's words. If
            this parameter is None, the POS tags of the words remain unchanged. 
            Defaults to None. 
        """
        for word in self :
            if surface is not None :
                word.surface = surface
            if lemma is not None :
                word.lemma = lemma
            if pos is not None :
                word.pos = pos       
                
################################################################################

    def get_freq_value( self, freq_name ) :
        """
            Returns the value of a `Frequency` in the frequencies list. The 
            frequency is identified by the frequency name provided as input to 
            this function. If two frequencies have the same name, only the first 
            value found will be returned.
            
            @param freq_name A string that identifies the `Frequency` of the 
            candidate for which you would like to know the value.
            
            @return Value of the searched frequency. If there is no frequency 
            with this name, then it will return 0.
        """
        for freq in self.freqs :
            if freq.name == freq_name :
                return freq.value
        return 0     
        
################################################################################

    def update_freq_value( self, freq_name, freq_value ) :
        """
            Updates the value of a `Frequency` in the frequencies list. The 
            frequency is identified by the frequency name. If two frequencies 
            have the same name, only the first will be updated. If no frequency
            has the given name, a new one is added to the ngram.
            
            @param freq_name A string that identifies the `Frequency` of the 
            candidate which you would like to update (or add, if it does not
            exist).
            
            @param freq_value Value of the frequency. If there is no frequency 
            with this name, then it will return 0.
        """
        for freq in self.freqs :
            if freq.name == freq_name :
                freq.value = freq_value
                return
        self.add_frequency( Frequency( freq_name, freq_value ) )                                     
            
################################################################################   

    def count( self, an_ngram, ignore_pos=False ) :
        """
            Matches the current `Ngram` with another `Ngram` given as parameter.
            The return, instead of boolean, is an integer that corresponds to 
            the number of times `an_ngram` occurs in the current ngram.
            
            @param an_ngram An `Ngram` that is going to be searched within the
            current `Ngram` (therefore, shorter or equal to it)
            
            @param ignore_pos If True, ngrams are counted regardless of POS tag,
            otherwise ngrams with different POS sequences are considered 
            different (default).
            
            @return The number of times that `an_ngram` was found in the current
            `Ngram`.            
        """
        i = 0
        result_count = 0
        n = len( an_ngram )

        for w in self :
            bef_pos = w.pos
            if ignore_pos :
                w.pos = WILDCARD
            
            if i == n :
                result_count = result_count + 1
                if w.match( an_ngram[ 0 ] ) :
                    i = 1
                else :
                    i = 0
            
            elif w.match( an_ngram[ i ] ) :
                i = i + 1
            elif w.match( an_ngram[ 0 ] ) :
                i = 1
            else :
                i = 0
            
            w.pos = bef_pos
        if i == n :
            result_count = result_count + 1
        return result_count            

################################################################################   

    def find( self, an_ngram, ignore_pos=False ) :
        """
            Matches the current `Ngram` with another `Ngram` given as parameter.
            The return value is an integer that corresponds to the position in
            the ngram where the first instance of `an_ngram` was found.
            
            @param an_ngram An `Ngram` that is going to be searched within the
            current `Ngram` (therefore, shorter or equal to it)
            
            @param ignore_pos If True, ngrams are counted regardless of POS tag,
            otherwise ngrams with different POS sequences are considered 
            different (default).
            
            @return The position in the current `Ngram` where the first instance 
            of `an_ngram` was found.            
        """
        i = 0
        n = len( an_ngram )
        result_pos = -n        
        for w in self :
            bef_pos = w.pos
            if ignore_pos :
                w.pos = WILDCARD
            
            if i == n :
                return result_pos            
            elif w.match( an_ngram[ i ] ) :
                i = i + 1
            elif w.match( an_ngram[ 0 ] ) :
                i = 1
            else :
                i = 0                
            w.pos = bef_pos
            result_pos = result_pos + 1
        if i == n :
            return result_pos        
        return -1         

################################################################################

    def match( self, some_ngram, ignore_case=False, lemma_or_surface=False ) :
        """
            A simple matching algorithm that returns true if ALL the words of
            the current pattern match all the words of the given ngram. Since a 
            pattern does generally contain `WILDCARD`s to express loose
            constraints, the matching is done at the word level considering only
            the parts that are defined, for example, POS tags for candidate
            extraction or lemmas for automatic gold standard evaluation.
            
            @param some_ngram A `Ngram` against which we would like to compare
            the current pattern. In general, the pattern contains the 
            `WILDCARD`s while `some_ngram` has all the elements with a defined
            value.

            @return Will return True if ALL the words of `some_ngram` match ALL
            the words of the current pattern (i.e. they have the same number of
            words and all of them match in the same order). Will return False if
            the ngrams have different sizes or if ANY of the words of 
            `some_ngram` does not match the corresponding word of the current 
            pattern.
        """
        if( len( some_ngram ) == len( self ) ) :
            for i in range( len( self ) ) :
                if not self[ i ].match( some_ngram[ i ], ignore_case=ignore_case, lemma_or_surface=lemma_or_surface ) :
                    return False
            return True
        else :
            return False
