from zope.interface import Interface


class IStatefulActionAdapter(Interface):
    """ an action adapter that stores values for later editing """

    def getExistingValue(field, userkey):
        """ retrieve any existing value for the given field and user"""

    def hasExistingValues(userkey):
        """ are there existing submission values for the given user? """
