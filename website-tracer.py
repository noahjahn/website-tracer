import argparse
import sys
from bs4 import BeautifulSoup
import requests
import requests.exceptions
from urllib.parse import urlsplit
from urllib.parse import urlparse
from collections import deque
from heapq import heappush, heappop

def get_heuristic(local_url):
    return len(local_url.split('/')) - 1

def get_local_url_from_public(public_url, top_level_domain):
    return public_url.split(top_level_domain)[1]

def is_public_url(url, expected_domain, expected_top_level_domain):
    if not url.find(expected_domain + expected_top_level_domain) == -1:
        return 1
    elif not url.find(expected_domain + expected_top_level_domain) == -1:
        return 1
    else:
        return -1


parser = argparse.ArgumentParser(
    description="python website-tracer.py https://reddit.com https://reddit.com/r/news",
)

parser.add_argument("src", help="specify the source webpage you would like to start from")
parser.add_argument("dest", help="specify the destination webpage on the same website as src you would like to trace to")

if len(sys.argv) == 1:
    parser.print_help(sys.stderr)
    sys.exit(1)

args = parser.parse_args()

src = args.src
dest = args.dest

protocols = (
    "https://",
    "http://"
)
top_level_domains = (
    ".com",
    ".org",
    ".net",
    ".dev",
    ".edu",
    ".gov",
    ".info",
    ".biz",
    ".us",
)

# If dest is the same as src, print error and exit
if src.find(dest) >= 0:
    print("Please choose a different dest url from the chosen src")
    sys.exit(1)

# If src is not in destination, print error and exit
if not dest.find(src) == 0:
    print ("Please provide a dest url on the same website as src")
    sys.exit(1)

# Check if valid top level domain
for domain in top_level_domains:
    if not src.find(domain) == -1:
        is_src_valid = 1
        src_top_level_domain = domain
        if not dest.find(domain) == -1:
            is_dest_valid = 1
            dest_top_level_domain = domain
        else:
            is_dest_valid = 0
        break
    else:
        is_src_valid = 0

# Print error if invalid top level domain and exit
if not is_src_valid:
    print("Please provide a src with a valid top-level domain")
    sys.exit(1)

if not is_dest_valid:
    print("Please provide a dest with the same top-level domain as src")
    sys.exit(1)

# Check if valid protocol
for protocol in protocols:
    if not src.find(protocol) == -1:
        is_src_valid = 1
        src_protocol = protocol
        if not dest.find(protocol) == -1:
            is_dest_valid = 1
            dest_protocol = protocol
        else:
            is_dest_valid = 0
        break
    else:
        is_src_valid = 0

# Print error if invalid protocol and exit
if not is_src_valid:
    print("Please provide a src with a valid protocol")
    sys.exit(1)

if not is_dest_valid:
    print("Please provide a dest with the same protocol as src")

# Get src and dest domain
src_split = src.split('.', 3)
if src_split[1] == src_top_level_domain.split('.')[1]:
    domain = src_split[0].split(src_protocol, 1)[1]
    subdomain = ''
elif src_split[2] == src_top_level_domain.split('.')[1]:
    domain = src_split[1]
    subdomain = src_split[0]
else:
    print("Please provide a valid src url")
    sys.exit(1)

base_url = src_protocol + subdomain + '.' + domain + src_top_level_domain + src.split(src_top_level_domain, 2)[1]
dest_heuristic = get_heuristic(get_local_url_from_public(dest, dest_top_level_domain))

urls_to_traverse = []

response = requests.get(src)
soup = BeautifulSoup(response.text, "lxml")

for link in soup.find_all('a'):
    anchor = link.attrs["href"] if "href" in link.attrs else ''
    print(anchor)
    if is_public_url(anchor, domain, src_top_level_domain) == 1:
        print(get_heuristic(get_local_url_from_public(anchor, src_top_level_domain)))
    else:
        print(get_heuristic(anchor))
# try:
#     response = requests.get(src)
# except(requests.exceptions.MissingSchema, requests.exceptions.ConnectionError, requests.exceptions.InvalidURL, requests.exceptions.InvalidSchema):
#     # add broken urls to it’s own set, then continue
#     broken_urls.add(url)
# continue

