import argparse

from . import pubCrawlLib

def download_pmid():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('pmid', type=str, help='The pubmed id to download')

    args = parser.parse_args()

    print(args)

    meta = pubCrawlLib.downloadPubmedMeta(args.pmid)
    pdf_file = pubCrawlLib.crawlOneDoc(meta, doc_type='pdf')

    with open('{}.pdf'.format(args.pmid), 'wb') as file:
        file.write(pdf_file)

