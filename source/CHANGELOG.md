# Islam Companion Desktop Reader 1.2.0

## New features
  
  * Add all 43 languages to the language menu.
  * Create config files for quran and hadith readers.
  * Update the quran reader so it reads the font and table info from db.
  * Update the quran reader so it reads the font files from a folder.

# Islam Companion Desktop Reader 1.1.0

## Minor bug fixes and improvements

  * Update the path of the db file in qmanager.py and hmanager.py.
  * Update the import statements so the code can be deployed.

# Islam Companion Desktop Reader 1.1.0

## New features

  * The quran and hadith readers need to support English, Arabic and Urdu languages.
  * The pyqtdeploy script does not seem to support sqlite3 Python module. The quran and hadith apis need to be updated so they use QtSql module of PyQt5.
  * The quran and hadith api source code needs to be included with the applications.
  * The quran and hadith api source code needs to be tested using unittest Python module.
  * The source code for all files needs to be commented and documented using Sphinx documentation format. Also parameter type hints should be used for all method parameters.

# Islam Companion Desktop Reader 1.0.0

  * Initial release.