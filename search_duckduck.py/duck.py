from duckduckgo_search import ddg

def search_duckduckgo(query, max_results=5):
    results = ddg(query, max_results)
    for idx, result in enumerate(results):
        print(f"{idx + 1}. {result['title']}")
        print(result['href'])
        print(result['body'])
        print("-" * 40)

if __name__ == "__main__":
    keyword = input("Enter search query: ")
    search_duckduckgo(keyword)
