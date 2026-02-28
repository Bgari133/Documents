from app.routes.sqli import bp as sqli_bp
from app.routes.xss import bp as xss_bp
from app.routes.auth import bp as auth_bp
from app.routes.idor import bp as idor_bp
from app.routes.path_traversal import bp as path_traversal_bp
from app.routes.cmd_injection import bp as cmd_injection_bp
from app.routes.csrf import bp as csrf_bp
from app.routes.deserialize import bp as deserialize_bp
from app.routes.misc import bp as misc_bp

__all__ = [
    "sqli_bp",
    "xss_bp",
    "auth_bp",
    "idor_bp",
    "path_traversal_bp",
    "cmd_injection_bp",
    "csrf_bp",
    "deserialize_bp",
    "misc_bp",
]
