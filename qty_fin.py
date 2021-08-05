import os
from app import create_app, db
from app.models import Product
from flask_migrate import Migrate

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)
app.run()


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, Product=Product)
