import json
import pandas as pd
import sys
import os
from typing import List
from random import sample


class QuestionBank:
    def __init__(self, path: str) -> None:
        self.questions = pd.read_csv(path, header=None, names=[
                                     'question', 'answer', 'tags'])

        self.count = self.questions.shape[0]

    def get_random_questions(self, num_questions: int) -> List[str]:
        '''
        Randomly selects n questions from the question bank
        to build up a mock exam. The random algorithm initially
        based on the random module.

        Later on, this will be replaced by a more sophisticated algorithm
        to takes into account question types and tags.
        '''
        return sample(self.questions['question'].tolist(), min(num_questions, self.count))


class Exam:
    def __init__(self, questions: List[str]):
        self.questions = questions

    def save_to_file(self, path: str):
        with open(path, 'w') as f:
            for i, q in enumerate(self.questions):
                f.write(f'{i+1}. {q}\n\n\n')

class Config:
    def __init__(self, path: str):
        with open(path, 'r') as f:
            self.config = json.load(f)

    def get_num_questions(self):
        return self.config['num_questions']


def main() -> None:
    in_dir, out_dir = sys.argv[1], sys.argv[2]
    question_bank_path = os.path.join(in_dir, 'question_bank.csv')
    inp_dict_path = os.path.join(in_dir, 'variables.dictionary')

    question_bank = QuestionBank(question_bank_path)
    config = Config(inp_dict_path)

    questions = question_bank.get_random_questions(config.get_num_questions())
    exam = Exam(questions)

    out_path = os.path.join(out_dir, 'mock_exam.txt')
    exam.save_to_file(out_path)


if __name__ == '__main__':
    main()
