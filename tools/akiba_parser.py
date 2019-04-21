import newspaper
from datetime import datetime, timedelta, timezone
import pytz
import csv
from queue import Queue
from threading import Thread

OUTPUT_BASENAME = "articles"
ADDRESSES = ["https://www.archdaily.com",
             "https://venturebeat.com/",
             "https://www.tokyodev.com",
             "https://www.popsci.com",
             "https://www.citylab.com",
             "https://longreads.com",
             "https://kotaku.com",
             "https://www.independent.co.uk",
             "https://interestingengineering.com",
             "https://www.mirror.co.uk",
             "https://www.dezeen.com/",
             "https://www.disruptingjapan.com/",
             "http://bloomberg.com",
             "http://arstechnica.com/",
             "http://wired.com/",
             "http://bbc.co.uk/",
             "http://cnn.com/",
             "http://theverge.com/",
             "http://readwriteweb.com/",
             "http://theatlantic.com/",
             "http://theguardian.com/",
             "http://guardian.co.uk/",
             "http://slate.com/",
             "http://theregister.co.uk/",
             "http://technologyreview.com/",
             "http://posterous.com/",
             "http://gizmodo.com/",
             "http://bbc.com/",
             "http://businessweek.com/",
             "http://allthingsd.com/",
             "https://spectrum.ieee.org/",
             "http://newyorker.com/",
             "http://qz.com/",
             "http://vice.com/",
             "http://time.com/",
             "http://techdirt.com/",
             "https://hbr.org/",
             "http://extremetech.com/",
             "https://www.juxtapoz.com/"
             ]

japanese_blogs = ["https://blog.gaijinpot.com/", ]

titles = []
entries = []


def parse_article(paper):
    """

    :param paper:
    :return:
    """

    # parse articles / blog entries of the website
    # for article in paper.articles:

    articles = paper.articles
    # parse articles / blog entries of the website
    for article in articles:
        # try to download and parse the article, if error pass to the next one
        try:
            article.download()
            article.parse()
        except:
            continue

        # do the NLP treatment on the article (recover keywords and summary)
        article.nlp()

        for keyword in article.keywords:
            # check if there is japan/japanese in the keywords and that we haven't already had this title
            if ("japan" in keyword.lower() or "akihabara" in keyword.lower() or "tokyo" in keyword.lower()) and article.title not in titles:
                titles.append(article.title)
                print("++++++++++++++++++++++", article.url)
                entry = [str(article.publish_date), paper.brand, article.title, article.top_image, article.url]
                entries.append(entry)
                break


class DownloadWorker(Thread):
    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            # Get the work from the queue and expand the tuple
            paper = self.queue.get()
            parse_article(paper)
            self.queue.task_done()

def write_output_file(articles):

    date_to_seconds = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = OUTPUT_BASENAME + date_to_seconds + ".csv"

    if articles:
        # creating / overwriting the output file
        with open(filename, 'a') as output_file:
            output_file.write("sep=," + "\n")
            output_writer = csv.writer(output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for article in articles:
                output_writer.writerow(article)
    else:
        print("======================== NO ARTICLES TO WRITE. OUTPUT FILE WILL NOT BE CREATED.")


def main():

    # Create a queue to communicate with the worker threads
    queue = Queue()

    worker = DownloadWorker(queue)
    # Setting daemon to True will let the main thread exit even though the workers are blocking
    worker.daemon = True
    worker.start()

    # for every website in the list
    for address in ADDRESSES:
        address = address.strip()
        # instantiate newspaper object for website
        paper = newspaper.build(address, memoize_articles=True)

        # print out the address of current website
        print("=========================== PARSING ARTICLES for ", address, ", size: ", paper.size())

        # Put the tasks into the queue as a tuple
        queue.put(paper)

    # Causes the main thread to wait for the queue to finish processing all the tasks
    queue.join()

    write_output_file(entries)

if __name__ == '__main__':
    main()
