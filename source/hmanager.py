import sys, os
from random import randint

from PyQt5 import QtCore, QtGui, QtWidgets

from source.hapi import HadithApi
from source.hconfig import HConfig

class Ui_Manager():
    """
    This class is used to add hadith data to the user interface.

    Methods
    -------
    initialize_ui()
        Loads the source, book and title combo boxes and the hadith text.
    
    _update_btn_icon()
        Updates the path to the random icon to an absolute path.       
    _update_layout()
        Updates the layout of the hadith reader so it supports the current
        language.
    _select_lang()
        Event handler for the language menu items.
    _next_btn_handler()
        Even handler for the next button.
    _prev_btn_handler()
        Even handler for the previous button.
    _rand_hadith()
        Loads a random hadith in the hadith box.
    _next_hadith()
        Loads the next hadith.
    _prev_hadith()
        Loads the previous hadith.
    _source_selected()
        It loads the book and title combo boxes and also the hadith box.
    _book_selected()
        It loads the title combo box and the hadith box.
    _get_current_selection()
        It returns the currently selected source, book and title.
    _load_hadith()
        It updates the hadith box with the current hadith.
    _load_source_list()
        It loads the source combo box with list of sources.
    _load_book_list()
        It loads the book combo box with list of books.
    _load_title_list()
        It loads the title combo box with list of titles for the selected
        hadith source and book.
    _update_settings()
        It saves the current settings to database.
    _load_settings()
        It loads the current settings from database.    
    """

    def initialize_ui(self, MainWindow: QtWidgets.QMainWindow) -> None:
        """It initializes the reader layout.
        
        - It loads the source combo box with list of hadith sources.
        - It loads the book combo box with books in the current hadith source.
        - It loads the title combo box with titles in the current hadith source
          and book.
        - It displays hadith verses in the text area.
        - It connects the source, book and title combo boxes to callbacks.
        - It connects the next and previous buttons to callbacks.
        - It sets the current language to Urdu.
        
        :param MainWindow: The hadith reader window object.
        :type MainWindow: QtWidgets.QMainWindow.
        """
        
        # The application configuration
        hconfig       = HConfig()
        self.config   = hconfig.get_config()    
        # The current language
        self.lang     = self.config["default_lang"]
        # Creates an instance of the HadithApi class
        self.api = HadithApi(self.config["db_path"], self.lang)
        # Loads settings from database
        self._load_settings()
        # The main window object is set as obj attribute
        self.MainWindow = MainWindow
        
        # The layout is updated for the new language
        self._update_layout()
        # Connects the source combo box to a call back
        self.MainWindow.sourceComboBox.activated.connect(self._source_selected)
        # Connects the book combo box to a call back
        self.MainWindow.bookComboBox.activated.connect(self._book_selected)
        # Connects the title combo box to a call back
        self.MainWindow.titleComboBox.activated.connect(self._load_hadith_box)
        # Connects the next button to a call back
        self.MainWindow.nextButton.clicked.connect(self._next_btn_handler)
        # Connects the prev button to a call back
        self.MainWindow.prevButton.clicked.connect(self._prev_btn_handler)        
        # Connects the random button to a call back
        self.MainWindow.randomButton.clicked.connect(self._rand_hadith)        
        # Connects the urdu checkbox menu item to a call back
        self.MainWindow.actionUrdu.triggered.connect(self._select_lang)
        # Connects the english checkbox menu item to a call back
        self.MainWindow.actionEnglish.triggered.connect(self._select_lang)
        # Connects the arabic checkbox menu item to a call back
        self.MainWindow.actionArabic.triggered.connect(self._select_lang)
        # Update the language menu so only one item can be selected at a time
        self.MainWindow.langGroup.setExclusive(True)
        
        # Updates the icon path
        self._update_btn_icon()          
        # Loads the source combo box with list of sources
        self._load_source_list()
        # Loads the book combo box with list of books
        self._load_book_list()
        # Loads the title combo box with list of titles
        self._load_title_list()
        # Displays the hadith text
        self._load_hadith_box()        

    def _update_btn_icon(self) -> None:
        """Updates the path to the random icon to an absolute path.
        """
        
        # An icon is created
        icon = QtGui.QIcon()
        # The path to the random.png image
        icon.addPixmap(
            QtGui.QPixmap(self.config["random_icon_path"]), 
            QtGui.QIcon.Normal, QtGui.QIcon.Off)
        # The icon is set
        self.MainWindow.randomButton.setIcon(icon)        
        
    def _update_layout(self) -> None:
        """Updates the layout of the hadith reader so it supports the current
        language.
        
        The position of the combo boxes, labels and buttons is updated. The
        locale and alignment of the combo boxes is also updated.  

        The current language in the language menu is checked 
        """

        # If the current language is "English"
        if self.lang == "English":
            # The English option is selected
            self.MainWindow.actionEnglish.setChecked(True)
            # The position of the combo boxes is updated
            self.MainWindow.gridLayout.addWidget(
                self.MainWindow.bookComboBox, 5, 1, 1, 1)
            self.MainWindow.gridLayout.addWidget(
                self.MainWindow.sourceComboBox, 5, 0, 1, 1)
            self.MainWindow.gridLayout.addWidget(
                self.MainWindow.titleComboBox, 5, 2, 1, 1)

            self.MainWindow.gridLayout.addWidget(
                self.MainWindow.sourceLabel, 2, 0, 1, 1)
            self.MainWindow.gridLayout.addWidget(
                self.MainWindow.bookLabel, 2, 1, 1, 1)
            self.MainWindow.gridLayout.addWidget(
                self.MainWindow.titleLabel, 2, 2, 1, 1)

            self.MainWindow.gridLayout.addWidget(
                self.MainWindow.prevButton, 5, 8, 1, 1)
            self.MainWindow.gridLayout.addWidget(
                self.MainWindow.randomButton, 5, 9, 1, 1)
            self.MainWindow.gridLayout.addWidget(
                self.MainWindow.nextButton, 5, 7, 1, 1)                      
                
            # The direction of the combo boxes is updated
            self.MainWindow.bookComboBox.setLayoutDirection(
                QtCore.Qt.LeftToRight)
            self.MainWindow.bookComboBox.setLocale(
                QtCore.QLocale(
                    QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
            
            self.MainWindow.titleComboBox.setLayoutDirection(
                QtCore.Qt.LeftToRight)
            self.MainWindow.titleComboBox.setLocale(
                QtCore.QLocale(
                    QtCore.QLocale.English, QtCore.QLocale.UnitedStates))                
                
            self.MainWindow.sourceComboBox.setLayoutDirection(
                QtCore.Qt.LeftToRight)
            self.MainWindow.sourceComboBox.setLocale(
                QtCore.QLocale(
                    QtCore.QLocale.English, QtCore.QLocale.UnitedStates))      
                
            # The font for the combo boxes is updated
            font = QtGui.QFont()
            font.setFamily("DejaVu Sans")
            font.setPointSize(10)
            font.setBold(True)
            
            self.MainWindow.bookComboBox.setFont(font)
            self.MainWindow.titleComboBox.setFont(font)
            self.MainWindow.sourceComboBox.setFont(font)
            font.setBold(False)
            font.setPointSize(12)
            self.MainWindow.hadithText.setFont(font)
            
        else:
            # If the language is Urdu
            if self.lang == "Urdu":
                self.MainWindow.actionUrdu.setChecked(True)
            else:
                self.MainWindow.actionArabic.setChecked(True)
            # The position of the combo boxes is updated
            self.MainWindow.gridLayout.addWidget(
                self.MainWindow.bookComboBox, 5, 9, 1, 1)
            self.MainWindow.gridLayout.addWidget(
                self.MainWindow.sourceComboBox, 5, 10, 1, 1)
            self.MainWindow.gridLayout.addWidget(
                self.MainWindow.titleComboBox, 5, 5, 1, 1)

            self.MainWindow.gridLayout.addWidget(
                self.MainWindow.sourceLabel, 2, 10, 1, 1)
            self.MainWindow.gridLayout.addWidget(
                self.MainWindow.bookLabel, 2, 9, 1, 1)
            self.MainWindow.gridLayout.addWidget(
                self.MainWindow.titleLabel, 2, 5, 1, 1)

            self.MainWindow.gridLayout.addWidget(
                self.MainWindow.randomButton, 5, 4, 1, 1)
            self.MainWindow.gridLayout.addWidget(
                self.MainWindow.nextButton, 5, 1, 1, 1)
            self.MainWindow.gridLayout.addWidget(
                self.MainWindow.prevButton, 5, 3, 1, 1)
                
            # The layout of the combo boxes is updated
            self.MainWindow.bookComboBox.setLayoutDirection(
                QtCore.Qt.RightToLeft)
            self.MainWindow.bookComboBox.setLocale(
                QtCore.QLocale(QtCore.QLocale.Urdu, QtCore.QLocale.Pakistan))
            
            self.MainWindow.titleComboBox.setLayoutDirection(
                QtCore.Qt.RightToLeft)
            self.MainWindow.titleComboBox.setLocale(
                QtCore.QLocale(QtCore.QLocale.Urdu, QtCore.QLocale.Pakistan))                
                
            self.MainWindow.sourceComboBox.setLayoutDirection(
                QtCore.Qt.RightToLeft)
            self.MainWindow.sourceComboBox.setLocale(
                QtCore.QLocale(QtCore.QLocale.Urdu, QtCore.QLocale.Pakistan))
                
            # The font of the combo boxes is updated
            font = QtGui.QFont()
            font.setFamily("Nafees [PYRS]")
            font.setPointSize(14)
            font.setBold(False)
            font.setWeight(50)
            
            self.MainWindow.bookComboBox.setFont(font)
            self.MainWindow.titleComboBox.setFont(font)
            self.MainWindow.sourceComboBox.setFont(font)
            font.setPointSize(18)
            self.MainWindow.hadithText.setFont(font)
            
    def _select_lang(self) -> None:
        """Event handler for the language menu items.
        
        It sets the current language to the selected language. It changes the 
        language of the text in the hadith box to the selected language.
        """
        # The translate function
        _translate = QtCore.QCoreApplication.translate
        
        # The status text and shortcut keys are updated
        self.MainWindow.nextButton.setStatusTip(_translate("MainWindow", 
            "Next Hadith (Ctrl+N)"))
        self.MainWindow.nextButton.setShortcut(_translate("MainWindow", 
            "Ctrl+N"))
        self.MainWindow.prevButton.setStatusTip(_translate("MainWindow", 
            "Previous Hadith (Ctrl+P)"))
        self.MainWindow.prevButton.setShortcut(_translate("MainWindow", 
            "Ctrl+P"))
        
        # If the currently selected language is Urdu
        if self.MainWindow.actionUrdu.isChecked():
            # The current language is set
            self.lang = "Urdu"
        # If the currently selected language is English
        elif self.MainWindow.actionEnglish.isChecked():
            # The current language is set
            self.lang = "English"
            # The status text and shortcut keys are updated
            self.MainWindow.nextButton.setStatusTip(_translate("MainWindow", 
                "Previous Hadith (Ctrl+P)"))
            self.MainWindow.nextButton.setShortcut(_translate("MainWindow", 
                "Ctrl+P"))
            self.MainWindow. prevButton.setStatusTip(_translate("MainWindow", 
                "Next Hadith (Ctrl+N)"))
            self.MainWindow.prevButton.setShortcut(_translate("MainWindow", 
                "Ctrl+N"))                               
        # If the currently selected language is Arabic
        elif self.MainWindow.actionArabic.isChecked():
            # The current language is set
            self.lang = "Arabic"
            
        # The layout is updated for the new language
        self._update_layout()
                    
        # The current language is set in the api object
        self.api.set_lang(self.lang)
        
        # Loads the source combo box with list of sources
        self._load_source_list()
        # Loads the book combo box with list of books
        self._load_book_list()
        # Loads the title combo box with list of titles
        self._load_title_list()
        # Loads the hadith box with text
        self._load_hadith_box()
         # The settings are updated in database
        self._update_settings()
        
    def _next_btn_handler(self) -> None:
        """Even handler for the next button.
        
        If the current language is "en", then it calls the _prev_hadith method.
        Otherwise it calls the _next_hadith method.
        """
        
        # If the current language is "English"
        if self.lang == "English":
            # The _prev_hadith method is called
            self._prev_hadith()
        else:
            # The _next_hadith method is called
            self._next_hadith()    
         # The settings are updated in database
        self._update_settings()        
            
    def _prev_btn_handler(self) -> None:
        """Even handler for the prev button.
        
        If the current language is "English", then it calls the _next_hadith
        method. Otherwise it calls the _prev_hadith method.
        """
        
        # If the current language is "English"
        if self.lang == "English":
            # The _next_hadith method is called
            self._next_hadith()
        else:
            # The _prev_hadith method is called
            self._prev_hadith()
         # The settings are updated in database
        self._update_settings()  
                    
    def _rand_hadith(self) -> None:
        """Loads a random hadith in the hadith box.
        
        It loads the text of a random hadith to hadith box.
        It also loads the source, book and title combo boxes.
        """
    
        # The number of hadith sources
        scount  = self.MainWindow.sourceComboBox.count()
        # A random source index
        sindex  = randint(0, scount-1)
        # The current index of source combo box is set
        self.MainWindow.sourceComboBox.setCurrentIndex(sindex)
        
        # The book list is loaded
        self._load_book_list()
        # The number of hadith books
        bcount  = self.MainWindow.bookComboBox.count()
        # A random book index
        bindex  = randint(0, bcount-1)
        # The current index of book combo box is set
        self.MainWindow.bookComboBox.setCurrentIndex(bindex)
        
        # The title list is loaded
        self._load_title_list()
        # The number of hadith titles
        tcount  = self.MainWindow.titleComboBox.count()
        # A random book title
        tindex  = randint(0, tcount-1)
        # The current index of title combo box is set
        self.MainWindow.titleComboBox.setCurrentIndex(tindex)
        
        # The hadith text box is loaded
        self._load_hadith_box()
         # The settings are updated in database
        self._update_settings()
                            
    def _next_hadith(self) -> None:
        """Loads the next hadith.
        
        It loads the text of next hadith to hadith box.
        It also loads the source, title and book combo boxes if needed.
        """

        # The current selection
        sel     = self._get_current_selection()
        
        # The index of the current item in the title combo box
        ctindex = self.MainWindow.titleComboBox.currentIndex()
        # The number of items in the title combo box
        tcount  = self.MainWindow.titleComboBox.count()
        
        # The index of the current item in the book combo box
        cbindex = self.MainWindow.bookComboBox.currentIndex()
        # The number of items in the book combo box
        bcount  = self.MainWindow.bookComboBox.count()
        
        # The index of the current item in the source combo box
        csindex = self.MainWindow.sourceComboBox.currentIndex()
        # The number of items in the source combo box
        scount  = self.MainWindow.sourceComboBox.count()        
        
        # If the currently selected title is the last one
        if ctindex == (tcount-1):
            # If the currently selected book is the last one
            if cbindex == (bcount-1):
                # If the currently selected source is the last one
                if csindex == (scount-1):
                    # The currently selected item in the source combo box is
                    # set to the first one
                    self.MainWindow.sourceComboBox.setCurrentIndex(0)
                else:
                    # The currently selected item in the source combo box is
                    # set to the next one
                    self.MainWindow.sourceComboBox.setCurrentIndex(csindex+1)
                # The book combo box is updated
                self._load_book_list()
                # The title combo box is updated
                self._load_title_list()
            else:
                # The book combo box selected item is updated
                self.MainWindow.bookComboBox.setCurrentIndex(cbindex+1)
            # The title combo box is loaded
            self._load_title_list()
        else:
            # The currently selected item in the title combo box is set
            self.MainWindow.titleComboBox.setCurrentIndex(ctindex+1)
        # The hadith box is loaded
        self._load_hadith_box()            
        
    def _prev_hadith(self) -> None:
        """Loads the previous hadith.
        
        It loads the text of previous hadith to hadith box.
        It also loads the source, title and book combo boxes.
        """

        # The current selection
        sel     = self._get_current_selection()
        
        # The index of the current item in the title combo box
        ctindex = self.MainWindow.titleComboBox.currentIndex()
        # The number of items in the title combo box
        tcount  = self.MainWindow.titleComboBox.count()
        
        # The index of the current item in the book combo box
        cbindex = self.MainWindow.bookComboBox.currentIndex()
        # The number of items in the book combo box
        bcount  = self.MainWindow.bookComboBox.count()
        
        # The index of the current item in the source combo box
        csindex = self.MainWindow.sourceComboBox.currentIndex()
        # The number of items in the source combo box
        scount  = self.MainWindow.sourceComboBox.count()          
        
        # If the currently selected title is the last one
        if ctindex == 0:
            # If the currently selected book is the last one
            if cbindex == 0:
                # If the currently selected source is the last one
                if csindex == 0:
                    self.MainWindow.sourceComboBox.setCurrentIndex(scount-1)
                else:
                    # The currently selected item in the source combo box is set
                    # to the previous one
                    self.MainWindow.sourceComboBox.setCurrentIndex(csindex-1)
                # The book combo box is loaded
                # The title combo box is loaded
                self._load_book_list()
                self._load_title_list()                    
            else:
                # The book combo box selected item is set to the previous one
                self.MainWindow.bookComboBox.setCurrentIndex(cbindex-1)
            # The title combo box is loaded
            self._load_title_list()                
        else:
            # The title combo box selected item is set to the previous one
            self.MainWindow.titleComboBox.setCurrentIndex(ctindex-1)

        # The hadith text box is loaded
        self._load_hadith_box() 
                    
    def _source_selected(self) -> None:
        """It loads the book and title combo boxes and also the hadith box.
        """
        
        # The book combo box is loaded
        self._load_book_list()
        # The title combo box is loaded
        self._load_title_list()
        # The hadith text box is loaded
        self._load_hadith_box()
         # The settings are updated in database
        self._update_settings()   
        
    def _book_selected(self) -> None:
        """It loads the title combo box and the hadith box.
        """

        # The title combo box is loaded
        self._load_title_list()
        # The hadith text box is loaded
        self._load_hadith_box()
         # The settings are updated in database
        self._update_settings()
        
    def _get_current_selection(self) -> dict:
        """It returns the currently selected source, book and title.
        
        :return: The selected source, book and title.
        :rtype: dict.            
        """
        
        # If the source combo box contains items
        if self.MainWindow.sourceComboBox.count() > 0:
            # The currently selected source
            source    = self.MainWindow.sourceComboBox.currentText()
        else:
            # The selected source is set to empty
            source    = ""

        # If the book combo box contains items
        if self.MainWindow.bookComboBox.count() > 0:
            # The position of the currently selected book
            book      = self.MainWindow.bookComboBox.currentData()
            book      = int(book)
        else:
            # The position of the currently selected book is set to 1
            book      = 1
            
        # If the title combo box contains items
        if self.MainWindow.titleComboBox.count() > 0:        
            # The position of the currently selected title
            title = self.MainWindow.titleComboBox.currentData()
            title = int(title)
            # The text of the currently selected title
            ttext = self.MainWindow.titleComboBox.currentText()
        else:
            # The position of the currently selected title is set to 1
            title = 1
            # The text of the currently selected title is set to empty
            ttext = "";
        
        # The currently selected items
        selection = {
                      "source": source,
                      "book": book,
                      "title": title,
                      "ttext": ttext
        }
        
        return selection

    def _load_hadith_box(self) -> None:
        """It updates the hadith box with the current hadith.
        """
        
        # The current selection
        sel   = self._get_current_selection()
        # The hadith text is fetched
        htext = self.api.get_hadith_text(sel["title"])
        # The style for the hadith text
        style = "margin: 15px; padding-top: 20px;"
        style += "line-height:50px; padding-bottom: 20px";
        text  = "<div style='" + style + "'>"
        text  += "<div style='color: green;'>" 
        text  += sel["ttext"] + "</div><br/>"
        text += htext
        text += "</div>"
        # The hadith text html is set
        self.MainWindow.hadithText.setHtml(text)
        # The settings are updated in database
        self._update_settings()
                
    def _load_source_list(self) -> None:
        """It loads the source combo box with list of sources.
        
        It fetches list of source names from database.
        It loads the source combo box with source names.
        """
        
        # The source combo box is cleared
        self.MainWindow.sourceComboBox.clear()
        
        # The counter is initialized
        count=1       
        # The list of sources is fetched
        source_list = self.api.get_source_list()
        # Each source is added to the source combo box
        for i in source_list:
            # The source is added to the combo box
            self.MainWindow.sourceComboBox.addItem(i, count)
            # The loop counter is increased by 1
            count += 1
        # The title value is set to the settings value
        self.MainWindow.sourceComboBox.setCurrentText(self.settings["source"])
            
    def _load_book_list(self) -> None:
        """It loads the book combo box with list of books.
        
        It fetches list of book names from database.
        It loads the book combo box with book names for the current source.
        """

        # The book combo box is cleared
        self.MainWindow.bookComboBox.clear()
        # The current selection is fetched
        sel       = self._get_current_selection()
        # The currently selected source
        source    = sel["source"]

        # The book list is fetched for the current source
        book_list = self.api.get_book_list(source)
        # Each book in the list is added to the book combo box
        for book in book_list:
            # The book is added to the book combo box
            self.MainWindow.bookComboBox.addItem(book[1], str(book[0]))

        # The book value is set to the settings value
        self.MainWindow.bookComboBox.setCurrentText(self.settings["book"])
            
    def _load_title_list(self) -> None:
        """It loads the title combo box with list of titles for the selected
        hadith source and book.
        """

        # The title combo box is cleared               
        self.MainWindow.titleComboBox.clear()
        # The current selection is fetched
        sel         = self._get_current_selection()        
        # The title list for the current book
        title_list  = self.api.get_title_list(sel["book"])
        # Each title in the title list is added to the title combo box
        for title in title_list:
            # The title is added to the title combo box
            self.MainWindow.titleComboBox.addItem(title[1], str(title[0]))
        # The title value is set to the settings value
        self.MainWindow.titleComboBox.setCurrentText(self.settings["title"])

    def _load_settings(self) -> None:
        """Loads the current settings from database.
        """

        # The sql query
        sql = "SELECT language, row_id FROM `ic_hadith_settings`"            
        # The settings data is fetched
        rows = self.api._fetch_data(sql, [], 2)        
        # The language settings value
        self.lang = rows[0][0]
        # The row id
        row_id = rows[0][1]
        # The language is set in the hapi object
        self.api.set_lang(self.lang)
        # The row values are fetched
        self.settings = self.api.get_row(row_id)                
        

    def _update_settings(self) -> None:
        """It saves the current settings to database.
        """
        
        # The current selection is fetched
        sel = self._get_current_selection()  
        # The settings are updated in database
        self.api.update_settings(self.lang, sel["title"])
