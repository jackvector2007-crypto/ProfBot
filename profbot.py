import importlib.util
import os

# This wrapper loads the original file with the space in its name ("profbot. py")
# and exposes the Flask `app` object so Gunicorn can import profbot:app.
here = os.path.dirname(__file__)
legacy_path = os.path.join(here, "profbot. py")

spec = importlib.util.spec_from_file_location("profbottest", legacy_path)
profbottest = importlib.util.module_from_spec(spec)
spec.loader.exec_module(profbottest)

# Expose the Flask application object for Gunicorn (profbot:app)
app = getattr(profbottest, "app")

# Optional: expose other objects if needed
__all__ = ["app"]
