import wanikani_provider
from os import environ

def main():
    wk_api_key = environ.get("WK_API_KEY")

    if wk_api_key is None:
        raise EnvironmentError('Missing environment variable WK_API_KEY')

    wk_provider = wanikani_provider.WanikaniKnownWordsProvider(wk_api_key)

    known_words = wk_provider.get_known_words()
    # known_words = wk_provider.get_known_words(False)  # No cache
    print(known_words)


if __name__ == '__main__':
    # Only run if this is the entrypoint of the program (for testing purposes)
    main()
