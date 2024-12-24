from urllib.parse import urlparse
from flask import abort

class Validator:
    @staticmethod
    def url_validator(url):
        try:

            parse_url = urlparse(url)
            domain = parse_url.netloc.lower()

            if not domain:
                abort(400, description="Invalid URL format: Missing domain")
            
            if domain!="engineering.utdallas.edu":
                abort(400, description="Invalid URL format: Missing domain")
        except Exception as e:
            abort(400 , description = f"Invalid URLD format : {str(e)}")
        
        