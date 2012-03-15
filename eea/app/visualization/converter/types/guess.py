""" Guess All Types utility
"""
import re
import operator
from zope.component import getUtilitiesFor
from zope.interface import implements
from Products.CMFPlone.utils import normalizeString
from eea.app.visualization.converter.types.interfaces import IGuessType
from eea.app.visualization.converter.types.interfaces import IGuessTypes

REGEX = re.compile(r"[\W]+")

class GuessTypes(object):
    """ Guess types utility

        >>> from zope.component import getUtility
        >>> from eea.app.visualization.converter.types.interfaces import \
        ...     IGuessTypes
        >>> guess = getUtility(IGuessTypes)
        >>> guess
        <eea.app.visualization.converter.types.guess.GuessTypes object...>

    """
    implements(IGuessTypes)

    def column_type(self, column):
        """ Get column and type from column name

            >>> guess.column_type("start:Date")
            ('start', 'date')

            >>> guess.column_type("Website:URL")
            ('website', 'url')

            >>> guess.column_type("Items: one, two:List")
            ('items_one_two', 'list')

            >>> guess.column_type("Title")
            ('title', 'text')

            >>> guess.column_type("Title is some-thing. + something @lse")
            ('title_is_some_thing_something_lse', 'text')

        """

        if ":" not in column:
            column = normalizeString(column, encoding='utf-8')
            column = REGEX.sub('_', column)
            return column, "text"

        typo = column.split(":")[-1].lower()
        column = ":".join(column.split(":")[:-1])
        column = normalizeString(column, encoding='utf-8')
        column = REGEX.sub('_', column)
        return column, typo

    def __call__(self, datatable):
        """ Guess CSV column types

            >>> csvtable = [
            ... ['label:label', 'Year', 'country', 'Map', 'Population', 'EU'],
            ... ['romania', '2010', 'Romania', '45.76, 27.98', '21959278', 'y'],
            ... ['italy', '2012', 'Italy', '42.8333, 12.83', '60340328', ''],
            ... ['junk', '', '2010', 'Junk', '34, 56', '3423423']
            ... ]

            >>> mapping = guess(csvtable)
            >>> print '\n'.join(' => '.join(x) for x in sorted(mapping.items()))
            country => text
            eu => boolean
            label => text
            map => latlong
            population => number
            year => number

        You can't guess latitude and longitude as they are numbers, and you
        don't want to detect, for example, a percent column as latitude:

            >>> csvtable = [
            ...   ['Country', 'Working Population'],
            ...   ['Romania', '57.43'],
            ...   ['Italy', '83.45']
            ... ]

            >>> mapping = guess(csvtable)
            >>> print '\n'.join(' => '.join(x) for x in sorted(mapping.items()))
            country => text
            working_population => number

        If you still want to detect latitude and longitude, add this in label:

            >>> csvtable = [
            ...   ['Country', 'y:latitude', 'x:longitude'],
            ...   ['Romania', '45.76', '27.98'],
            ...   ['Italy', '42.83', '12.83'],
            ... ]

            >>> mapping = guess(csvtable)
            >>> print '\n'.join(' => '.join(x) for x in sorted(mapping.items()))
            country => text
            x => longitude
            y => latitude

        """
        def compare(a, b):
            """ Compare utilities tuples
            """
            return cmp(a[1].order, b[1].order)

        utilities = getUtilitiesFor(IGuessType)
        utilities = sorted(utilities, cmp=compare)

        mapping = {}
        if not datatable:
            return mapping

        csvtable = datatable[:]
        header = csvtable.pop(0)
        for row in csvtable:
            for index, cell in enumerate(row):
                label = header[index]
                label, typo = self.column_type(label)
                mapping.setdefault(label, {typo: 0})
                for name, guess in utilities:
                    # Skip latitude and longitude guess utilities
                    # as they can mess our auto-detection
                    if name == 'latitude' and 'lat' not in typo:
                        continue
                    elif name == 'longitude'and 'long' not in typo:
                        continue
                    # Skip number if :date in label
                    elif name == 'number' and 'date' in typo:
                        continue
                    if guess(cell, label):
                        mapping[label].setdefault(name, 0)
                        mapping[label][name] += 1
                        break

        res = {}
        for label, statistics in sorted(mapping.items()):
            types = sorted(statistics.items(), key=operator.itemgetter(1),
                           reverse=True)
            res[label] = types[0][0]
        return res