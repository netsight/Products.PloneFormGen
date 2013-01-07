from zope.interface import Interface


class IStatefulActionAdapter(Interface):
    """ an action adapter that stores values for later editing """

    def hasExistingValuesFor(userkey):
        """ are there existing submission values for the given userkey? """

    def getExistingValueFor(field, userkey):
        """ retrieve any existing value for the given userkey and field"""

    def isFinalised(userkey):
        """ has the given user's submission been finalised? (no longer editable)"""
