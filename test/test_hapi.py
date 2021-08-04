import os, unittest
from hapi import HadithApi

class TestHadithApi(unittest.TestCase):
    """Used to test the HadithApi class.
    """

    def test_hadith_api(self):
        """Used to test all the methods of the HadithApi class
        """

        # The absolute path to the database
        cur_dir = os.path.dirname(os.path.realpath(__file__))
        db_path = os.path.abspath(cur_dir + "/../data/hadith.db")
        # An instance of the HadithApi class is created
        hapi = HadithApi(db_path, "ur")

        # The get_source_list method is tested 
        source_list = hapi.get_source_list()
        # Check that the number of elements in source_list is correct
        self.assertEqual(len(source_list), 5)
        
        # The get_book_list method is tested 
        book_list = hapi.get_book_list(source_list[0])
        # Check that the number of elements in book_list is correct
        self.assertEqual(len(book_list), 95)

        # The get_title_list method is tested 
        title_list = hapi.get_title_list(book_list[0][0])
        # Check that the number of elements in title_list is correct
        self.assertEqual(len(title_list), 7)

        # The get_hadith_text method is tested 
        hadith_text = hapi.get_hadith_text(1)
        # Check that the hadith text has data
        self.assertGreaterEqual(len(hadith_text), 10)

        # The set_lang method is tested 
        hapi.set_lang("ur")
        # Check that the tbl_books attribute has the correct value
        self.assertEqual(hapi.tbl_books, "ic_hadith_books_urdu")
        # Check that the tbl attribute has the correct value
        self.assertEqual(hapi.tbl_text, "ic_hadith_urdu")
        # Check that the lang attribute has the correct value
        self.assertEqual(hapi.lang, "ur")

if __name__ == '__main__':
    unittest.main()