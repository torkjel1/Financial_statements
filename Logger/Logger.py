
class Logger:

    instance = None
    filename = None

    def __new__(cls, filename):
        if cls.instance is None:
            cls.instance = super().__new__(cls)
            cls.filename = filename
        else:
            return cls.instance

    @classmethod
    def set_filename(cls, filename):
        cls.filename = filename

    def write_to_log(self, message):
        if not os.path.exists(self.filename):
            open(self.filename, 'w').close()  # Create the file if it doesn't exist

        with open(self.filename, 'a') as file:
            file.write(message + '\n')


