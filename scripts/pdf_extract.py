
from app.utils.adobe import extract, adobe_credentials
import argparse


def main(input_file: str):
    with open(input_file, 'rb') as f:
        content = f.read()
    
    test = extract(adobe_credentials, content)
    print(test)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input-file", type=str)
    args = parser.parse_args()
    main(args.input_file)




# file_path = "/Users/guiwoso/Documents/Personal/ARGO/_AI Input Proposals/Known/BC Transit/RFP.pdf"
