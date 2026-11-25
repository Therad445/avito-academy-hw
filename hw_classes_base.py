from math import log


TRAIN_CORPUS = [
    'Марс сигнал сигнал',
    'Марс пыль',
    'Марс сигнал антенна',
]

CHECK_CORPUS = [
    'СИГНАЛ шум сигнал',
    'антенна пыль',
    'марс марс марс',
    'комета',
    '',
]


class CountVectorizer:
    """Считает вхождения слов или биграмм из обученного словаря."""

    def __init__(self, lowercase=True, ngram_size=1):
        if ngram_size not in (1, 2):
            raise ValueError('ngram_size должен быть равен 1 или 2')
        self.lowercase = lowercase
        self.ngram_size = ngram_size
        self._vocabulary = {}

    @property
    def vocabulary(self):
        return self._vocabulary

    @vocabulary.setter
    def vocabulary(self, vocabulary):
        indices = list(vocabulary.values())
        if any(not isinstance(index, int) or isinstance(index, bool)
               for index in indices):
            raise ValueError('Индексы слов должны быть целыми числами')
        if sorted(indices) != list(range(len(indices))):
            raise ValueError('Индексы должны идти с нуля без пропусков')
        self._vocabulary = vocabulary.copy()

    @vocabulary.deleter
    def vocabulary(self):
        self._vocabulary = {}

    def add_word(self, word):
        if word not in self._vocabulary:
            self._vocabulary[word] = len(self._vocabulary)
        return self._vocabulary[word]

    def tokenize(self, text):
        if self.lowercase:
            text = text.lower()
        words = text.split()
        if self.ngram_size == 1:
            return words
        return [' '.join(words[index:index + 2])
                for index in range(len(words) - 1)]

    def fit(self, corpus):
        new_vectorizer = CountVectorizer(self.lowercase, self.ngram_size)
        for text in corpus:
            for word in self.tokenize(text):
                new_vectorizer.add_word(word)
        if not new_vectorizer.vocabulary:
            raise ValueError('В корпусе нет слов для обучения')
        self.vocabulary = new_vectorizer.vocabulary
        return self

    def transform(self, corpus):
        if not self._vocabulary:
            raise RuntimeError(
                'Сначала обучите векторизатор или задайте словарь'
            )
        matrix = []
        for text in corpus:
            counts = [0] * len(self._vocabulary)
            for word in self.tokenize(text):
                if word in self._vocabulary:
                    counts[self._vocabulary[word]] += 1
            matrix.append(counts)
        return matrix

    def get_feature_names(self):
        return sorted(self._vocabulary, key=self._vocabulary.get)

    def fit_transform(self, corpus):
        corpus = list(corpus)
        return self.fit(corpus).transform(corpus)

    def to_dict(self):
        return {
            'lowercase': self.lowercase,
            'ngram_size': self.ngram_size,
            'vocabulary': self._vocabulary.copy(),
        }

    @classmethod
    def from_dict(cls, state):
        vectorizer = cls(
            lowercase=state['lowercase'],
            ngram_size=state['ngram_size'],
        )
        vectorizer.vocabulary = state['vocabulary']
        return vectorizer


class BinaryVectorizer(CountVectorizer):
    """Отмечает наличие признака единицей."""

    def transform(self, corpus):
        matrix = super().transform(corpus)
        return [[int(count > 0) for count in row] for row in matrix]


class TfidfVectorizer(CountVectorizer):
    """Вычисляет TF или TF-IDF без дополнительной нормализации."""

    def __init__(self, lowercase=True, use_idf=True, ngram_size=1):
        super().__init__(lowercase=lowercase, ngram_size=ngram_size)
        self.use_idf = use_idf
        self._idf = []

    @property
    def idf(self):
        return self._idf.copy()

    @classmethod
    def from_config(cls, config):
        return cls(
            lowercase=config.get('lowercase', True),
            use_idf=config.get('use_idf', True),
        )

    def fit(self, corpus):
        corpus = list(corpus)
        super().fit(corpus)
        self._idf = []
        if self.use_idf:
            document_counts = [0] * len(self._vocabulary)
            for text in corpus:
                for word in set(self.tokenize(text)):
                    document_counts[self._vocabulary[word]] += 1
            self._idf = [
                log((len(corpus) + 1) / (count + 1)) + 1
                for count in document_counts
            ]
        return self

    def transform(self, corpus):
        matrix = super().transform(corpus)
        if self.use_idf and len(self._idf) != len(self._vocabulary):
            raise RuntimeError('Для TF-IDF сначала вызовите fit()')
        result = []
        for counts in matrix:
            total = sum(counts)
            if total == 0:
                result.append([0.0] * len(counts))
                continue
            weights = [count / total for count in counts]
            if self.use_idf:
                weights = [weight * idf
                           for weight, idf in zip(weights, self._idf)]
            result.append(weights)
        return result


class KeywordExtractor:
    """Выбирает ключевые слова по весам переданного векторизатора."""

    def __init__(self, vectorizer, top_n=3):
        self.vectorizer = vectorizer
        self.top_n = top_n

    @property
    def top_n(self):
        return self._top_n

    @top_n.setter
    def top_n(self, value):
        if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
            raise ValueError('top_n должен быть положительным целым числом')
        self._top_n = value

    def fit(self, corpus):
        self.vectorizer.fit(corpus)
        return self

    def extract(self, corpus):
        words = self.vectorizer.get_feature_names()
        matrix = self.vectorizer.transform(corpus)
        result = []
        for weights in matrix:
            pairs = [(word, weight) for word, weight in zip(words, weights)
                     if weight > 0]
            pairs.sort(key=lambda pair: (-pair[1], pair[0]))
            result.append(pairs[:self.top_n])
        return result


def demo():
    # 1. TF-IDF: неизвестные слова пропускаются, idf возвращает копию.
    tfidf = TfidfVectorizer.from_config({})
    train_matrix = tfidf.fit_transform(TRAIN_CORPUS)
    print('1. Веса TF-IDF')
    print('Слова:', tfidf.get_feature_names())
    print('IDF:', tfidf.idf)
    print('Обучающий корпус:', train_matrix)
    print('Проверочный корпус:', tfidf.transform(CHECK_CORPUS))
    idf = tfidf.idf
    idf.clear()
    print('IDF после очистки копии:', tfidf.idf)

    # 2. Сохраняем регистр, отключаем IDF и проверяем замену словаря.
    tf = TfidfVectorizer.from_config({
        'lowercase': False,
        'use_idf': False,
    })
    tf_matrix = tf.fit_transform(['Марс марс', 'МАРС сигнал'])
    print('\n2. Настройки и повторное обучение')
    print('Слова:', tf.get_feature_names())
    print('IDF:', tf.idf)
    print('TF:', tf_matrix)
    tfidf.fit(['Венера облака'])
    print('Новый словарь:', tfidf.get_feature_names())
    print('Новый IDF:', tfidf.idf)
    print('Новая матрица:', tfidf.transform(['Марс Венера облака']))

    # 3. Меняем число ключевых слов и обрабатываем неверный top_n.
    extractor = KeywordExtractor(tfidf, top_n=2)
    extractor.fit(TRAIN_CORPUS)
    print('\n3. Ключевые слова')
    print('top_n=2:', extractor.extract(CHECK_CORPUS))
    extractor.top_n = 1
    print('top_n=1:', extractor.extract(CHECK_CORPUS))
    try:
        extractor.top_n = 0
    except ValueError as error:
        print('Ошибка:', error)


if __name__ == '__main__':
    demo()
