# Exam Review Tool - The Ultimate Self-Study App

## Introduction

Our app is designed to help students prepare for exams more effectively. It gives more control to the students by allowing them to create their own exams and review them. Simply upload a csv file with the questions and answers and the app will take care of the rest.

## Question Bank

The question bank is a csv file with no header.

The csv file should have the following format:

```
questions, answers, tags
```

You can have more than 1 tag, just separate them with a semicolon. We will use the tags to filter the questions when creating an exam.

For example:

```
What is the capital of France?, Paris, geography;capital cities
```

## Question Tags

You don't have to use tags, but they can be useful to filter the questions to generate the most relevant exam for you.

For each tag, it should follow the format `tag: count`. The count is the number of questions you want to include in the exam. If you don't specify the count, we will include all the questions with that tag.

Here is how you would use tags during exam creation:

```
geography: 30, calculus: 20, physics: 100
```

## Math Notation

You might want to use math notation in your questions. We support ASCII Math notation, remember to wrap your texts between 2 backtick signs \`\`. For more information about ASCII Math syntax, check out [here](https://asciimath.org/)

If the mock exam does not display the math notation correctly, you can try to refresh the page or use a different browser.

## Create your own exam here

1. Upload your question bank (get default question bank [here](https://raw.githubusercontent.com/ball2004244/Exam-Review-Tool/main/batches/standard/input/question_bank.csv)):
   { question_bank }

2. How many questions would you like to have?
   { num_questions }

3. What question tags would you like to have? (Leave blank to include all)
   { question_tags }
