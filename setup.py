from setuptools import setup, find_packages
import os

version = __import__('dojo').__version__
#version = "2.0"

install_requires = [
    'django',
    'south',
    'django-autoslug',
    'django-tinymce',
    'djangorestframework',
]

setup(
    name = "django-dojo",
    version = version,
    url = 'http://github.com/powellc/django-dojo',
    license = 'BSD',
    platforms=['OS Independent'],
    description = "A learning dojo, the red-hot core of thinkninja.com",
    author = "Colin Powell",
    author_email = 'colin.powell@gmail.com',
    packages=find_packages(),
    install_requires = install_requires,
    include_package_data=True,
    zip_safe=False,
    classifiers = [
        'Development Status :: 4 - Beta',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    package_dir={
        'django-dojo': 'dojo',
    },
)