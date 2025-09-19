import csv
import json
from retriever import RetrieverService

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--csv', help='knowledge.csv file', required=False)
    parser.add_argument('--json', help='knowledge.json file', required=False)
    args = parser.parse_args()

    r = RetrieverService()
    docs = []
    if args.csv:
        with open(args.csv, encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                docs.append({'id': row['id'], 'text': row['text']})
    if args.json:
        with open(args.json, encoding='utf-8') as f:
            data = json.load(f)
            for row in data:
                docs.append({'id': row['id'], 'text': row['text']})
    if docs:
        r.add_documents(docs)
        print('Upserted', len(docs), 'docs to Pinecone')
    else:
        print('No docs provided')
