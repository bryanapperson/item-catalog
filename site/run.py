#!/usr/bin/env python
"""Run the item_catalog application."""

from item_catalog import app
import sys


def main():
    """Main function for application server."""
    try:
        portnum = 8080
        address = '0.0.0.0'
        print("Web Server running on port %s" % portnum)
        app.run(host=address, port=portnum)
    except KeyboardInterrupt:
        print(" entered, stopping web server....")
        sys.exit(0)
    except Exception:
        print("Uncaught exception!")
        sys.exit(1)


if __name__ == '__main__':
    main()
