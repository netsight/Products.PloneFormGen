from AccessControl import ClassSecurityInfo

from Products.ATContentTypes.content.base import registerATCT
from Products.Archetypes.public import Schema, StringField, StringWidget
from Products.CMFCore.permissions import View, ModifyPortalContent

from Products.PloneFormGen.config import USE_ENCRYPTION_PERMISSION
from Products.PloneFormGen.content.fields import FGStringField
from Products.PloneFormGen.config import PROJECTNAME
from Products.PloneFormGen import PloneFormGenMessageFactory as _
from Products.PloneFormGen.content.ya_gpg import gpg

ENCRYPTED_VALUE_MARKER = '****ENCRYPTED**VALUE****'


class EncryptionError(Exception):
    pass

encryptedStringFieldSchema = FGStringField.schema.copy()

if gpg is not None:
    encryptedStringFieldSchema = encryptedStringFieldSchema + Schema((
        StringField('gpg_keyid',
                    required=True,
                    accessor='getGPGKeyId',
                    mutator='setGPGKeyId',
                    write_permission=USE_ENCRYPTION_PERMISSION,
                    read_permission=ModifyPortalContent,
                    widget=StringWidget(
                        description=_(u'help_gpg_key_id', default=u"""
                        Give your key-id, e-mail address or
                        whatever works to match a public key from current keyring.
                        It will be used to encrypt the message body (not attachments).
                        Contact the site administrator if you need to
                        install a new public key.
                        Note that you will probably wish to change your message
                        template to plain text if you're using encryption.
                        TEST THIS FEATURE BEFORE GOING PUBLIC!
                        """),
                        label=_(u'label_gpg_key_id', default=u'Key-Id'),
                    ),
                    ),
    ))


class FGEncryptedStringField(FGStringField):
    """ A string entry field that provides encryption support via gpg """
    security = ClassSecurityInfo()

    # Standard content type setup
    portal_type = meta_type = 'FormEncryptedStringField'
    archetype_name = 'Encrypted String Field'
    content_icon = 'EncryptedStringField.gif'
    typeDescription = 'A string field that supports encryption'
    schema = encryptedStringFieldSchema

    def __init__(self, oid, **kwargs):
        """ initialize class """

        FGStringField.__init__(self, oid, **kwargs)
        self.fgField.encrypted = True

    security.declareProtected(View, 'getValue')
    def getValue(self, REQUEST):
        """ get the current value for this field from the request """
        if REQUEST is None:
            return None

        value = REQUEST.get(self.getId())
        if not value:
            return value

        if value == ENCRYPTED_VALUE_MARKER:
            return None

        keyid = getattr(self, 'gpg_keyid')
        value = gpg.encrypt(value, keyid)
        if not value.strip():
            # encryption failed
            raise EncryptionError('Encryption failed.')

        return value

registerATCT(FGEncryptedStringField, PROJECTNAME)
