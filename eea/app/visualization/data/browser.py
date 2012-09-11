""" Custom converters to JSON
"""
import logging
import json as simplejson
from StringIO import StringIO
from zope.interface import implements
from zope.component import queryUtility, queryAdapter, queryMultiAdapter
from Products.Five.browser import BrowserView
from eea.app.visualization.interfaces import IVisualizationData
from eea.app.visualization.interfaces import IVisualizationJson
from eea.app.visualization.interfaces import IVisualizationConfig
from eea.app.visualization.converter.interfaces import ITable2JsonConverter
from eea.app.visualization.cache import ramcache, cacheJsonKey
from eea.app.visualization.converter.converter import sortProperties

logger = logging.getLogger('eea.app.visualization')

class JSON(BrowserView):
    """ Abstract view to provide "daviz-view.json" multiadapter
    """
    implements(IVisualizationJson)

    @ramcache(cacheJsonKey, dependencies=['eea.daviz'])
    def json(self, column_types=None):
        """ Implement this method in order to provide a valid exhibit JSON
        """
        res = {'items': [], 'properties': {}}

        # Get data
        adapter = queryAdapter(self.context, IVisualizationData)
        if not (adapter or adapter.data):
            return simplejson.dumps(res)

        # Convert to JSON
        datafile = StringIO(adapter.data)
        converter = queryUtility(ITable2JsonConverter)
        try:
            _cols, res = converter(datafile, column_types)
        except Exception, err:
            logger.debug(err)
            return simplejson.dumps(res)

        # Update JSON with existing annotations properties
        accessor = queryAdapter(self.context, IVisualizationConfig)
        if not accessor:
            return sortProperties(simplejson.dumps(res))

        my_json = accessor.json
        res.setdefault('properties', {})
        res['properties'].update(my_json.get('properties', {}))
        return sortProperties(simplejson.dumps(res))

class RelatedItems(JSON):
    """ Merged JSON from related items
    """
    @ramcache(cacheJsonKey, dependencies=['eea.daviz'])
    def json(self, column_types=None):
        """ JSON
        """
        my_json = queryMultiAdapter(
            (self.context, self.request), name=u'daviz-view.json')
        if my_json:
            try:
                my_json = simplejson.loads(my_json())
            except Exception, err:
                logger.exception(err)
                my_json = {}
        else:
            my_json = {}

        relatedItems = getattr(self.context, 'getRelatedItems', ())
        if relatedItems:
            relatedItems = relatedItems()

        new_json = {'items': [], 'properties': {}}
        for item in relatedItems:
            daviz_json = queryMultiAdapter(
                (item, self.request), name=u'daviz-view.json')

            if not daviz_json:
                continue

            try:
                column_types = dict(
                    (key, value.get('columnType',
                                    value.get('valueType', 'text'))
                     if isinstance(value, dict) else value)
                    for key, value in my_json.get('properties', {}).items()
                )
                daviz_json = simplejson.loads(daviz_json(
                    column_types=column_types
                ))
            except Exception, err:
                logger.exception(err)
                continue

            new_json['items'].extend(daviz_json.get('items', []))
            new_json['properties'].update(daviz_json.get('properties', {}))

        # Also add my own daviz-view.json to this json
        new_json['items'].extend(my_json.get('items', []))
        new_json['properties'].update(my_json.get('properties', {}))

        return sortProperties(simplejson.dumps(new_json))
