# QuizApp

QuizApp is a web application that allows user to register and take quizes. They can also follow global leaderboard or follow their friends progress on their profiles.


## Installation
To get started with this project, clone this repository using git:

```bash
git clone https://github.com/juhum/QuizApp.git
```

To run the project, navigate to the QuizApp directory and install the necessary dependencies:

```bash
pip install -r requirements.txt
```

Create the .env and update the SECRET_KEY in the newly created .env file like in .envexample


Then you can run the app locally:

```bash
python main.py
```

## Usage

You can create new account, login, solve the quiz which has randomized questions. You can also check the leaderboard. Visit your profile and see the stats or search for a friend profile.


There also data_insert.py script which you can use to insert new questions into the quiz and delete_questions.py to delete all the questions.

## Features

- Friendly user interface

- Login, register functions

- Database

- Quizes with randomized questions.

- Leaderboard

- Search friend system

![showcase](https://github.com/juhum/QuizApp/blob/master/showcase.gif)
