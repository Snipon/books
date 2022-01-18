import requests, json, sys, getopt, math
from progress.bar import IncrementalBar

session = requests.Session()


def main(argv):
    query = ""
    outputfile = ""

    try:
        opts, args = getopt.getopt(argv, "ho:q:", ["ofile=", "query="])
    except getopt.getopt.GetoptError:
        print("books.py -o <outputfile>.json -q <query>")
        sys.exit(2)
    for opt, arg in opts:
        if opt == "-h":
            print("books.py -o <outputfile>.json -q <query>")
            sys.exit()
        elif opt in ("-o", "--ofile"):
            outputfile = arg
        elif opt in ("-q", "--query"):
            query = arg

    print("Output: ", outputfile, "\nQuery: ", query)

    offset = 0
    url = "https://openlibrary.org/search.json"
    first = session.get(
        url, params={"offset": offset, "language": "dan", "q": query}
    ).json()

    totalpages = math.ceil(first["numFound"] / 100)
    page = 0

    bar = IncrementalBar("Importing page", max=totalpages)

    with open(outputfile, "w") as file:
        result = {"total": first["numFound"], "data": []}

        while first["numFound"] > offset:
            page += 1
            offset += 100
            bar.next()

            next_page = session.get(
                url, params={"offset": offset, "language": "dan", "q": query}
            ).json()

            for doc in next_page["docs"]:
                result["data"].append(doc)

        file.write(json.dumps({"result": result}))
        file.close()
        bar.finish()


if __name__ == "__main__":

    main(sys.argv[1:])
