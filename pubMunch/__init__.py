import argparse

from . import pubCrawlLib

def download_pmid(pmid):
    meta = pubCrawlLib.getArticleMeta(pmid)
    pdf_file = pubCrawlLib.crawlOneDoc(meta, doc_type='pdf')
    return pdf_file

def download_pmid_program():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('pmid', type=str, help='The pubmed id to download')

    args = parser.parse_args()

    print(args)

    pdf_file = download_pmid(args.pmid)

    with open('{}.pdf'.format(args.pmid), 'wb') as file:
        file.write(pdf_file)

