import spacy
from spacy.lang.pt.stop_words import STOP_WORDS as sw_pt
from spacy.lang.en.stop_words import STOP_WORDS as sw_en
from sklearn.feature_extraction.text import CountVectorizer
import argparse


def summarization(args):
    if args.lang == "PT":
        stopwords = sw_pt
        
        if args.method == "eff":
            model = spacy.load("pt_core_news_sm")

        elif args.method == "acc":
            model = spacy.load("pt_core_news_lg")

        else:
            print("Unsupported method")

    elif args.lang == "EN":
        stopwords = sw_en
        
        if args.method == "eff":
            model = spacy.load("en_core_web_sm")

        elif args.method == "acc":
            model = spacy.load("en_core_web_trf")

        else:
            raise ValueError("Unsupported method")

    else:
        raise ValueError("Unsupported language")

    text = str(input("Enter text: \n"))

    doc = model(text)

    text_lower = [sent.text.lower() for sent in doc.sents]

    cv = CountVectorizer(stop_words=list(stopwords))
    cv_fit = cv.fit_transform(text_lower)
    word_list = cv.get_feature_names()
    count_list = cv_fit.toarray().sum(axis=0)

    word_frequency = dict(zip(word_list, count_list))

    val = sorted(word_frequency.values())

    if args.most_common:
        higher_word_frequencies = [
            word for word, freq in word_frequency.items() if freq in val[-3:]
        ]
        print(f"\nMost frequent words: {higher_word_frequencies}")

    higher_frequency = val[-1]
    for word in word_frequency.keys():
        word_frequency[word] /= higher_frequency

    sentence_rank = {}
    for sent in doc.sents:
        for word in sent:
            if word.text.lower() in word_frequency.keys():
                if sent in sentence_rank.keys():
                    sentence_rank[sent] += word_frequency[word.text.lower()]
                else:
                    sentence_rank[sent] = word_frequency[word.text.lower()]

    top_sentences = sorted(sentence_rank.values())[::-1]
    top_sent = top_sentences[: args.nsentences]

    summary = []
    for sent, strength in sentence_rank.items():
        if strength in top_sent:
            summary.append(sent)

    return text, summary


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Document summarizer")

    parser.add_argument(
        "--nsentences",
        dest="nsentences",
        default=3,
        type=int,
        help="How many sentences will be in the summary (default: 3)",
    )

    parser.add_argument(
        "--lang",
        dest="lang",
        default="PT",
        type=str,
        help="Input text language: 'PT' (default) or 'EN'",
    )

    parser.add_argument(
        "--method",
        dest="method",
        default="eff",
        type=str,
        help="Choose method: 'eff' (default, faster, but less acurate) or 'acc' (slower, but more accurate)",
    )
    
    parser.add_argument(
        "--most_common",
        dest="most_common",
        default=False,
        type=bool,
        help="Choose to show the most frequents words (default: False)",
    )

    args = parser.parse_args()

    text, summary = summarization(args)

    print("\n")
    for i in summary:
        print(i, end=" ")
    print("\n")
