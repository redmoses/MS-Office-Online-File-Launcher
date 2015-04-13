from setuptools import setup

setup(name='poom',
      version='0.0.4',
      description='Open office documents with Microsoft Office Online',
      long_description="This is primarily a Dropbox app and acts as a Dropbox client."
                       " The app doesn't have any permission over your existing Dropbox files."
                       " So when you open a document with the app it first uploads the file to"
                       " its own directory on your Dropbox and then opens the file from there"
                       " using the Microsoft Office online edition. The app supports both way syncing."
                       "Once you've edited the file in Dropbox the changes are going to be temporarily"
                       " saved there. The next time you open the same file using this app it will show"
                       " you the last modified version of the file, meaning if the file was last modified"
                       " on Dropbox it will open the Dropbox version and sync your local file and vice versa.",
      classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Topic :: Utilities',
        'Environment :: Console',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux'
      ],
      keywords='dropbox, microsoft office, office online',
      url='http://redmoses.github.io/poom/',
      author='Red Moses',
      author_email='musa@redmoses.me',
      maintainer='redmoses',
      maintainer_email='musa@redmoses.me',
      license='MIT',
      packages=['poom'],
      install_requires=['dropbox', 'pytz', 'tzlocal', 'python-dateutil'],
      entry_points = {
        'console_scripts': ['poom=poom.app:run'],
      },
      platforms=['Linux'],
      include_package_data=True,
      zip_safe=False)
