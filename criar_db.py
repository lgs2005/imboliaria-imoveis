import os
from app import create_app, DATABASE_FILE
from modelo import db


if __name__ == '__main__':
    app = create_app()

    with app.app_context():
        os.remove(os.path.join(app.instance_path, DATABASE_FILE))
        db.create_all()