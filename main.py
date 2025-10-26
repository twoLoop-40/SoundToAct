"""
SoundToAct - Voice-triggered automation app


Main entry point for the application.
Choose between CLI mode or API server mode.
"""
import sys
import argparse


def run_cli():
    """Run CLI mode with voice listener"""
    from app.voice_listener import VoiceListener
    from app.actions import action_registry

    print("Starting SoundToAct in CLI mode...")

    # Create and initialize listener
    listener = VoiceListener()
    listener.initialize()

    # Register default actions
    listener.register_action(
        "엄마", lambda: action_registry.call_action({"contact": "엄마"})
    )
    listener.register_action("음악", lambda: action_registry.play_music_action({}))
    listener.register_action(
        "불꺼", lambda: action_registry.lights_action({"state": "off"})
    )

    # Start listening
    listener.start_listening()


def run_server(host: str = "0.0.0.0", port: int = 8000, reload: bool = False):
    """Run FastAPI server"""
    import uvicorn

    print(f"Starting SoundToAct API server on {host}:{port}...")
    print(f"API docs will be available at http://{host}:{port}/docs")

    uvicorn.run("app.api:app", host=host, port=port, reload=reload)


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="SoundToAct - Voice-triggered automation app",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py cli                    # Run in CLI mode
  python main.py server                 # Run API server
  python main.py server --port 3000     # Run API server on port 3000
  python main.py server --reload        # Run with auto-reload (dev mode)
        """,
    )

    parser.add_argument(
        "mode",
        choices=["cli", "server"],
        help="Run mode: 'cli' for command-line interface, 'server' for API server",
    )
    parser.add_argument(
        "--host",
        default="0.0.0.0",
        help="Server host (default: 0.0.0.0)",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Server port (default: 8000)",
    )
    parser.add_argument(
        "--reload",
        action="store_true",
        help="Enable auto-reload (development mode)",
    )

    args = parser.parse_args()

    try:
        if args.mode == "cli":
            run_cli()
        elif args.mode == "server":
            run_server(host=args.host, port=args.port, reload=args.reload)
    except KeyboardInterrupt:
        print("\n\nShutting down SoundToAct...")
        sys.exit(0)
    except Exception as e:
        print(f"\nError: {e}")
        sys.exit(1)



if __name__ == "__main__":
    main()
