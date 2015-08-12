from setuptools import setup

try:
    long_description = open('README.md').read()
except IOError:
    long_description = ''

setup(
    name='django-events',
    version='0.1',
    description='A simple event management app',
    license='BSD',
    author='MIET.im team',
    url='https://miet.im/',
    author_email='team@miet.im',
    keywords="django",
    packages=['events'],
    include_package_data=True,
    zip_safe=False,
    platforms=['any'],
    install_requires=[
        'django-enumfield',
        'django-solo',
        'djangorestframework',
        'djangorestframework-camel-case',
    ],
    classifiers=[
        'Framework :: Django',
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Software Development',
        'Topic :: Software Development :: User Interfaces',
    ],
)
