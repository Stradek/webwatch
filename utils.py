class LogStream:
    def __init__(self, file=None):
        self.log_file = file

    def set_log_file(self, file):
        self.log_file = file

    def log(self, message):
        print(message)
        if self.log_file is not None:
            self.log_file.write(message + "\n")

    def warning(self, message):
        message = f"WARNING: {message}"
        self.log(message)

    def error(self, message):
        message = f"ERROR: {message}"
        self.log(message)