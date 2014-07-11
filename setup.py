from distutils.core import setup
from archive_manager import __version__

setup(
    name='Archive Manager',
    version=__version__,
    url='https://github.com/univ-of-utah-marriott-library-apple/archive_manager',
    author='Pierce Darragh, Marriott Library IT Services',
    author_email='mlib-its-mac-github@lists.utah.edu',
    description=('Archives items from one location into another, with renaming and depth!'),
    license='MIT',
    packages=['archive_manager'],
    package_dir={'archive_manager': 'archive_manager'},
    scripts=['archiver.py'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Environment :: MacOS X',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: MacOS :: MacOS X',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.8'
    ],
)
