"""
entry point of the application
"""
import sys
from app import runner
import logging


def main():
    """
    Entry point
    """
    logging.basicConfig(format='[%(levelname)s] - %(message)s', level=logging.INFO)
    scraper = sys.argv[1]
    keyword = sys.argv[2]
    if scraper not in ['seek', 'gumtree']:
        raise NotImplementedError()
    app = runner.Runner(scraper, keyword)
    app.run()


if __name__ == '__main__':
    main()
