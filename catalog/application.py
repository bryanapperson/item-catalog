#!/usr/bin/env python
"""Development server to run the item_catalog application."""

from item_catalog import app
import sys


def main():
    """Main function for application server."""
    try:
        portnum = 8080
        address = '0.0.0.0'
        app.run(host=address, port=portnum)
    except Exception:
        print("Uncaught exception!")
        sys.exit(1)
    # All is well that ends well.
    sys.exit(0)


if __name__ == '__main__':
    main()
