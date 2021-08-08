import sys, os

from PyQt5 import QtCore, QtGui, QtWidgets
from source.qapi import QuranApi

class Ui_Manager():
    """This class is used to add quran data to the user interface.

    Methods
    -------
    initialize_ui()
        Loads the sura, ruku combo boxes, ayat range and the ayat text.
    
    _select_lang()
        Event handler for the language menu items.
     _next_btn_handler()
        Even handler for the next button.
    _prev_btn_handler()
        Even handler for the previous button.    
    _next_ruku()
        Loads the next ruku in the ayat box.
    _prev_ruku()
        Loads the previous ruku in the ayat box.
    _rand_ruku()
        Loads a random ruku in the ayat box.
    _sura_selected()
        It loads the ruku combo box and the ayat box.
    _ruku_selected()
        It loads the ruku combo box and the ayat box.
    _get_current_selection()
        It returns the currently selected sura and ruku.
    _update_layout()
        Sets the file path of the random.png icon to an absolute path.
    _setFont()
        It sets the font for the ayat text box depending on the current
        language.
    _get_text_styles()
        It returns the html styles for the ayat text as a dictionary obj.
    _load_ayat_box()
        It sets the ayat text.
    _load_ayat_range()
        It updates the ayat range label.
    _load_ruku_list()
        It loads the ruku combo box with list of rukus.
    _load_sura_list()
        It loads the sura combo box with list of suras.
    """

    def initialize_ui(self, MainWindow: QtWidgets.QMainWindow) -> None:
        """It initializes the reader layout

        - It loads the sura combo box with list of sura names.
        - It loads the ruku box with list of rukus in the current sura.
        - It displays the range of ayat numbers in the current ruku.
        - It displays quran verses in the text area.
        - It connects the sura and ruku combo boxes to callbacks.
        - It connects the next and previous buttons to callback.
        - It sets the current language to Urdu.

        :param MainWindow: The quran reader window object.
        :type MainWindow: QtWidgets.QMainWindow.
        """

        # The current language
        self.lang = "ur"
        # The absolute path to the database
        db_path = "/usr/local/share/islamcompanion/quran.db"
        # Creates an instance of the QuranApi class
        self.api = QuranApi(db_path, self.lang)
        # The main window object is set as obj attribute
        self.MainWindow = MainWindow

        # Updates the layout of the reader
        self._update_layout()
        # Connects the sura combo box to a call back
        self.MainWindow.suraComboBox.activated.connect(self._sura_selected)
        # Connects the ruku combo box to a call back
        self.MainWindow.rukuComboBox.activated.connect(self._ruku_selected)
        # Connects the next button to a call back
        self.MainWindow.nextButton.clicked.connect(self._next_btn_handler)
        # Connects the prev button to a call back
        self.MainWindow.prevButton.clicked.connect(self._prev_btn_handler)
        # Connects the random button to a call back
        self.MainWindow.randomButton.clicked.connect(self._rand_ruku)
        # Connects the urdu checkbox menu item to a call back
        self.MainWindow.actionUrdu.triggered.connect(self._select_lang)
        # Connects the english checkbox menu item to a call back
        self.MainWindow.actionEnglish.triggered.connect(self._select_lang)
        # Connects the arabic checkbox menu item to a call back
        self.MainWindow.actionArabic.triggered.connect(self._select_lang)
        # Update the language menu so only one item can be selected at a time
        self.MainWindow.langGroup.setExclusive(True)

        # Loads the sura combo box with list of suras
        self._load_sura_list()
        # Loads the ruku combo box with list of rukus
        self._load_ruku_list()
        # Sets the start and end ayat numbers
        self._load_ayat_range()
        # Displays the ayat text
        self._load_ayat_box()

    def _update_layout(self):
        """Sets the file path of the random.png icon to an absolute path.        
        """
        
        # An icon is created
        icon = QtGui.QIcon()
        # The path to the random.png image
        icon.addPixmap(
            QtGui.QPixmap("/usr/local/share/islamcompanion/random.png"), 
            QtGui.QIcon.Normal, QtGui.QIcon.Off)
        # The icon is set
        self.MainWindow.randomButton.setIcon(icon)
        
        
    def _select_lang(self):
        """Event handler for the language menu items.

        It sets the current language to the selected language. It changes the 
        language of the text in the ayat box to the selected language.
        """

        # The translate function
        _translate = QtCore.QCoreApplication.translate

        # The status text and shortcut keys are updated
        self.MainWindow.nextButton.setStatusTip(_translate("MainWindow",
                                                           "Next Ruku (Ctrl+N)"))
        self.MainWindow.nextButton.setShortcut(_translate("MainWindow",
                                                          "Ctrl+N"))
        self.MainWindow.prevButton.setStatusTip(_translate("MainWindow",
                                                           "Previous Ruku (Ctrl+P)"))
        self.MainWindow.prevButton.setShortcut(_translate("MainWindow",
                                                          "Ctrl+P"))

        # If the currently selected language is Urdu
        if self.MainWindow.actionUrdu.isChecked():
            # The current language is set
            self.lang = "ur"
        # If the currently selected language is English
        elif self.MainWindow.actionEnglish.isChecked():
            # The current language is set
            self.lang = "en"
            # The status text and shortcut keys are updated
            self.MainWindow.nextButton.setStatusTip(_translate("MainWindow",
                                                               "Previous Ruku (Ctrl+P)"))
            self.MainWindow.nextButton.setShortcut(_translate("MainWindow",
                                                              "Ctrl+P"))
            self.MainWindow. prevButton.setStatusTip(_translate("MainWindow",
                                                                "Next Ruku (Ctrl+N)"))
            self.MainWindow.prevButton.setShortcut(_translate("MainWindow",
                                                              "Ctrl+N"))
        # If the currently selected language is Arabic
        elif self.MainWindow.actionArabic.isChecked():
            # The current language is set
            self.lang = "ar"

        # The current language is set in the api object
        self.api.set_lang(self.lang)

        # The ayat box is loaded
        self._load_ayat_box()

    def _next_btn_handler(self):
        """Even handler for the next button.

        If the current language is "en", then it calls the _prev_ruku method.
        Otherwise it calls the _next_ruku method.
        """

        # If the current language is "en"
        if self.lang == "en":
            # The _prev_ruku method is called
            self._prev_ruku()
        else:
            # The _next_ruku method is called
            self._next_ruku()

    def _prev_btn_handler(self):
        """Even handler for the prev button.

        If the current language is "en", then it calls the _next_ruku method.
        Otherwise it calls the _prev_ruku method.
        """

        # If the current language is "en"
        if self.lang == "en":
            # The _next_ruku method is called
            self._next_ruku()
        else:
            # The _prev_ruku method is called
            self._prev_ruku()

    def _next_ruku(self):
        """Loads the next ruku in the ayat box.

        It loads the text of next ruku to ayat box.
        It also loads the sura and ruku combo boxes.
        It also updates the ayat range.
        """

        # The current selection
        selection = self._get_current_selection()
        next_sura = selection["sura"]
        next_ruku = selection["ruku"]

        # If the current ruku is not the last one in the ruku combo box
        if selection["ruku"] < self.MainWindow.rukuComboBox.count():
            next_ruku += 1
        # If the current ruku is the last one in the ruku combo box
        else:
            # The next ruku is set to 1
            next_ruku = 1
            # The sura is set to the next one
            next_sura += 1
            # If the next sura number is out of range
            if next_sura > self.MainWindow.suraComboBox.count():
                # The next sura is set to 1
                next_sura = 1
            # The current sura is set
            self.MainWindow.suraComboBox.setCurrentIndex(next_sura-1)
            #  The ruku combo box is loaded
            self._load_ruku_list()

        # The current ruku is selected
        self.MainWindow.rukuComboBox.setCurrentIndex(next_ruku-1)
        # The ayat range is updated
        self._load_ayat_range()
        # The ayat box is loaded
        self._load_ayat_box()

    def _prev_ruku(self):
        """Loads the prev ruku in the ayat box.

        It loads the text of previous ruku to ayat box.
        It also loads the sura and ruku combo boxes.
        It also updates the ayat range.
        """

        # The current selection is fetched
        selection = self._get_current_selection()
        # The previous sura
        prev_sura = selection["sura"]
        # The previous ruku
        prev_ruku = selection["ruku"]

        # If a ruku is currently selected
        if selection["ruku"] > 1:
            # The previous ruku is set
            prev_ruku -= 1
        # If a ruku is not currently selected
        else:
            # The previous ruku is set
            prev_sura -= 1
            # If the previous sura id is less than 1
            if prev_sura < 1:
                # The previous sura is set to the last sura
                prev_sura = 114
            # The current sura is updated
            self.MainWindow.suraComboBox.setCurrentIndex(prev_sura-1)
            # The ruku list is updated
            self._load_ruku_list()
            # The number of items in the ruku combo box
            prev_ruku = self.MainWindow.rukuComboBox.count()

        # The current ruku is updated
        self.MainWindow.rukuComboBox.setCurrentIndex(prev_ruku-1)
        # The ayat range is updated
        self._load_ayat_range()
        # The ayat box is updated
        self._load_ayat_box()

    def _rand_ruku(self):
        """Loads a random ruku in the ayat box.

        It loads the text of a random ruku to ayat box.
        It also loads the sura and ruku combo boxes and updates the ayat range.
        """

        # A random sura is fetched
        ruku_details = self.api.get_random_ruku()
        # The sura is selected
        self.MainWindow.suraComboBox.setCurrentIndex(
            ruku_details["sura"]-1)
        # The ruku list box is loaded
        self._load_ruku_list()
        # The ruku is selected in the ruku combo box
        self.MainWindow.rukuComboBox.setCurrentIndex(
            ruku_details["sura_ruku"]-1)
        self._load_ayat_range()
        self._load_ayat_box()

    def _sura_selected(self):
        """It loads the ruku combo box and the ayat box
        """
        self._load_ruku_list()
        self._load_ayat_range()
        self._load_ayat_box()

    def _ruku_selected(self):
        """It loads the ruku combo box and the ayat box
        """
        self._load_ayat_range()
        self._load_ayat_box()

    def _get_current_selection(self):
        """It returns the currently selected sura and ruku.

        It also returns the start and end ayat numbers. The sura data includes
        the sura short name and number

        :return: The selected sura, ruku and ayat numbers.
        :rtype: dict.        
        """

        # If the sura combo box contains items
        if self.MainWindow.suraComboBox.count() > 0:
            # The selected sura data is fetched
            sura = self.MainWindow.suraComboBox.currentData()
            # The sura id is converted to int
            sura = int(sura)
            # The sura text in English
            stext = self.MainWindow.suraComboBox.currentText().split(" (")
            stext = stext[0]
        else:
            # The default sura data
            sura = 1
            stext = "Al-Faatiha"

        # If the ruku combo box contains items
        if self.MainWindow.rukuComboBox.count() > 0:
            # The selected ruku data is fetched
            ruku = self.MainWindow.rukuComboBox.currentData()
            # The ruku id is converted to int
            ruku = int(ruku)
        else:
            # The default ruku data
            ruku = 1

        # The ayat range data is parsed
        text = self.MainWindow.ayatRange.text()
        text = text.replace("Ayas ", "").split(" - ")
        # The start ayat number
        start = int(text[0])
        # The end ayat number
        end = int(text[1])

        # The current data in the quran reader
        sel = {
            "sura": sura,
            "ruku": ruku,
            "start": start,
            "end": end,
            "stext": stext
        }

        return sel

    def _setFont(self):
        """It sets the font for the ayat text box depending on the current
        language.
        """

        # The font object
        font = QtGui.QFont()
        # If the current language is English
        if self.lang == "en":
            font.setFamily("Sans Serif")
            font.setPointSize(12)
        else:
            font.setFamily("Nafees [PYRS]")
            font.setPointSize(18)
            font.setWeight(50)

        font.setBold(False)
        # The font is set
        self.MainWindow.ayatText.setFont(font)

    def _get_text_styles(self):
        """It returns the html styles for the ayat text as a dictionary obj.

        It returns the style for the outer and inner list tags and the caption
        text.

        :return: The html styles for the hadith text.
        :rtype: dict.
        """

        # The margin style for the ayat text
        os = "margin-left: 25px;"
        os = os + "list-style-type: none;"
        # The style for the green text
        cs = "color:green;font-size: 12pt;font-weight: bold;"
        # The style for the list elements
        ls = "line-height:50px; padding-bottom: 20px;"
        # If the language is english
        if self.lang == "en":
            # The style for the green text
            cs = "color:green;font-size: 10pt;font-weight: bold;"
            # The margin style for the ayat text
            os = "margin-right: 10px;margin-left: -20px;"
            os = os + "list-style-type: none;"
            # The style for the list elements
            ls = "line-height:40px; padding-bottom: 20px"
        # The required styles
        styles = {"os": os, "ls": ls, "cs": cs}

        return styles

    def _load_ayat_box(self):
        """It sets the ayat text
        """

        # The font for the ayat text is set
        self._setFont()
        # The styles for the ayat box
        styles = self._get_text_styles()

        # The current ruku and ayat selection
        sel = self._get_current_selection()
        # The ayat text is fetched
        ayat_list = self.api.get_ayat_text(sel["sura"], sel["ruku"])
        # The start ayat number
        aya = sel["start"]
        # The html list for the ayat text
        text = "<ol style='" + styles["os"] + "'>"
        # Each list item is added to the list
        for line in ayat_list:
            text += "<li style='" + styles["ls"] + "'>" + line
            text += " <br/><span style='" + styles["cs"] + "'>("
            text += sel["stext"] + " " + str(sel["sura"]) + ":"
            text += str(aya) + ")</span></li>"
            # The ayat count is increased by 1
            aya += 1
        # The closing tag for the html list
        text += "</ol>"

        # The html list is displayed
        self.MainWindow.ayatText.setHtml(text)

    def _load_ayat_range(self):
        """It updates the ayat range label.

        It sets the start and end ayat values to the label.
        """

        # The current sura and ruku selection is fetched
        sel = self._get_current_selection()

        # The ayat range data is fetched
        ayat_data = self.api.get_ayat_range(sel["sura"], sel["ruku"])
        # The ayat range text
        text = str(ayat_data["start"]) + " - " + str(ayat_data["end"])
        text = "Ayas " + text
        # The ayat range text is set
        self.MainWindow.ayatRange.setText(text)

    def _load_ruku_list(self):
        """It loads the ruku combo box with list of rukus.

        It fetches number of rukus in the selected sura. It loads the ruku
        combo box with list of rukus.
        """

        # The ruku combo box is cleared
        self.MainWindow.rukuComboBox.clear()
        # If the sura combo box has items
        if self.MainWindow.suraComboBox.count() > 0:
            # The sura comb box data
            sura = self.MainWindow.suraComboBox.currentData()
            sura = int(sura)
        else:
            sura = 1
        # The ruku count is fetched
        ruku_count = self.api.get_ruku_count(sura)
        # For each ruku number
        for i in range(1, (ruku_count+1)):
            # The ruku number
            ruku = (str(i))
            # The ruku number is added to the combo box
            self.MainWindow.rukuComboBox.addItem(ruku, ruku)

    def _load_sura_list(self):
        """It loads the sura combo box with list of suras.

        It fetches list of sura names from database. It loads the sura combo
        box with sura names.
        """

        # The loop counter
        count = 1
        # The sura names are fetched
        sura_list = self.api.get_sura_names()
        # Each sura is added to the sura combo box
        for i in sura_list:
            # The sura is added
            self.MainWindow.suraComboBox.addItem(i, count)
            # The loop counter is increased
            count += 1
