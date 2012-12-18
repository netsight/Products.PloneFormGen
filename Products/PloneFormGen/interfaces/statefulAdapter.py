from zope.interface import Interface


class IStatefulActionAdapter(Interface):
    """ an action adapter that stores values for later editing """

    def getExistingValue(field, request):
        """ retrieve any existing value for the given field """
