import sys,os
sys.path.append('..')

from icdesktopapi.quran_api import Quran_Api

class Ui_Manager():
    """
    This class is used to add quran data to the user interface

    Methods
    -------
    initialize_ui()
        Loads the sura and ruku combo boxes. Also displays quran verses
    """
    def initialize_ui(self, MainWindow):
        """It initializes the reader layout
        
        It loads the sura combo box with list of sura names.
        It loads the ruku box with list of rukus in the current sura.
        It displays the range of ayat numbers in the current ruku.
        It displays quran verses in the text area.
        It connects the sura and ruku combo boxes to callbacks
        It connects the next and previous buttons to callback
        
        Parameters
        ----------
        MainWindow : QMainWindow
            The quran reader window
        """
    
        # The absolute path to the database
        cur_dir        = os.path.dirname(os.path.realpath(__file__))
        db_path        = os.path.abspath(cur_dir + "/data/holy-quran.db")
        # Creates an instance of the Quran_Api class
        self.api        = Quran_Api(db_path)
        # The main window object is set as obj attribute
        self.MainWindow = MainWindow
        
        # Connects the sura combo box to a call back
        self.MainWindow.suraComboBox.activated.connect(self._sura_selected)
        # Connects the ruku combo box to a call back
        self.MainWindow.rukuComboBox.activated.connect(self._ruku_selected)
        # Connects the next button to a call back
        self.MainWindow.nextButton.clicked.connect(self._next_ruku)
        # Connects the prev button to a call back
        self.MainWindow.prevButton.clicked.connect(self._prev_ruku)        
        
        # Loads the sura combo box with list of suras
        self._load_sura_list()
        # Loads the ruku combo box with list of rukus
        self._load_ruku_list()
        # Sets the start and end ayat numbers
        self._load_ayat_range()
        # Displays the ayat text
        self._load_ayat_box()        

    def _next_ruku(self):
        """Event handler for the next ruku button.
        
        It loads the text of next ruku to ayat box.
        It also loads the sura and ruku combo boxes.
        It also updates the ayat range.
        """
        selection = self._get_current_selection()
        next_sura = selection["sura"]
        next_ruku = selection["ruku"]
        
        if selection["ruku"] < self.MainWindow.rukuComboBox.count():
            next_ruku += 1
        else:
            next_ruku = 1
            next_sura += 1
            if next_sura > self.MainWindow.suraComboBox.count():
                next_sura = 1
                 
            self.MainWindow.suraComboBox.setCurrentIndex(next_sura-1)
            self._load_ruku_list()
                            
        self.MainWindow.rukuComboBox.setCurrentIndex(next_ruku-1)
        self._load_ayat_range()
        self._load_ayat_box()
        
    def _prev_ruku(self):
        """Event handler for the prev ruku button.
        
        It loads the text of previous ruku to ayat box.
        It also loads the sura and ruku combo boxes.
        It also updates the ayat range.
        """
        selection = self._get_current_selection()
        prev_sura = selection["sura"]
        prev_ruku = selection["ruku"]
        
        if selection["ruku"] > 1:
            prev_ruku -= 1
        else:
            prev_sura -= 1
            if prev_sura < 1:
                prev_sura = 114
            self.MainWindow.suraComboBox.setCurrentIndex(prev_sura-1)
            self._load_ruku_list()
            prev_ruku = self.MainWindow.rukuComboBox.count()
            
        self.MainWindow.rukuComboBox.setCurrentIndex(prev_ruku-1)        
        self._load_ayat_range()
        self._load_ayat_box()
                    
    def _sura_selected(self):
        """It loads the ruku combo box and the ayat box"""
        self._load_ruku_list()
        self._load_ayat_range()
        self._load_ayat_box()   
        
    def _ruku_selected(self):
        """It loads the ruku combo box and the ayat box"""
        self._load_ayat_range()
        self._load_ayat_box()
        
    def _get_current_selection(self):
        """It returns the currently selected sura and ruku
        It also returns the start and end ayat numbers
        The sura data includes the sura short name and number
        
        Returns
        -------
        selection
            The selected sura, ruku and ayat numbers
        """
        
        if self.MainWindow.suraComboBox.count() > 0:
            sura      = self.MainWindow.suraComboBox.currentData()
            sura      = int(sura)
            stext     = self.MainWindow.suraComboBox.currentText().split(" (")
            stext     = stext[0]
        else:
            sura      = 1
            stext     = "Al-Faatiha"

        if self.MainWindow.rukuComboBox.count() > 0:        
            ruku      = self.MainWindow.rukuComboBox.currentData()
            ruku      = int(ruku)
        else:
            ruku      = 1
        
        text          = self.MainWindow.ayatRange.text().split(" - ");
        start         = int(text[0])
        end           = int(text[1])
        
        selection     = {
                            "sura": sura,
                            "ruku": ruku,
                            "start": start,
                            "end": end,
                            "stext": stext
                        }
        
        return selection

    def _load_ayat_box(self):
        """It sets the ayat text"""
        
        sel       = self._get_current_selection()
        ayat_list = self.api.get_ayat_text(sel["sura"], sel["ruku"])
        aya       = sel["start"]
        text      = "<ol style='margin-left: 25px; list-style-type: none'>";
        style     = "color:green; font-size: 12pt;"
        for line in ayat_list:
            text  += "<li style='line-height:50px; padding-bottom: 20px'>" + line
            text  += " <br/><span style='" + style + "'>("
            text  += sel["stext"] + " " + str(sel["sura"]) + ":"
            text  += str(aya) + ")</span></li>"
            aya   += 1
            
        text      += "</ol>"

        self.MainWindow.ayatText.setHtml(text)

    def _load_ayat_range(self):
        """It sets the ayat range label.

        It sets the start and end ayat values to the label
        """
        
        selection = self._get_current_selection()
                        
        ayat_data = self.api.get_ayat_range(selection["sura"], selection["ruku"])
        text      = str(ayat_data["start"]) + " - " + str(ayat_data["end"])
        self.MainWindow.ayatRange.setText(text)
            
    def _load_ruku_list(self):
        """It loads the ruku combo box with list of rukus
        
        It fetches number of rukus in the selected sura.
        It loads the ruku combo box with list of rukus.
        """
        
        self.MainWindow.rukuComboBox.clear()
        
        if self.MainWindow.suraComboBox.count() > 0:
            sura      = self.MainWindow.suraComboBox.currentData()
            sura      = int(sura)
        else:
            sura      = 1
            
        ruku_count    = self.api.get_ruku_count(sura)

        for i in range(1, (ruku_count+1)):
            ruku   = (str(i))
            self.MainWindow.rukuComboBox.addItem(ruku, ruku)
                
    def _load_sura_list(self):
        """It loads the sura combo box with list of suras
        
        It fetches list of sura names from database.
        It loads the sura combo box with sura names.
        """
        
        count=1
        sura_list = self.api.get_sura_names()
        for i in sura_list:
            self.MainWindow.suraComboBox.addItem(i, count)
            count += 1
