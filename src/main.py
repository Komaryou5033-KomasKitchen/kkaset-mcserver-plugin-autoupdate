"""
KKASET Minecraft Plugin Manager - Main Entry Point
"""

import os
import sys
import argparse
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent))

def main():
    """
    Main entry point for the plugin manager
    """
    parser = argparse.ArgumentParser(
        description="KKASET Minecraft Plugin Auto-Update Manager",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py                    # Start the web UI
  python main.py --setup            # Initial setup
  python main.py --check            # Manual update check
  python main.py --version          # Show version
        """
    )
    
    parser.add_argument(
        "--setup",
        action="store_true",
        help="Run initial setup wizard"
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Manually check for plugin updates"
    )
    parser.add_argument(
        "--version",
        action="store_true",
        help="Show version information"
    )
    parser.add_argument(
        "--config",
        type=str,
        default="config/servers.yaml",
        help="Path to servers configuration file (default: config/servers.yaml)"
    )
    parser.add_argument(
        "--host",
        type=str,
        default="0.0.0.0",
        help="Web UI host (default: 0.0.0.0)"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=5000,
        help="Web UI port (default: 5000)"
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug mode"
    )
    
    args = parser.parse_args()
    
    if args.version:
        from . import __version__
        print(f"KKASET Minecraft Plugin Auto-Update v{__version__}")
        print(f"Author: Komaryou5033")
        print(f"Repository: https://github.com/Komaryou5033-KomasKitchen/kkaset-mcserver-plugin-autoupdate")
        return
    
    print("🎮 KKASET Minecraft Plugin Manager")
    print("=" * 60)
    
    if args.setup:
        print("\n📋 Running initial setup wizard...")
        # TODO: Implement setup wizard
        print("TODO: Setup wizard not yet implemented")
        return
    
    if args.check:
        print("\n🔍 Checking for plugin updates...")
        # TODO: Implement manual check
        print("TODO: Manual check not yet implemented")
        return
    
    # Default: Start web UI
    print(f"\n🌐 Starting Web UI...")
    print(f"   Access: http://{args.host}:{args.port}")
    print(f"   Config: {args.config}")
    print()
    
    try:
        from web.app import create_app
        app = create_app(config_path=args.config, debug=args.debug)
        app.run(host=args.host, port=args.port, debug=args.debug)
    except ImportError as e:
        print(f"❌ Error: Could not import Flask app: {e}")
        print("   Please ensure all dependencies are installed:")
        print("   pip install -r requirements.txt")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
