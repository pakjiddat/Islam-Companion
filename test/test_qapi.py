import os, unittest
from source.qapi import QuranApi
from source.qconfig import QConfig

class TestQuranApi(unittest.TestCase):
    """Used to test the QuranApi class.
    """

    def test_quran_api(self) -> None:
        """Used to test all the methods of the QuranApi class
        """

        # The application configuration
        qconfig  = QConfig()
        config   = qconfig.get_config()    
        # An instance of the QuranApi class is created
        qapi = QuranApi(config["db_path"], config["default_lang"])

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
        qapi.set_lang("English")
        # Check that the tbl attribute has the correct value
        self.assertEqual(qapi.tbl, "ic_quranic_text-en")
        # Check that the lang attribute has the correct value
        self.assertEqual(qapi.lang, "English")

        # The get_lang_list method is tested 
        lang_list = qapi.get_lang_list()
        # Check that the number of languages is correct
        self.assertEqual(len(lang_list), 43)

        # The is_rtl method is tested 
        is_rtl = qapi.is_rtl("Arabic")
        # Check that the rtl vlaue is correct
        self.assertTrue(is_rtl)

        # The get_font_details method is tested 
        font_details = qapi.get_font_details("Arabic")
        # Check that the font family value is correct
        self.assertEqual(font_details["family"], "Nafees [PYRS]")
        # Check that the font size is correct
        self.assertEqual(font_details["size"], 18)        

if __name__ == '__main__':
    unittest.main()