""" Downloads controllers
"""
import json
import csv
import logging
from zope.component import queryMultiAdapter
from Products.Five.browser import BrowserView
logger = logging.getLogger('eea.app.visualization')

class ExcelTSV(csv.excel):
    """ CSV Tab Separated Dialect
    """
    delimiter = '\t'
csv.register_dialect("eea.app.visualization.tsv", ExcelTSV)

class Download(BrowserView):
    """ Download Visualization data in various formats
    """
    def __init__(self, context, request):
        super(Download, self).__init__(context, request)
        self._data = {}

    @property
    def data(self):
        """ JSON data
        """
        if not self._data:
            data = queryMultiAdapter((self.context, self.request),
                                     name=u'daviz-relateditems.json')
            try:
                self._data = json.loads(data())
            except Exception, err:
                logger.debug(err)
                self._data = {'properties':{}, 'items': []}
        return self._data

    def table(self):
        """ Download as HTML table
        """
        items = self.data.get('items', [])

        # Table header
        if not items:
            yield []
        else:
            yield items[0].keys()

        # Table body
        for item in items:
            yield item

    def csv(self, dialect='excel'):
        """ Download as Comma Separated File
        """
        if dialect == 'excel':
            self.request.response.setHeader(
                'Content-Type', 'application/csv')
            self.request.response.setHeader(
                'Content-Disposition',
                'attachment; filename="%s.csv"' % self.context.getId())
        else:
            self.request.response.setHeader(
                'Content-Type', 'application/tsv')
            self.request.response.setHeader(
                'Content-Disposition',
                'attachment; filename="%s.tsv"' % self.context.getId())

        writter = csv.writer(self.request.response, dialect=dialect)
        row = []
        headers = self.data.get('properties', {}).keys()
        for col in headers:
            header = u'%s:%s' % (col,
                                 self.data.get('properties', {}).get(
                                     col, {}).get(
                                         'valueType', 'text'
                                     )
                                 )
            row.append(header)
        writter.writerow(row)

        for item in self.data['items']:
            row = []
            for col in headers:
                row.append(unicode(item.get(col, '')))
            writter.writerow(row)
        return ''

    def tsv(self, dialect='eea.app.visualization.tsv'):
        """ Download as Tab Separated File
        """
        return self.csv(dialect=dialect)

    def json(self):
        """ Downlaod as JSON
        """
        headers = {'Accept' : 'application/sparql-results+json'}
        self.request.response.setHeader(
            'Content-Type', 'application/json')
        self.request.response.setHeader(
            'Content-Disposition',
            'attachment; filename="%s.json"' % self.context.getId())

        headers = self.data.get('properties', {}).keys()
        data = {
            'head': {
                'vars': headers,
            },
            'results': {
                'bindings': [
                    # Items here
                ]
            }
        }

        for item in self.data.get('items', []):
            convertedItem = {}
            for header in headers:
                convertedItem[header] = {
                    "type": "literal",
                    "xml:lang": "en",
                    "value": item.get(header, "")
                }
            data['results']['bindings'].append(convertedItem)

        return json.dumps(data, indent=2)

    def exhibit(self):
        """ Download as Exhibit JSON
        """
        self.request.response.setHeader(
            'Content-Type', 'application/json')
        self.request.response.setHeader(
            'Content-Disposition',
            'attachment; filename="%s.exhibit.json"' % self.context.getId())
        return json.dumps(self.data, indent=2)