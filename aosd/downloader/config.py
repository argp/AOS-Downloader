import sys
sys.path.append('.')
sys.path.append('..')

from helpers.logging_helper import logging_helper

try:
    import urllib.parse as comp_urlparse # For Python 3.0 and later
except ImportError:
    import urlparse as comp_urlparse # Fall back to Python 2's urllib2

import plistlib
import os

from .utilities import utilities

class config(object):

    @classmethod
    def read(cls):
        config_contents = {}
        config_plist_path = utilities.getconfigurationplistpath()
        if os.path.exists(config_plist_path) == False:
            logging_helper.getLogger().error('Fatal error, cannot locate the configuration plist. Use the "config defaults" command to restore defaults.')
        else:
            config_contents = plistlib.readPlist(config_plist_path)
        return config_contents

    @classmethod
    def write(cls, new_settings):
        config_plist_path = utilities.getconfigurationplistpath()
        plistlib.writePlist(new_settings, config_plist_path)

    @classmethod
    def getUpdateURL(cls):
        settings = cls.read()
        return settings['core_url']

    @classmethod
    def setUpdateURL(cls, url):
        settings = cls.read()
        new_url = comp_urlparse.urlparse(url)
        if bool(new_url.scheme) == True:
            settings['core_url'] = url
            cls.write(settings)
        else:
            logging_helper.getLogger().error('The supplied URL is not valid (lacks a scheme).')

    @classmethod
    def getDownloadDir(cls):
        settings = cls.read()
        return os.path.expanduser(settings['download_directory'])

    @classmethod
    def setDownloadDir(cls, download_dir):
        download_dir = os.path.expanduser(download_dir)
        settings = cls.read()

        try:
            os.makedirs(download_dir)
        except OSError:
            pass

        if os.path.exists(download_dir) == True:
            settings['download_directory'] = download_dir
            cls.write(settings)
        else:
            logging_helper.getLogger().error('the directory specified "'+download_dir+'" does not exist, please create it first.')

    @classmethod
    def getVerboseLogging(cls):
        settings = cls.read()
        return settings['verbose_logging']

    @classmethod
    def setVerboseLogging(cls, enable):
        settings = cls.read()
        is_enabled = settings['verbose_logging']
        if enable in ['True', 'TRUE', 'true']:
            is_enabled = True
        elif enable in ['False', 'FALSE', 'false']:
            is_enabled = False
        else:
            logging_helper.getLogger().error('the value passed "'+enable+'" must be "True" or "False".')
        settings['verbose_logging'] = is_enabled
        cls.write(settings)

    @classmethod
    def getUseHTTPS(cls):
        settings = cls.read()
        return settings['requests_via_https']

    @classmethod
    def setUseHTTPS(cls, enable):
        settings = cls.read()
        is_enabled = settings['requests_via_https']
        if enable in ['True', 'TRUE', 'true']:
            is_enabled = True
        elif enable in ['False', 'FALSE', 'false']:
            is_enabled = False
        else:
            logging_helper.getLogger().error('the value passed "'+enable+'" must be "True" or "False".')
        settings['requests_via_https'] = is_enabled
        cls.write(settings)

    @classmethod
    def toggleFirstRun(cls):
        settings = cls.read()
        value = settings['first_run']
        if value == True:
            settings['first_run'] = False
            cls.write(settings)

    @classmethod
    def getFirstRun(cls):
        settings = cls.read()
        return settings['first_run']

    @classmethod
    def defaults(cls):
        default_values = {
            'core_url': 'https://raw.githubusercontent.com/samdmarshall/AOS-Downloader/master/aosd/data/',
            'first_run': True,
            'requests_via_https': True,
            'download_directory': '/home/argp/archive/osx/kernel',
            'verbose_logging': False,
        }
        cls.write(default_values)

# EOF
