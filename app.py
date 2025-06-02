from flask import Flask
from dotenv import load_dotenv
from routes import stats_routes, basics_routes

# Charger les variables d’environnement
load_dotenv()

app = Flask(__name__)
app.register_blueprint(stats_routes.stats_api)
app.register_blueprint(basics_routes.basics_api)

if __name__ == '__main__':
    app.run(debug=True)