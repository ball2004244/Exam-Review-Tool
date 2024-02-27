# Exam Review Platform - The Ultimate Self-Study App

## Introduction

Our app is designed to help students prepare for exams more effectively. It gives more control to the students by allowing them to create their own exams and review them. Simply upload a csv file with the questions and answers and the app will take care of the rest.

## CSV Format

The csv file should have the following format:

```
questions, answers, tags
```

No header is required.

You can have more than 1 tag, just separate them with a semicolon. We will use the tags to filter the questions when creating an exam.

For example:

```
What is the capital of France?, Paris, geography;capital cities
```

## Create your own exam here

1. Upload your question bank (get default question bank [here](https://raw.githubusercontent.com/ball2004244/Exam-Review-Platform/main/batches/standard/input/question_bank.csv)):
   { question_bank }

2. How many questions would you like to have?
   { num_questions }
