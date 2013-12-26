#!/usr/bin/env python

from setuptools import setup, find_packages
version = '0.0.1'

if __name__ == '__main__':
    setup(name='dynamic_model_classes',
          version=version,
          description='Creates dynamicaly model classes in memory',
          author='Sergey Duka',
          author_email='sergey.duka@gmail.com',
          url='https://github.com/boooka/dynamic_model_classes/',
          packages=find_packages(),
          license='GPL',
          classifiers=[
              "Intended Audience :: Developers",
              "License :: OSI Approved :: GNU General Public License (GPL)",
              "Natural Language :: English",
              "Programming Language :: Python",
              "Topic :: Software Development :: Libraries :: Python Modules",
              ],
          install_requires = ['pyyaml', 'annoying'],
          package_data = {'dynamic_model_classes.views': ['templates/*.html'] },
          include_package_data = True,
          )

