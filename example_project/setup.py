from setuptools import setup, find_packages
import os

version = "1.0"

install_requires = [
    'south',
    'django-markdown-deux',
    'django_dynamic_fixture',
]

setup(
    name = "example_project",
    version = version,
    url = '',
    license = 'BSD',
    platforms=['OS Independent'],
    description = "",
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
        'example_project': 'example_project',
    },
)