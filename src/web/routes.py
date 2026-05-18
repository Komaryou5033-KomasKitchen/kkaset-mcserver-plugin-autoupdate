"""
Web routes for the Flask application
"""

from flask import Blueprint, render_template, jsonify, request, current_app
import logging

logger = logging.getLogger(__name__)

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    """
    Main dashboard page
    """
    return render_template('index.html')

@bp.route('/api/servers')
def get_servers():
    """
    Get list of all servers
    """
    try:
        from ..core.config_loader import ConfigLoader
        config_path = current_app.config.get('CONFIG_PATH', 'config/servers.yaml')
        loader = ConfigLoader(config_path)
        servers = loader.get_servers()
        
        return jsonify({
            'success': True,
            'servers': servers
        })
    except Exception as e:
        logger.error(f"Error fetching servers: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@bp.route('/api/server/<server_name>')
def get_server(server_name: str):
    """
    Get specific server information
    """
    try:
        from ..core.config_loader import ConfigLoader
        config_path = current_app.config.get('CONFIG_PATH', 'config/servers.yaml')
        loader = ConfigLoader(config_path)
        server = loader.get_server(server_name)
        
        if not server:
            return jsonify({
                'success': False,
                'error': f'Server not found: {server_name}'
            }), 404
        
        return jsonify({
            'success': True,
            'server': server
        })
    except Exception as e:
        logger.error(f"Error fetching server {server_name}: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@bp.route('/api/health')
def health():
    """
    Health check endpoint
    """
    return jsonify({
        'status': 'ok',
        'version': '0.1.0'
    })

@bp.errorhandler(404)
def not_found(error):
    """
    Handle 404 errors
    """
    return jsonify({
        'success': False,
        'error': 'Not found'
    }), 404

@bp.errorhandler(500)
def internal_error(error):
    """
    Handle 500 errors
    """
    logger.error(f"Internal error: {error}")
    return jsonify({
        'success': False,
        'error': 'Internal server error'
    }), 500
