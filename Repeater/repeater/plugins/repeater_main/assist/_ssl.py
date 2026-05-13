import ssl

class SSLContext:
    def __init__(self):
        self.ssl_context: ssl.SSLContext = ssl.create_default_context()

    def get_ssl_context(self):
        return self.ssl_context
    
    def set_ssl_context(self, ssl_context: ssl.SSLContext):
        self.ssl_context = ssl_context
    
    def create_default_context(self):
        self.ssl_context = ssl.create_default_context()
        return self.ssl_context

ssl_context = SSLContext()

def get_ssl_context():
    return ssl_context

def set_ssl_context(ssl_context: ssl.SSLContext):
    ssl_context.set_ssl_context(ssl_context)