from app import app
import werkzeug as wk
import os


class Web:
    @staticmethod
    def get_web_file_uri(web_file):
        filename = wk.secure_filename(web_file.filename)
        web_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return os.path.join(app.config['UPLOAD_FOLDER'], filename)
