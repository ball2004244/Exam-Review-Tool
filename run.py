import json
import sys
from pathlib import Path
from typing import List, Tuple
from random import sample
import pandas as pd


class QuestionBank:
    def __init__(self, path: str) -> None:
        self.questions = pd.read_csv(path, header=None, names=[
                                     'question', 'answer', 'tags'])

        self.count = self.questions.shape[0]

    def get_random_questions(self, num_questions: int) -> List[Tuple[str, str]]:
        '''
        Randomly selects n questions from the question bank
        to build up a mock exam. The random algorithm initially
        based on the random module.

        Later on, this will be replaced by a more sophisticated algorithm
        to takes into account question types and tags.

        Return with pairs of random questions and answers
        '''

        selected_idx = sample(
            range(self.count), min(num_questions, self.count))

        selected_qa = self.questions.iloc[selected_idx]
        return list(zip(selected_qa['question'], selected_qa['answer']))


class Exam:
    def __init__(self, question_pairs: List[Tuple[str, str]]) -> None:
        '''
        A question pair contains of 1 question & 1 answer
        '''
        self.question_pairs = question_pairs

    def format_ascii_math(self, text: str) -> str:
        '''
        Format ASCII Math to Markdown
        '''
        #TODO: Implement this function
        return text
        # return f'${text}$'

    def format_question(self, order: int, question: str) -> str:
        '''
        Load Markdown template for question
        '''
        formatted_question = f'{order}. {self.format_ascii_math(question)}'
        
        return formatted_question

    def format_answer(self, id: int, answer: str) -> str:
        '''
        Load Markdown template for answer
        '''

        formatted_answer = ''
        with open('format_answer.html', 'r') as f:
            formatted_answer = f.read()
            
        formatted_answer = formatted_answer.replace('{{final_answer}}', self.format_ascii_math(answer))
        formatted_answer = formatted_answer.replace('{{id}}', str(id))
        
        return formatted_answer

    def display_question(self, path: str) -> None:
        '''
        Display the exam in a html format on the browser
        '''
        with open(path, 'w') as f:
            f.write(f'{i+1}. {qa_pair[0]}\n\n')
            
            for i, qa_pair in enumerate(self.question_pairs):
                formatted_question = self.format_question(i + 1, qa_pair[0])
                formatted_answer = self.format_answer(i, qa_pair[1])

                f.write(f'<br>{formatted_question}<br>{formatted_answer}')
            f.write('<br>')

    def save_to_file(self, path: str) -> None:
        '''
        Generate a raw text file for download
        '''
        with open(path, 'w') as f:
            for i, qa_pair in enumerate(self.question_pairs):
                f.write(f'{i+1}. {qa_pair[0]}\n\n')


class Config:
    def __init__(self, path: str) -> None:
        with open(path, 'r') as f:
            self.config = json.load(f)

    def get_num_questions(self) -> int:
        return self.config['num_questions']


def main() -> None:
    # Defines path
    in_dir, out_dir = Path(sys.argv[1]), Path(sys.argv[2])
    question_bank_path = in_dir / 'question_bank.csv'
    inp_dict_path = in_dir / 'variables.dictionary'
    display_file = out_dir / 'display_exam.txt'
    download_file = out_dir / 'mock_exam.txt'

    # Set up input
    question_bank = QuestionBank(question_bank_path)
    config = Config(inp_dict_path)

    # Main Logic
    question_pairs = question_bank.get_random_questions(
        config.get_num_questions())
    exam = Exam(question_pairs)

    # Process output
    exam.display_question(display_file)
    exam.save_to_file(download_file)


if __name__ == '__main__':
    main()
