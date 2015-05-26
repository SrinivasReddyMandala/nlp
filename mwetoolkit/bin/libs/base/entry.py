#!/usr/bin/python
# -*- coding:UTF-8 -*-

################################################################################
#
# Copyright 2010-2014 Carlos Ramisch, Vitor De Araujo, Silvio Ricardo Cordeiro,
# Sandra Castellanos
#
# entry.py is part of mwetoolkit
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
    This module provides the `Entry` class. This class represents a ngram
    entry, i.e. a sequence of words (or word patterns) as they occur in the
    pattern or reference lists (as in mwetoolkit-dict.dtd). An `Entry` contains
    not only an ngram but also associated features, that may contain, for
    instance, reference classes or entry glosses.
"""
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import

from .ngram import Ngram
from .feature import FeatureSet
from .__common import UNKNOWN_FEAT_VALUE

################################################################################

class Entry( Ngram ) :
    """
        An entry is a sequence of words that express a constraint on another
        ngram. The class `Entry` extends `Ngram`, so both contain lists of
        `Word`s. However, an entry is intended to contain additional features.
        Moreover, entries may represent patterns, in which case its words have
        probably `WILDCARD`s to express undefined constraints. The `freqs` list
        of an `Entry` is generally not used.
    """
    def __init__( self, id_number, base=None, freqs=None, features=None ) :
        """
        """
        super( Entry, self ).__init__( base, freqs )
        self.id_number = int(id_number)
        assert features is None or isinstance(features, FeatureSet), features
        # XXX using `max` to merge... Not always a good idea, though,
        # since some features should be summed, and not all features
        # are even numeric!...
        self.features = features or FeatureSet("feat", max)


###############################################################################

    def merge_from(self, other):
        r"""Merge `other` into `self`."""
        super(Entry, self).merge_from(other)
        self.features.merge_from(other.features)


################################################################################

    def to_xml(self):
        """Provides an XML string representation of the
        current object, including internal variables.
            
        @return A string containing the XML element <ngram> with its 
        internal structure, according to mwetoolkit-candidates.dtd.
        """
        ret = ['<entry entryid="', unicode(self.id_number), '">']
        self._to_xml_into(ret)
        ret.append("</entry>")
        return "".join(ret)


    def _to_xml_into( self, output, _print_features=True ) :
        r"""Output stuff into `output`, to be "".join()'ed
        inside the `to_xml` caller function.

        The `print_features` argument is used by the
        Candidate subclass temporarily, but should be removed
        as soon as we have all our regression tests working,
        because there is no good reason to reorder the position
        of the <features> tag and have duplicate code...
        """
        super(Entry, self)._to_xml_into(output)
        if self.features and _print_features :
            output.append("    <features>\n")
            self.features._to_xml_into(output)
            output.append("    </features>\n")

################################################################################

    def add_feat( self, feat ) :
        """
            Add a feature to the list of features of the candidate.

            @param feat A `Feature` of this candidate. No test is performed in
            order to verify whether this is a repeated feature in the list.
        """
        self.features.add( feat.name, feat.value )

################################################################################

    def get_feat_value( self, feat_name ) :
        """
            Returns the value of a `Feature` in the features list. The feature
            is identified by the feature name provided as input to this
            function. If two features have the same name, only the first
            value found will be returned.

            @param feat_name A string that identifies the `Feature` of the
            candidate for which you would like to know the value.

            @return Value of the searched feature. If there is no feature with
            this name, then it will return `UNKNOWN_FEAT_VALUE` (generally "?"
            as in the WEKA's arff file format).
        """
        for feat in self.features :
            if feat.name == feat_name :
                return feat.value
        return UNKNOWN_FEAT_VALUE    
