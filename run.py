import json
import sys
from pathlib import Path
from typing import List, Tuple, Dict
from random import sample
import pandas as pd


class QuestionBank:
    def __init__(self, path: str) -> None:
        self.questions = pd.read_csv(path, header=None, names=[
                                     'question', 'answer', 'tags'])

        self.count = self.questions.shape[0]
        self.all_tags = set()

        for tag in self.questions['tags'].str.strip().str.split(';').explode().unique():
            if not tag.strip():
                continue
            self.all_tags.add(tag.strip())

    def __get_random_questions(self, num_questions: int) -> List[Tuple[str, str]]:
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

    def generate_tags_questions(self, num_questions: int, tags: Dict[str, int]) -> List[Tuple[str, str]]:
        '''
        Generate questions based on tags.
        If no tags are provided, then generate exam using normal random selection
        '''

        # If no tags are provided, then generate exam from all questions
        if tags is None or len(tags) == 0:
            return self.__get_random_questions(num_questions)

        # randomly select questions based on tags
        selected_qa = set()
        for tag, count in tags.items():
            if not tag in self.all_tags:
                continue

            # find all questions with the tag
            tag_idx = self.questions[self.questions['tags'].str.contains(
                tag)].index

            # if there are not enough questions, then select all
            if len(tag_idx) <= count:
                selected_qa.update(tag_idx)
                continue

            # randomly select questions excluding the existed questions
            available_idx = list(set(tag_idx) - selected_qa)
            selected_idx = sample(
                available_idx, min(count, len(available_idx)))
            selected_qa.update(selected_idx)

        # if there are still not enough questions, then select stop

        selected_qa = self.questions.iloc[list(selected_qa)]
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
        # TODO: Implement this function
        return text

    def format_question(self, order: int, question: str) -> str:
        '''
        Load Markdown template for question
        '''
        formatted_question = f'{order}. {question}'

        return formatted_question

    def format_answer(self, id: int, answer: str, template: str = 'static/format_answer.html') -> str:
        '''
        Load Markdown template for answer
        '''

        formatted_answer = ''
        with open(template, 'r') as f:
            formatted_answer = f.read()

        formatted_answer = formatted_answer.replace('{{final_answer}}', answer)
        formatted_answer = formatted_answer.replace('{{id}}', str(id))

        return formatted_answer

    def display_question(self, path: str) -> None:
        '''
        Display the exam in a html format on the browser
        '''
        html_content = ''

        with open(path, 'w') as f:
            for i, qa_pair in enumerate(self.question_pairs):
                formatted_question = self.format_question(i + 1, qa_pair[0])
                formatted_answer = self.format_answer(i, qa_pair[1])

                html_content += f'\n<br>{formatted_question}<br>\n{formatted_answer}'

            f.write(f'{html_content}<br>')

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

    def __get_raw_tags(self) -> str:
        return self.config['question_tags']

    def get_format_tags(self) -> Dict[str, int]:
        # Convert user input string to a dictionary, where each tag is a key
        raw_tags = self.__get_raw_tags()
        tags_dict = {}
        raw_tags = raw_tags.strip().split(',')  # split into pairs
        for i, tag in enumerate(raw_tags):
            # skip invalid tags
            if ':' not in tag:
                continue

            # split into key value pair
            tag, value = tag.split(':')

            tag = tag.strip()
            value = value.strip()

            # skip empty tags
            if tag == '':
                continue

            # if value is not a digit, then set it to default 1
            if not value.isdigit():
                value = 1

            tags_dict[tag.strip()] = int(value)

        return tags_dict


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
    # This does not use tags
    # question_pairs = question_bank.get_random_questions(
    #     config.get_num_questions())

    question_pairs = question_bank.generate_tags_questions(
        config.get_num_questions(), config.get_format_tags())

    exam = Exam(question_pairs)

    # Process output
    exam.display_question(display_file)
    exam.save_to_file(download_file)


if __name__ == '__main__':
    main()
