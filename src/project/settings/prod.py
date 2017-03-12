from __future__ import absolute_import, unicode_literals

from .base import *

DEBUG = False

ALLOWED_HOSTS = ['*']

# static path
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'

# using s3 as the storage of static and media files
import csv
# settings of aws authentication, bucket name and domain
AWS_PEM = csv.reader(open('/usr/local/etc/aws_credentials.csv'), delimiter=',')
AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY = next(AWS_PEM)

AWS_HEADERS = {
    'Expires': 'Thu, 31 Dec 2099 20:00:00 GMT',
    'Cache-Control': 'max-age=94608000',
}

AWS_STORAGE_BUCKET_NAME = 'joeyliu-webapps'
AWS_S3_CUSTOM_DOMAIN = '{0}.s3.amazonaws.com'.format(AWS_STORAGE_BUCKET_NAME)

# settings of project name and media path in s3
MEDIAFILES_LOCATION = 'blog/media'

MEDIA_URL = "//{0}/{1}/".format(AWS_S3_CUSTOM_DOMAIN, MEDIAFILES_LOCATION)

# tell boto the place where media files are
DEFAULT_FILE_STORAGE = 'project.settings.custom_path.MediaStorage'

try:
    from .local import *
except ImportError:
    pass
