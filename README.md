# Summarizer

Um sumarizador de textos recebidos via input.

## Método utilizado

Utilizou-se da biblioteca `spacy` para pegar modelos de linguagem já preparados em conjunto com o `CountVectorizer` da biblioteca Scikit-learn.

## Requerimentos para funcionar

1) Baixar o `spacy` e o `scikit-learn` via `pip install`
2) Rodar os commandos abaixo:
    - `python -m spacy download pt_core_news_sm` (utilizado para interpretar textos em português com o método mais eficiente)
    - `python -m spacy download pt_core_news_lg` (utilizado para interpretar textos em português com o método mais preciso)
    - `python -m spacy download en_core_web_sm` (utilizado para interpretar textos em inglês com o método mais eficiente)
    - `python -m spacy download en_core_web_trf` (utilizado para interpretar textos em inglês com o método mais preciso)

## Como utilizar

Basta rodar o programa `summarizer.py`. Há argumentos que podem ser utilizados no programa (rodar com `-h`ou `--help` para ver os possíveis argumentos.)
Há exemplos de textos para utilizar na pasta `examples`.

**IMPORTANTE:** Os textos devem ser uma frase única, sem a presença do caractere `\n` (caso ele esteja presente o input sai quebrado)
