import epub
from space import client, parser
import argparse

cmdparser = argparse.ArgumentParser(
    description="Returns spacebattles fic epub."
)
cmdparser.add_argument("link", help="Link to specific fic on Spacebattles")
args = cmdparser.parse_args()
if args.link:
    scraper = client.Mine(args.link)
    content = parser.Parser(scraper.responses)

