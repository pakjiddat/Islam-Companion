class QConfig():

    def __init__(self) -> None:
        """Initializes configuration settings for quran reader
        """

        # The application mode. It can be "dev" or "prod"
        self.mode = "dev"
        # The development environment settings
        self.dev_config = {
            "db_path": "source/data/quran.db",
            "font_dir": "./source/data/fonts", 
            "random_icon_path": "source/data/random.png",
            "default_lang": "Urdu"
        }
        # The production environment settings
        self.prod_config = {
            "db_path": "/usr/local/share/islamcompanion/quran.db",
            "font_dir": "/usr/local/share/islamcompanion/fonts",
            "random_icon_path": "/usr/local/share/islamcompanion/random.png",  
            "default_lang": "Urdu"
        }

    def get_config(self) -> dict:
        """Returns the configuration data for the current environment.
        """

        # If the application is in development mode
        if self.mode == "dev":
            conf = self.dev_config
        # If the application is in production mode
        elif self.mode == "prod":
            conf = self.prod_config    

        return conf
