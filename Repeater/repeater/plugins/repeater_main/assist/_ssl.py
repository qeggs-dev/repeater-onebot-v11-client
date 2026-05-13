import ssl
from typing import ClassVar

class SSLContext:
    ssl_context: ClassVar[ssl.SSLContext] = ssl.create_default_context()

    @classmethod
    def get_ssl_context(cls):
        return cls.ssl_context
    
    @classmethod
    def set_ssl_context(cls, ssl_context: ssl.SSLContext):
        cls.ssl_context = ssl_context
    
    @classmethod
    def create_default_context(cls):
        cls.ssl_context = ssl.create_default_context()
        return cls.ssl_context

ssl_context = SSLContext()

def get_ssl_context():
    return ssl_context

def set_ssl_context(ssl_context: ssl.SSLContext):
    ssl_context.set_ssl_context(ssl_context)