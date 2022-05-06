from searcher import find_content
import random


def search_sentence(word: str):
    """
    Функция находит фильтрует по длине и выдает массив предложений со словом
    """
    correct_text = " ".join([data['content'] for data in find_content.get_content(word)])
    if len(correct_text) > 5000:
        correct_text = correct_text[:5000]
    correct_text = correct_text.split('.')
    return correct_text



def build_correct_sentence_task(word: str):
    """
    Мешает слова в предложениях и выдает массив перемешанных слов
    """
    correct_text = search_sentence(word)
    sentence_count = 0
    task_array = []
    for example_sentences in correct_text:
        sentence_count += 1
        first_sentence = "".join(example_sentences).split(' ')
        first_sentence = random.sample(first_sentence, len(first_sentence))
        task_array.append(" ".join(first_sentence))
        if sentence_count == 5:
            return task_array
    return task_array


def checker(task_word, sentence):
    """
    Проверка выполнения задания Проверка каждого предложения на правлиьность составления.
    Оценку варрирует correct_point
    """
    correct_sentence = search_sentence(task_word)
    correct_point = 0
    study_sentences = sentence.split('.')
    for i in range(len(study_sentences)):
        if study_sentences[i] == correct_sentence[0]:
            correct_point += 1
    return 'Молодец ты крут' if correct_point >= 3 else 'Попробуй еще раз'

