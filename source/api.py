import sys

from PyQt5.QtSql import QSqlQuery, QSqlDatabase
from PyQt5.QtWidgets import QMessageBox


class Api():
    """
    This class is the base class for the QuranApi and HadithApi classes.

    Methods
    -------
    __init__()
        The class constructor. It creates a connection to the sqlite3 database
        and sets the default language.
    _display_error()
        Error handling method.
    _fetch_data()
        It runs the given sql select query and returns the fetched data.    
    """

    def __init__(self, db_path: str) -> None:
        """It creates a connection to the sqlite3 database.

        :param db_path: The absolute path to the database.
        :type db_path: str.
        """        
        
        # The database name and connection options are set
        self.con = QSqlDatabase.addDatabase("QSQLITE")
        self.con.setDatabaseName(db_path)
        # self.con.setConnectOptions("QSQLITE_OPEN_READONLY=0")
        # Try to open the connection and handle possible errors
        if not self.con.open():
            # The db path is printed
            print(db_path)
            # The error is shown in message box
            self._display_error("")

    def _display_error(self, last_query: str) -> None:
        """Error handling method.

        It displays the given error message in a message box and ends the
        program. It also prints the error to console.

        :param last_query: The last sql query.
        :type last_query: str.
        """

        # The error message
        msg = "Database error: %s" % self.con.lastError().databaseText()

        # If the last query is given
        if last_query != "":
            msg += " Last query: " + last_query

        QMessageBox.critical(
            None,
            "Quran Reader - Error!",
            msg,
        )

        # The error message is printed to console
        print(msg)

        # The application exits
        sys.exit(1)

    def _fetch_data(self, sql: str, bind_values: list, sel_count: int) -> list:
        """It runs the given sql select query and returns the fetched data

        The sql query placeholder should be "?". The values in the bind_values
        parameter will replace "?".

        :param sql: The sql query to run.
        :type sql: str.        
        :param bind_values: The values to bind to the query placeholders.
        :type bind_values: list.
        :param sel_count: The number of fields in select query.
        :type sel_count: int.
        :return: The required data.
        :rtype: list.
        """

        # Try to open the connection and handle possible errors
        if not self.con.open():
            # The error is shown in message box
            self._display_error("")
            
        # The query object is created
        query = QSqlQuery()

        # If the sql query contains placeholders
        if len(bind_values) > 0:
            # Prepared query is used
            query.prepare(sql)
            # Each given bind value is added
            for val in bind_values:            
                # The bind value is added
                query.addBindValue(val)
            # The query is run
            if not query.exec():
                self._display_error(sql)
        else:
            # The query is run
            if not query.exec(sql):
                self._display_error(sql)

        # All rows
        rows = []
        # All rows are fetched
        while query.next():
            # The row of data
            row = []            
            # All selected field values are fetched
            for i in range(sel_count):
                # The query value
                qval = query.value(i)
                # The query value is appended to the row
                row.append(qval)
            # The row in appended to the list of rows
            rows.append(row)
                
        # The resources associated with the query object are freed
        query.finish()
        # The connection is closed
        #self.con.close()
        # The data is returned
        return rows        
        
    def _update_data(self, sql: str, bind_values: list) -> None:
        """It runs the given sql update query

        The sql query placeholder should be "?". The values in the bind_values
        parameter will replace "?".

        :param sql: The sql query to run.
        :type sql: str.        
        :param bind_values: The values to bind to the query placeholders.
        :type bind_values: list.
        """

        # Try to open the connection and handle possible errors
        if not self.con.open():
            # The error is shown in message box
            self._display_error("")
            
        # The query object is created
        query = QSqlQuery()

        # If the sql query contains placeholders
        if len(bind_values) > 0:
            # Prepared query is used
            query.prepare(sql)
            # Each given bind value is added
            for val in bind_values:            
                # The bind value is added
                query.addBindValue(val)
            # The query is run
            if not query.exec():
                self._display_error(sql)
        else:
            # The query is run
            if not query.exec(sql):
                self._display_error(sql)       
                
        # The resources associated with the query object are freed
        query.finish()
        # The connection is closed
        #self.con.close()     
