from setuptools import setup

from vttformatter import __version__ as VERSION

readme = 'README.md'

long_description = open( readme ).read()

config = {

    'description': 'WEBVTT to text converter',

    'long_description': long_description,

    'long_description_content_type': 'text/markdown',

    'name': 'vttformatter',

    'author': 'Georgina L. Wellock',

    'author_email': 'g.l.wellock@bath.ac.uk',

    'packages': ['vttformatter'],

    'url': 'https://github.com/georgiewellock/VTT_formatter',

    'download_url': 'https://github.com/georgiewellock/VTT_formatter/archive/%s.tar.gz' % (VERSION),
    'version': VERSION,

    'install_requires': open( 'requirements.txt' ).read(),

    'license': 'MIT'

}



setup(**config)
