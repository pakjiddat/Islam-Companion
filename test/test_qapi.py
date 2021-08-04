import os, unittest
from qapi import QuranApi

class TestQuranApi(unittest.TestCase):
    """Used to test the QuranApi class.
    """

    def test_quran_api(self):
        """Used to test all the methods of the QuranApi class
        """

        # The absolute path to the database
        cur_dir = os.path.dirname(os.path.realpath(__file__))
        db_path = os.path.abspath(cur_dir + "/../data/quran.db")
        # An instance of the QuranApi class is created
        qapi = QuranApi(db_path, "ur")

        # The get_random_ruku method is tested 
        ruku_details = qapi.get_random_ruku()
        # Check that the sura value is correct
        self.assertTrue(
            ruku_details["sura"] >=0 and ruku_details["sura"] <= 114)
        # Check that the sura_ruku value is correct
        self.assertTrue(ruku_details["sura_ruku"] >=0 and 
            ruku_details["sura_ruku"] <= 40)

        # The get_ruku_count method is tested 
        ruku_count = qapi.get_ruku_count(2)
        # Check that the ruku_count value is correct
        self.assertEqual(ruku_count, 40)

        # The get_ayat_range method is tested 
        ayat_range = qapi.get_ayat_range(2, 10)
        # Check that the ayat_range start value is correct
        self.assertEqual(ayat_range["start"], 83)
        # Check that the ayat_range end value is correct
        self.assertEqual(ayat_range["end"], 86)

        # The get_ayat_text method is tested 
        ayat_text = qapi.get_ayat_text(2, 10)
        # Check that the ayat_text contains has the correct length
        self.assertEqual(len(ayat_text), 4)
        
        # The get_sura_names method is tested 
        sura_list = qapi.get_sura_names()
        # Check that the sura_list has the correct length
        self.assertEqual(len(sura_list), 114)

        # The set_lang method is tested 
        qapi.set_lang("en")
        # Check that the tbl attribute has the correct value
        self.assertEqual(qapi.tbl, "ic_quranic_text-en")
        # Check that the lang attribute has the correct value
        self.assertEqual(qapi.lang, "en")
        

if __name__ == '__main__':
    unittest.main()