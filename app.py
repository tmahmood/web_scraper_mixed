"""
entry point of the application
"""
import sys
from app import runner
import logging

MESSAGE = """
Parameter missing:

SEEK
py app.py seek "<keyword>"

GUMTREE
py app.py gumtree "<keyword>"

"""


def main():
    """
    Entry point
    """
    logging.basicConfig(
        format='[%(levelname)s] - %(message)s',
        level=logging.INFO)
    if len(sys.argv) < 3:
        logging.error(MESSAGE)
        sys.exit(1)
    scraper = sys.argv[1]
    keyword = sys.argv[2]
    if scraper not in ['seek', 'gumtree']:
        raise NotImplementedError()
    app = runner.Runner(scraper, keyword)
    app.run()


if __name__ == '__main__':
    main()
