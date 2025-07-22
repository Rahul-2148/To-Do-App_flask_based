from app import create_app, db
from flask_migrate import Migrate
import os

app = create_app()
migrate = Migrate(app, db)

if __name__ == '__main__':
    if not os.path.exists('todo.db'):
        with app.app_context():
            db.create_all()
    app.run(port=5001, debug=True)
