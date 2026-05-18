"""
Flask application factory for Web UI
"""

from flask import Flask, render_template, jsonify
from flask_cors import CORS
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

def create_app(config_path: str = "config/servers.yaml", debug: bool = False) -> Flask:
    """
    Create and configure Flask application
    
    Args:
        config_path: Path to servers.yaml
        debug: Enable debug mode
        
    Returns:
        Flask application instance
    """
    app = Flask(__name__)
    
    # Configuration
    app.config['DEBUG'] = debug
    app.config['CONFIG_PATH'] = config_path
    
    # Enable CORS
    CORS(app)
    
    # Setup logging
    if not app.debug:
        handler = logging.FileHandler('logs/web.log')
        handler.setLevel(logging.INFO)
        app.logger.addHandler(handler)
    
    # Register blueprints
    from . import routes
    app.register_blueprint(routes.bp)
    
    # Create necessary directories
    Path('logs').mkdir(exist_ok=True)
    Path('database').mkdir(exist_ok=True)
    Path('backups').mkdir(exist_ok=True)
    
    logger.info("Flask app created successfully")
    
    return app
