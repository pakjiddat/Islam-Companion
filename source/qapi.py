import os, sys

from source.api import Api

class QuranApi(Api):
    """
    This class is used to fetch quran data from sqlite3 database.

    Methods
    -------
    __init__()
        The class constructor. It creates a connection to the sqlite3 database
        and sets the default language.

    set_lang()
        Sets the language for the ayat text.
    is_rtl()
        Check if the given language is rtl.
    get_font_details()
        Gets the font family and font size for the given language.
    get_db_tbl_name()
        Gets the name of the db table for the given language.    
    get_lang_list()
        Gets the list of all supported languages from database.        
    get_sura_names()
        Fetches list of all sura names from database.
    get_ruku_count()
        Fetches the number of rukus in the given sura.
    get_ayat_range()
        Fetches the start and end ayat for the given sura and ruku.
    get_ayat_text()
        Fetches the ayat text for the given sura and ruku.,
    get_random_ruku()
        Fetches details for a randomly choosen ruku.
    update_settings()
        Updates the current settings in database.
    get_row()
        Gets the field values for the given row
    """

    def __init__(self, db_path: str, default_lang: str) -> None:
        """It creates a connection to the sqlite3 database and sets the default
        language.

        :param db_path: The absolute path to the database.
        :type db_path: str.
        :param default_lang: The default language.
        :type default_lang: str.
        """
        
        # The parent class constructor is called
        super().__init__(db_path)
        # The default language is set
        self.set_lang(default_lang)

    def set_lang(self, lang: str) -> None:
        """It sets the language and db table for the ayat text.

        :param lang: The language.
        :type lang: str.
        """

        # The language for the ayat text is set
        self.lang = lang

        # Returns the name of the db table for the given language
        self.tbl = self._get_db_tbl_name(lang)        

    def get_lang_list(self) -> list:
        """Gets the list of all supported languages from database.
        """

        sql = "SELECT language FROM ic_quranic_tbl_meta_data "
        sql += "ORDER BY language ASC"

        # The required language list
        lang_list = []
        # The language data is fetched
        rows = self._fetch_data(sql, [], 1)
        # Each row is added to a list
        for row in rows:
                lang_list.append(row[0])

        return lang_list

    def update_settings(self, lang: str, sura:int, ayat_id:int) -> None:
        """Updates the current settings in database.
        
        :param lang: The current language.
        :type lang: string
        :param sura: The current sura.
        :type sura: int
        :param ayat_id: The start ayat id.
        :type ayat_id: int
        """

        # The sql query
        sql = "SELECT id FROM `" + self.tbl + "` WHERE sura=? AND "
        sql += "sura_ayat_id=?"
        
        # The language data is fetched
        rows = self._fetch_data(sql, [sura, ayat_id], 1)
        
        # The bind values for the query
        bind_values = [lang, rows[0][0]]
        sql = "UPDATE ic_quranic_settings SET language=?, row_id=?"
        self._update_data(sql, bind_values)
        
    def get_font_details(self, lang:str) -> dict:
        """Gets the font family and font size for the given language.

        :param lang: The language.
        :type lang: string.        
        """

        # The sql query
        sql = "SELECT font_family, font_size FROM ic_quranic_tbl_meta_data"
        sql += " WHERE language=?"        
        
        # The language data is fetched
        rows = self._fetch_data(sql, [lang], 2)
        # The font details
        font_details = {}
        font_details["family"] = rows[0][0]
        font_details["size"] = int(rows[0][1])        
    
        return font_details

    def is_rtl(self, lang: str) -> bool:
        """Check if the given language is rtl.
        
        :param lang: The language.
        :type lang: string.        
        """

        # The sql query
        sql = "SELECT rtl FROM ic_quranic_tbl_meta_data WHERE language=?"        
        
        # The language data is fetched
        rows = self._fetch_data(sql, [lang], 1)
        # The rtl value
        rtl = bool(rows[0][0])
        
        return rtl

    def _get_db_tbl_name(self, lang: str) -> str:
        """Gets the name of the db table for the given language.
                
        :param lang: The language.
        :type lang: string.        
        """

        # The sql query
        sql = "SELECT tbl_name FROM ic_quranic_tbl_meta_data WHERE language=?"        
        
        # The language data is fetched
        rows = self._fetch_data(sql, [lang], 1)
        # The table name
        tbl_name = rows[0][0]

        return tbl_name

    def get_random_ruku(self) -> dict:
        """It fetches and returns the sura id and sura ruku id of a random ruku.       

        :return: The sura id and sura ruku id of a random ruku.
        :rtype: dict.            
        """

        sql = "SELECT sura, sura_ruku FROM ic_quranic_meta_data "
        sql += "ORDER BY random() LIMIT 0,1"

        # The ruku data is fetched
        rows = self._fetch_data(sql, [], 2)

        # The required ruku details
        ruku_details = {"sura": rows[0][0], "sura_ruku": rows[0][1]}

        return ruku_details

    def get_ayat_text(self, sura: int, ruku: int) -> list:
        """It fetches and returns the ayat text for the given sura and ruku.

        :param sura: The sura number.
        :type sura: int.        
        :param ruku: The ruku number
        :type ruku: int.
        :return: The list of ayas.
        :rtype: list.
        """

        # The required list of ayas
        ayat_list = []
        # The range of ayas is fetched
        data = self.get_ayat_range(sura, ruku)
        # The bind values for the sql query
        args = [str(sura), str(data['start']), str(data['end'])]

        # The sql query
        sql = "SELECT translated_text FROM `" + self.tbl + "`"
        sql += " WHERE sura=?"
        sql += " and sura_ayat_id>=?"
        sql += " and sura_ayat_id<=?"

        # The required data is fetched
        rows = self._fetch_data(sql, args, 1)
        # Each row is checked
        for row in rows:
                ayat_list.append(row[0])

        return ayat_list

    def get_sura_names(self) -> list:
        """It fetches and returns list of all sura names from database.

        :return: The list of sura names.
        :rtype: list.
        """

        sura_list = []
        sql = "SELECT tname, ename FROM ic_quranic_suras_meta"

        # The required data is fetched
        rows = self._fetch_data(sql, [], 2)
        # Each row is checked
        for row in rows:
            # The sura name
            sura_name = (row[0] + " (" + row[1] + ")")
            # The sura name is appended to the sura list
            sura_list.append(sura_name)                

        return sura_list

    def get_ruku_count(self, sura: int) -> int:
        """It returns the number of rukus in the given sura.

        :param sura: The sura number.
        :type sura: int.            
        :return: The number of rukus in the given sura.
        :rtype: int.
        """

        # The bind values for the sql query
        args = [sura]
        # The sql query
        sql  = "SELECT rukus FROM ic_quranic_suras_meta WHERE sindex=?"

        # The required data is fetched
        rows = self._fetch_data(sql, args, 1)
        # The ruku count
        ruku_count = int(rows[0][0])

        return ruku_count

    def get_ayat_range(self, sura: int, ruku: int) -> dict:
        """It returns the start and end ayat number for the given sura and ruku.

        :param sura: The sura number.
        :type sura: int.            
        :param ruku: The ruku number.
        :type ruku: int.            
        :return: The start and end ayat numbers.
        :rtype: dict.    
        """

        # The bind values for the sql query
        args = [sura, ruku]
        # The required ayat data
        ayat_data = {"start": "1", "end": "1"}

        # The sql query for start ayat
        sql = "SELECT sura_ayat_id FROM ic_quranic_meta_data"
        sql += " WHERE sura=?"
        sql += " AND sura_ruku=?"
        query = sql + " ORDER BY id ASC"

        # The required data is fetched
        rows = self._fetch_data(query, args, 1)
        # The start ayat
        ayat_data['start'] = rows[0][0]

        # The sql query for end ayat
        query = sql + " ORDER BY id DESC"
        # The required data is fetched
        rows = self._fetch_data(query, args, 1)
        # The end ayat
        ayat_data['end'] = rows[0][0]

        return ayat_data

    def get_row(self, row_id: int) -> list:
        """It returns the field values for the given row.

        :param row_id: The row id.
        :type row_id: int.                    
        :return: The field values for the given row.
        :rtype: dict.    
        """

        # The bind values for the sql query
        args = [row_id]

        # The sql query
        sql = "SELECT sura, sura_ruku FROM `ic_quranic_meta_data`"
        sql += " WHERE id=?"        

        # The required data is fetched
        rows = self._fetch_data(sql, args, 2)
  
        return rows