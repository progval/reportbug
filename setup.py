#!/usr/bin/env python

from setuptools import setup
import reportbug
import os
import glob

# i18n = []
# for lang in glob.glob('*.po'):
#     lang = lang[:-3]
#     if lang == 'messages':
#         continue
#     i18n.append( ('share/locale/%s/LC_MESSAGES' % lang,
#                   ['i18n/%s/LC_MESSAGES/foomatic-gui.mo' % lang]) )

setup(name='reportbug', version=reportbug.VERSION_NUMBER,
      description='bug reporting tool',
      author='reportbug maintainence team',
      author_email='reportbug-maint@lists.alioth.debian.org',
      url='http://alioth.debian.org/projects/reportbug',
      data_files=[('share/reportbug', ['share/handle_bugscript',
                                       'share/reportbug.el',
                                       'share/debian-swirl.svg']),
                  ('share/bug/reportbug', ['share/presubj', 'share/script'])],
      license='MIT',
      packages=['reportbug','reportbug.ui'],
      scripts=['bin/reportbug', 'bin/querybts'])
