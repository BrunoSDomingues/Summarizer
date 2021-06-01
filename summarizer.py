import argparse
import spacy
import warnings
from spacy.lang.pt.stop_words import STOP_WORDS as sw_pt
from spacy.lang.en.stop_words import STOP_WORDS as sw_en
from sklearn.feature_extraction.text import CountVectorizer


def summarization(args):
    if args.lang == "PT":
        stopwords = sw_pt

        if args.method == "eff":
            model = spacy.load("pt_core_news_sm")

        elif args.method == "acc":
            model = spacy.load("pt_core_news_lg")

        else:
            raise ValueError("Unsupported method")

    elif args.lang == "EN":
        # Não sei ao certo porque, mas este warning aparece nos stopwords em inglês somente
        warnings.filterwarnings(
            "ignore",
            message="Your stop_words may be inconsistent with your preprocessing.",
        )
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

    # Carrega o texto com o modelo selecionado
    doc = model(text)

    # Coloca os chars em minusculo
    text_lower = [sent.text.lower() for sent in doc.sents]

    # CountVectorizer
    cv = CountVectorizer(stop_words=list(stopwords))
    cv_fit = cv.fit_transform(text_lower)
    word_list = cv.get_feature_names()
    count_list = cv_fit.toarray().sum(axis=0)

    # Calcula a frequencia das palavras e ordena o dicionario pela frequecia
    word_frequency = dict(zip(word_list, count_list))
    val = sorted(word_frequency.values())

    # Se most_common for True, mostra as palavras mais comuns
    if args.most_common:
        most_frequent = [
            word for word, freq in word_frequency.items() if freq in val[-3:]
        ]
        print(f"\nMost frequent words: {most_frequent}")

    # Pega a maior frequencia e calcula as frequencias relativas a ela
    higher_frequency = val[-1]

    for word in word_frequency.keys():
        word_frequency[word] /= higher_frequency

    # Faz o ranking das frases
    sentence_rank = {}
    for sent in doc.sents:
        for word in sent:
            if word.text.lower() in word_frequency.keys():
                if sent in sentence_rank.keys():
                    sentence_rank[sent] += word_frequency[word.text.lower()]
                else:
                    sentence_rank[sent] = word_frequency[word.text.lower()]

    # Faz um sorting dos ranks de cada frase, coloca em ordem decrescente e depois seleciona as n frases
    top_sent = sorted(sentence_rank.values())[::-1][: args.nsentences]

    # Gera o sumario
    summary = [sent for sent, strength in sentence_rank.items() if strength in top_sent]

    return summary


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A simple document summarizer")

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
        help="Choose method for summarizing: 'eff' (default) (faster, but less acurate) or 'acc' (slower, but more accurate)",
    )

    parser.add_argument(
        "--most_common",
        dest="most_common",
        default=False,
        type=bool,
        help="Choose to show the most frequents words (default: False)",
    )

    args = parser.parse_args()

    summary = summarization(args)

    print("\n")
    for s in summary:
        print(s, end=" ")
    print("\n")
