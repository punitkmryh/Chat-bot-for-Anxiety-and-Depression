from collections import namedtuple


Question = namedtuple('Question', ['question', 'answers'])


class BaseQuiz:

    def __init__(self, id, questions, lang, question_number=0, answers=None, created_at=None):
        self.id = id
        self.questions = questions
        self.lang = lang
        self.question_number = question_number
        self.answers = [] if answers is None else answers
        self.created_at = created_at

    def get_question(self):
        raise NotImplementedError

    def save_answer(self, answer):
        self.answers.append(answer)
        self.question_number += 1

    def get_result(self):
        raise NotImplementedError

    @property
    def result(self):
        return sum(self.answers)

    @property
    def is_completed(self):
        return self.question_number == self.questions_count

    @property
    def questions_count(self):
        raise NotImplementedError


class HARSQuiz(BaseQuiz):

    RESULTS = {
        'en': ['mild anxiety severity', 'mild to moderate anxiety severity', 'moderate to severe anxiety severity']}

    type_ = 'hars'

    def get_question(self):
        return Question(
            "\u2753({}/{}) {}".format(
                (self.question_number + 1), self.questions_count,
                self.questions[self.lang]['questions'][self.question_number]),
            self.questions[self.lang]['answers'])

    def get_result(self):
        if not self.is_completed:
            raise ValueError("Can't calculate result for incomplete test")
        if self.result <= 17:
            description = self.RESULTS[self.lang][0]
        elif self.result <= 24:
            description = self.RESULTS[self.lang][1]
        else:
            description = self.RESULTS[self.lang][2]
        return '{}:\n{}/{}\n{}'.format(
            'Результат' if self.lang == 'ru' else 'Result',
            self.result, self.questions_count * 4, description)

    @property
    def questions_count(self):
        return len(self.questions[self.lang]['questions'])


class MADRSQuiz(BaseQuiz):

    RESULTS = {
        'en': ['normal 👍', 'mild depression 😐', 'moderate depression 😔', 'severe depression 😨']}

    type_ = 'madrs'

    def get_question(self):
        return Question(
            "\u2753({}/{}) {}".format(
                (self.question_number + 1), self.questions_count,
                self.questions[self.lang][self.question_number]['question']),
            self.questions[self.lang][self.question_number]['answers'])

    def get_result(self):
        if not self.is_completed:
            raise ValueError("Can't calculate result for incomplete test")
        if self.result <= 6:
            description = self.RESULTS[self.lang][0]
        elif self.result <= 19:
            description = self.RESULTS[self.lang][1]
        elif self.result <= 34:
            description = self.RESULTS[self.lang][2]
        else:
            description = self.RESULTS[self.lang][3]
        return '{}:\n{}/{}\n{}'.format(
            'Результат' if self.lang == 'ru' else 'Result',
            self.result, self.questions_count * 6, description)

    @property
    def questions_count(self):
        return len(self.questions[self.lang])
