import os, sys

from source.api import Api

class HadithApi(Api):
    """
    This class is used to fetch hadith data from SQLite3 database.

    Methods
    -------
    set_lang()
        Sets the language and db tables for the hadith text.
    get_source_list()
        Fetches list of all hadith sources from database.
    get_book_list()
        Fetches list of all hadith books for the given
        source from database.
    get_title_list()
        Fetches list of all hadith books and titles for given
        source from database.
    get_hadith_text()
        Fetches the hadith text for the given source and book.
    update_settings()
        Updates the current settings in database.
    get_row()
        Gets the field values for the given row.
    """
    
    def __init__(self, db_path: str, default_lang: str) -> None:
        """It creates a connection to the SQLite3 database and sets the default
        language.
 
        :param db_path: The absolute path to the database.
        :type db_path: str.
        :param default_lang: The default language.
        :type default_lang: str.
        """

        # The default language is set
        self.set_lang(default_lang)
        # The parent class constructor is called
        super().__init__(db_path)        

    def set_lang(self, lang: str) -> None:
        """It sets the language and db tables for the hadith text.
        
        :param lang: The 2 letter language code.
        :type lang: str.
        """
        
        # The language for the ayat text is set
        self.lang = lang    
        
        # If the language is "Urdu"
        if lang == "Urdu":
            # The db table for hadith text is set
            self.tbl_text = "ic_hadith_urdu"
            # The db table for hadith books is set
            self.tbl_books = "ic_hadith_books_urdu"
        # If the language is "English"
        elif lang == "English":
            # The db table for hadith text is set
            self.tbl_text = "ic_hadith_english"
            # The db table for hadith books is set
            self.tbl_books = "ic_hadith_books_english"
        # If the language is "Arabic"
        elif lang == "Arabic":
            # The db table for hadith text is set
            self.tbl_text = "ic_hadith_arabic"
            # The db table for hadith books is set
            self.tbl_books = "ic_hadith_books_arabic"
                            
    def get_source_list(self) -> list:
        """It fetches and returns list of all hadith sources from database.
        
        :return: The list of hadith sources.
        :rtype: list.
        """
        
        # The required source list
        source_list = []        
        # The sql query
        sql         = "SELECT DISTINCT source FROM " + self.tbl_books
        # The hadith source data is fetched
        rows        = self._fetch_data(sql, [], 1)
        # Each row is checked
        for row in rows:
            source_list.append(row[0])

        return source_list
        
    def get_book_list(self, source: str) -> list:
        """It fetches and returns list of all hadith books in the given source.
        
        :param source: The hadith source.
        :type lang: str.
        :return: The list of hadith books.
        :rtype: list.
        """
        
        # The required hadith book list
        book_list = []
        # The bind values for the sql query
        args      = [source]
        # The sql query
        sql       = "SELECT id, book FROM " + self.tbl_books
        sql       += " WHERE source=? ORDER BY book_number ASC"
        
        # The hadith book data is fetched
        book_list = self._fetch_data(sql, args, 2)
        
        return book_list
        
    def get_title_list(self, book: int) -> list:
        """It fetches and returns list of hadith titles for the given book.
        
        :param book: The hadith book id.
        :type book: int.
        :return: The list of hadith titles.
        :rtype: list.
        """
        
        # The required hadith title list
        title_list = []
        # The bind values for the sql query
        args  = [book]
        # The sql query
        sql   = "SELECT id, title FROM " + self.tbl_text + " WHERE book_id=?"
        sql   += " ORDER BY id ASC"
        
        # The hadith book data is fetched
        title_list = self._fetch_data(sql, args, 2)

        return title_list
        
    def get_hadith_text(self, hadith_id: int) -> str:
        """It fetches and returns the hadith text for the given hadith id.
        
        :param hadith_id: The hadith id.
        :type hadith_id: int.
        :return: The hadith text.
        :rtype: str.    
        """

        # The required hadith text
        hadith_text = ""
        # The bind values for the sql query
        args    = [int(hadith_id)]
        # The sql query
        sql     = "SELECT hadith_text FROM " + self.tbl_text + " WHERE id=?"
        
        # The hadith text data is fetched
        rows = self._fetch_data(sql, args, 1)
        # The hadith text is set
        hadith_text = rows[0][0]

        return hadith_text

    def update_settings(self, lang: str, row_id: int) -> None:
        """Updates the current settings in database.
        
        :param row_id: The current row id.
        :type row_id: int.        
        """

        # The bind values for the query
        bind_values = [lang, row_id]
        sql = "UPDATE ic_hadith_settings SET language=?, row_id=?"
        self._update_data(sql, bind_values)

    def get_row(self, row_id: int) -> dict:
        """It returns the field values for the given row.

        :param row_id: The row id.
        :type row_id: int.                    
        :return: The field values for the given row.
        :rtype: dict.    
        """

        # The bind values for the sql query
        args = [row_id]
        # The sql query
        sql = "SELECT book_id, title FROM `" + self.tbl_text + "`"
        sql += " WHERE id=?"        
        # The required data is fetched
        rows = self._fetch_data(sql, args, 2)
        # The book id
        book_id = rows[0][0]
        # The title
        title = rows[0][1]

        # The bind values for the sql query
        args = [book_id]
        # The sql query
        sql = "SELECT book, source FROM `" + self.tbl_books + "`"
        sql += " WHERE id=?"        
        # The required data is fetched
        rows = self._fetch_data(sql, args, 2)
        # The source
        book = rows[0][0]
        # The book
        source = rows[0][1]

        data = {"title": title, "source": source, "book": book}

        return data