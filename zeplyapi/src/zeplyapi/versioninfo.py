class VersionInfo:
    PRODUCT = "zeplyapi"
    VERSION = (0, 3, 0)
    COMPANY = "None"
    COPYRIGHT = "Apache GNU License 2.0"
    TRADEMARKS = ''
    DESCRIPTION = 'API for creating and retrieving blockchain addresses'
    COMMENTS = ''

    @staticmethod
    def version():
        return '.'.join(str(x) for x in VersionInfo.VERSION)

VERSION = VersionInfo.version()