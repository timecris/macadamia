import urllib, urlparse
import macadamia
from bs4 import BeautifulSoup

URLS = {
	"base": "http://www.gwtorrent.com/bbs/",
	"search": "board.php?bo_table={CATEGORY}&sfl=wr_subject&stx={KEYWORD}&sop=and",
	"article": "board.php?bo_table={CATEGORY}&wr_id={ID}",
	"download": "download.php?bo_table={CATEGORY}&wr_id={ID}"
}
CATEGORIES = ["torrent_drama", "torrent_ent"]
HOSTNAME = "gwtorrent.com"

def do_search(category, keyword):
	encodedKeyword = urllib.quote_plus(keyword)
	searchUrl = URLS["base"]
	searchUrl += URLS["search"].replace("{CATEGORY}", category)
	searchUrl = searchUrl.replace("{KEYWORD}", encodedKeyword)

	html = collector.retrieve(searchUrl)
	parseHtml = BeautifulSoup(html)
	return parseHtml

def do_filter(html):
	return html.find_all("td", class_="mw_basic_list_subject")

def do_collect(filtered):
	for entry in filtered:
		anchor = entry.find_all("a")[0]
		anchorUrl = anchor.attrs["href"]
		anchorInfo = {
			"title": anchor.text,
			"dataId": urlparse.parse_qs(anchorUrl)['wr_id'][0]
		}

		print "{0} ({1}/{2}) ...".format(
			anchorInfo["title"].encode("utf8"),
			filtered.index(entry) + 1,
			len(filtered)
		)

		articleUrl = article_0.replace("{ID}", anchorInfo["dataId"])
		seedUrl = seed_0.replace("{ID}", anchorInfo["dataId"])

		collector.retrieve(articleUrl)
		collector.addTorrent(HOSTNAME, anchorInfo["title"], collector.retrieve(seedUrl))

def do(root):
	global collector, article_0, seed_0
	collector = root
	for category in CATEGORIES:
		article_0 = URLS["base"] + URLS["article"].replace("{CATEGORY}", category)
		seed_0 = URLS["base"] + URLS["download"].replace("{CATEGORY}", category)

		parseHtml = do_search(category, collector.KEYWORD)
		entryDatas = do_filter(parseHtml)

		if len(entryDatas) == 0:
			continue

		do_collect(entryDatas)
