import sys,os
sys.path.append('..')

from icdesktopapi.hadith_api import Hadith_Api

class Ui_Manager():
    """
    This class is used to add hadith data to the user interface

    Methods
    -------
    initialize_ui()
        Loads the source, book and title combo boxes. Also displays hadith text
    """
    def initialize_ui(self, MainWindow):
        """It initializes the reader layout
        
        It loads the source combo box with list of hadith sources.
        It loads the book combo box with books in the current hadith source.
        It loads the title combo box with titles in the current hadith source and book.
        It displays hadith verses in the text area.
        It connects the source, book and title combo boxes to callbacks
        It connects the next and previous buttons to callbacks
        
        Parameters
        ----------
        MainWindow : QMainWindow
            The hadith reader window
        """
        
        # The absolute path to the database
        cur_dir         = os.path.dirname(os.path.realpath(__file__))
        db_path         = os.path.abspath(cur_dir + "/data/hadith.db")
        # Creates an instance of the Hadith_Api class
        self.api        = Hadith_Api(db_path)
        # The main window object is set as obj attribute
        self.MainWindow = MainWindow
        
        # Connects the source combo box to a call back
        self.MainWindow.sourceComboBox.activated.connect(self._source_selected)
        # Connects the book combo box to a call back
        self.MainWindow.bookComboBox.activated.connect(self._book_selected)
        # Connects the title combo box to a call back
        self.MainWindow.titleComboBox.activated.connect(self._load_hadith_box)
        # Connects the next button to a call back
        self.MainWindow.nextButton.clicked.connect(self._next_hadith)
        # Connects the prev button to a call back
        self.MainWindow.prevButton.clicked.connect(self._prev_hadith)        
        
        # Loads the source combo box with list of sources
        self._load_source_list()
        # Loads the book combo box with list of books
        self._load_book_list()
        # Loads the title combo box with list of titles
        self._load_title_list()
        # Displays the hadith text
        self._load_hadith_box()        

    def _next_hadith(self):
        """Event handler for the next hadith button.
        
        It loads the text of next hadith to hadith box.
        It also loads the source, title and book combo boxes if needed.
        """
        sel     = self._get_current_selection()
        
        ctindex = self.MainWindow.titleComboBox.currentIndex()
        tcount  = self.MainWindow.titleComboBox.count()
        
        cbindex = self.MainWindow.titleComboBox.currentIndex()
        bcount  = self.MainWindow.titleComboBox.count()
        
        csindex = self.MainWindow.sourceComboBox.currentIndex()
        scount  = self.MainWindow.sourceComboBox.count()        
        
        if ctindex == (tcount-1):
            if cbindex == (bcount-1):
                if csindex == (scount-1):
                    self.MainWindow.sourceComboBox.setCurrentIndex(0)
                else:
                    self.MainWindow.sourceComboBox.setCurrentIndex(csindex+1)
                self._load_book_list()
                self._load_title_list()
            else:
                self.MainWindow.bookComboBox.setCurrentIndex(cbindex+1)
            self._load_title_list()
        else:
            self.MainWindow.titleComboBox.setCurrentIndex(ctindex+1)

        self._load_hadith_box()            
        
    def _prev_hadith(self):
        """Event handler for the previous hadith button.
        
        It loads the text of previous hadith to hadith box.
        It also loads the source, title and book combo boxes.
        """
        sel     = self._get_current_selection()
        
        ctindex = self.MainWindow.titleComboBox.currentIndex()
        tcount  = self.MainWindow.titleComboBox.count()
        
        cbindex = self.MainWindow.titleComboBox.currentIndex()
        bcount  = self.MainWindow.titleComboBox.count()
        
        csindex = self.MainWindow.sourceComboBox.currentIndex()
        scount  = self.MainWindow.sourceComboBox.count()        
        
        if ctindex == 0:
            if cbindex == 0:
                if csindex == 0:
                    self.MainWindow.sourceComboBox.setCurrentIndex(scount-1)
                else:
                    self.MainWindow.sourceComboBox.setCurrentIndex(csindex-1)
                self._load_book_list()
                self._load_title_list()                    
            else:
                self.MainWindow.bookComboBox.setCurrentIndex(cbindex-1)
            self._load_title_list()                
        else:
            self.MainWindow.titleComboBox.setCurrentIndex(ctindex-1)

        self._load_hadith_box() 
                    
    def _source_selected(self):
        """It loads the book and title combo boxes and also the hadith box"""
        self._load_book_list()
        self._load_title_list()
        self._load_hadith_box()   
        
    def _book_selected(self):
        """It loads the title combo box and the hadith box"""
        self._load_title_list()
        self._load_hadith_box()
        
    def _get_current_selection(self):
        """It returns the currently selected source, book and title
        
        Returns
        -------
        selection
            The selected source, book and title
        """
        
        if self.MainWindow.sourceComboBox.count() > 0:
            source    = self.MainWindow.sourceComboBox.currentText()
        else:
            source    = "صحیح بخاری"

        if self.MainWindow.bookComboBox.count() > 0:        
            book      = self.MainWindow.bookComboBox.currentData()
            book      = int(book)
        else:
            book      = 1
            
        if self.MainWindow.titleComboBox.count() > 0:        
            title = self.MainWindow.titleComboBox.currentData()
            title = int(title)
            ttext = self.MainWindow.titleComboBox.currentText()
        else:
            title = 1
            ttext = "باب: رسول اللہ صلی اللہ علیہ وسلم پر وحی کی ابتداء کیسے ہوئی";
        
        selection = {
                      "source": source,
                      "book": book,
                      "title": title,
                      "ttext": ttext
        }
        
        return selection

    def _load_hadith_box(self):
        """It sets the hadith text"""
        
        sel   = self._get_current_selection()
        htext = self.api.get_hadith_text(sel["title"])
        style = "margin: 15px; padding-top: 20px;"
        style += "line-height:50px; padding-bottom: 20px";
        text  = "<div style='" + style + "'>"
        text += "عنوان: " + sel["ttext"] + "<br/><br/>";
        text += htext
        text += "</div>"
        
        self.MainWindow.hadithText.setHtml(text)
                
    def _load_source_list(self):
        """It loads the source combo box with list of sources
        
        It fetches list of source names from database.
        It loads the source combo box with source names.
        """
        
        self.MainWindow.sourceComboBox.clear()
        
        count=1       
        source_list = self.api.get_source_list()
        for i in source_list:
            self.MainWindow.sourceComboBox.addItem(i, count)
            count += 1
            
    def _load_book_list(self):
        """It loads the book combo box with list of books
        
        It fetches list of book names from database.
        It loads the book combo box with book names for the current source.
        """

        self.MainWindow.bookComboBox.clear()
        
        sel       = self._get_current_selection()
        source    = sel["source"]
        book_list = self.api.get_book_list(source)
        for book in book_list:
            self.MainWindow.bookComboBox.addItem(book[1], str(book[0]))
            
    def _load_title_list(self):
        """It loads the title combo box with list of titles
        For the selected hadith source and book
        """
               
        self.MainWindow.titleComboBox.clear()
                       
        sel         = self._get_current_selection()        
        title_list  = self.api.get_title_list(sel["book"])
        for title in title_list:
            self.MainWindow.titleComboBox.addItem(title[1], str(title[0]))
