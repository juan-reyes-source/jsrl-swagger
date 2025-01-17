class FileNotFoundException(Exception):
    
    def __init__(self,
                 file_path,
                 message='The file doesn\'t have in the expected path'):
        self.message = message
        self.file_path = file_path
        super().__init__(self.message, self.file_path)
