# Full Stack Trivia API Backend

## Introduction

The trivia API allows users to test their knowledge by answering randomized questions in a specific category or all categories. It displays a list of questions and categories, organizes questions by their category, allows users to add new questions, and view a question and the answer. The API is resource-oriented and organized around REST, it accepts input from the request body and request parameters, returns JSON-encoded responses, and uses standard HTTP response codes.

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```

## Error Handling
The API returns JSON-encoded responses for three types of errors:
1. 400 - Bad Request.
2. 404 - Resource not found.
3. 422 - Unprocessable entity.

The error response is formatted in the following way:
```
{
 'success': False,
 'error': 422,
 'message': 'Unprocessable entity.'
}
```
## API Endpoints
Base URL: http://127.0.0.1:5000, the app can only be run locally.
Authenticaton: Does not require authentication.
##### GET '/categories'
- General:
    - Lists all categories with their ID and type.
- Request Body: None.
- Request Parameters: None.
- Example: `curl http://127.0.0.1:5000/categories`
```
{
  "categories": [
    {
      "id": 1,
      "type": "Music"
    },
    {
      "id": 2,
      "type": "Science"
    },
    {
      "id": 3,
      "type": "Computer"
    },
    {
      "id": 4,
      "type": "Movies"
    },
    {
      "id": 5,
      "type": "Books"
    }
  ],
  "success": true
}
```
##### GET '/categories/<int:category_id>/questions'
- General:
    - Returns the current category type.
    - Lists all questions in a category.
    - Questions are paginated (10 questions per page).
    - Returns the total number of questions.
- Request Body: None.
- Request Parameters: None.
- Example: `curl http://127.0.0.1:5000/categories/1/questions`
```
{
  "current_category": "Music",
  "questions": [
    {
      "answer": "The Liver",
      "category": "1",
      "difficulty": 4,
      "id": 20,
      "question": "What is the heaviest organ in the human body?"
    },
    {
      "answer": "Alexander Fleming",
      "category": "1",
      "difficulty": 3,
      "id": 21,
      "question": "Who discovered penicillin?"
    },
    {
      "answer": "Blood",
      "category": "1",
      "difficulty": 4,
      "id": 22,
      "question": "Hematology is a branch of medicine involving the study of what?"
    }
  ],
  "success": true,
  "total_questions": 19
}
```
##### GET '/questions'
- General:
    - Lists all categories with their ID and type.
    - Lists all questions with their ID, question text, answer text, category ID, and difficulty rating.
    - Questions are paginated (10 questions per page).
    - Returns the total number of questions.
- Request Body: None.
- Request Parameters: Page, it is set to 1 by default.
- Example: `curl http://127.0.0.1:5000/questions?page=1`
```
{
  "categories": [
    {
      "id": 1,
      "type": "Music"
    },
    {
      "id": 2,
      "type": "Science"
    },
    {
      "id": 3,
      "type": "Computer"
    },
    {
      "id": 4,
      "type": "Movies"
    },
    {
      "id": 5,
      "type": "Books"
    }
  ],
  "questions": [
    {
      "answer": "Maya Angelou",
      "category": "4",
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    {
      "answer": "Muhammad Ali",
      "category": "4",
      "difficulty": 1,
      "id": 9,
      "question": "What boxer's original name is Cassius Clay?"
    },
    {
      "answer": "Apollo 13",
      "category": "5",
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
    {
      "answer": "Tom Cruise",
      "category": "5",
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": "5",
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    },
    {
      "answer": "Brazil",
      "category": "6",
      "difficulty": 3,
      "id": 10,
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    },
    {
      "answer": "Uruguay",
      "category": "6",
      "difficulty": 4,
      "id": 11,
      "question": "Which country won the first ever soccer World Cup in 1930?"
    },
    {
      "answer": "George Washington Carver",
      "category": "4",
      "difficulty": 2,
      "id": 12,
      "question": "Who invented Peanut Butter?"
    },
    {
      "answer": "Lake Victoria",
      "category": "3",
      "difficulty": 2,
      "id": 13,
      "question": "What is the largest lake in Africa?"
    },
    {
      "answer": "The Palace of Versailles",
      "category": "3",
      "difficulty": 3,
      "id": 14,
      "question": "In which royal palace would you find the Hall of Mirrors?"
    }
  ],
  "success": true,
  "total_questions": 19
}
```
##### POST '/questions'
- General:
    - Adds a new question to the database.
    - Returns the newly created question's information.
    - Lists all questions with their ID, question text, answer text, category ID, and difficulty rating.
    - Questions are paginated (10 questions per page).
    - Returns the total number of questions.
- Request Body:
    - Question (String) - The question itself.
    - Answer (String) - The question's answer.
    - Difficulty (Integer) - The question's difficulty rating.
    - Category (String) - The category ID that the question belongs to.
- Request Parameters: None.
- Example: `curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"question":"test", "answer":"test", "difficulty":"4", "category":"1"}'`
```
{
  "created_question": {
    "answer": "test",
    "category": "1",
    "difficulty": 4,
    "id": 24,
    "question": "test"
  },
  "questions": [
    {
      "answer": "Apollo 13",
      "category": "5",
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
    {
      "answer": "Tom Cruise",
      "category": "5",
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
    {
      "answer": "Maya Angelou",
      "category": "4",
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": "5",
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    },
    {
      "answer": "Muhammad Ali",
      "category": "4",
      "difficulty": 1,
      "id": 9,
      "question": "What boxer's original name is Cassius Clay?"
    },
    {
      "answer": "Brazil",
      "category": "6",
      "difficulty": 3,
      "id": 10,
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    },
    {
      "answer": "Uruguay",
      "category": "6",
      "difficulty": 4,
      "id": 11,
      "question": "Which country won the first ever soccer World Cup in 1930?"
    },
    {
      "answer": "George Washington Carver",
      "category": "4",
      "difficulty": 2,
      "id": 12,
      "question": "Who invented Peanut Butter?"
    },
    {
      "answer": "Lake Victoria",
      "category": "3",
      "difficulty": 2,
      "id": 13,
      "question": "What is the largest lake in Africa?"
    },
    {
      "answer": "The Palace of Versailles",
      "category": "3",
      "difficulty": 3,
      "id": 14,
      "question": "In which royal palace would you find the Hall of Mirrors?"
    }
  ],
  "success": true,
  "total_num_of_questions": 20
}
```
##### DELETE '/questions/<int:question_id>'
- General:
    - Deletes a question from the database.
    - Returns the deleted question's information.
    - Lists all questions with their ID, question text, answer text, category ID, and difficulty rating.
    - Questions are paginated (10 questions per page).
    - Returns the total number of questions.
- Request Body: None.
- Request Parameters: None.
- Example: `curl http://127.0.0.1:5000/questions/6`
```
{
  "deleted_question": {
    "answer": "Edward Scissorhands",
    "category": "5",
    "difficulty": 3,
    "id": 6,
    "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
  },
  "questions": [
    {
      "answer": "Apollo 13",
      "category": "5",
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
    {
      "answer": "Tom Cruise",
      "category": "5",
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
    {
      "answer": "Maya Angelou",
      "category": "4",
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    {
      "answer": "Muhammad Ali",
      "category": "4",
      "difficulty": 1,
      "id": 9,
      "question": "What boxer's original name is Cassius Clay?"
    },
    {
      "answer": "Brazil",
      "category": "6",
      "difficulty": 3,
      "id": 10,
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    },
    {
      "answer": "Uruguay",
      "category": "6",
      "difficulty": 4,
      "id": 11,
      "question": "Which country won the first ever soccer World Cup in 1930?"
    },
    {
      "answer": "George Washington Carver",
      "category": "4",
      "difficulty": 2,
      "id": 12,
      "question": "Who invented Peanut Butter?"
    },
    {
      "answer": "Lake Victoria",
      "category": "3",
      "difficulty": 2,
      "id": 13,
      "question": "What is the largest lake in Africa?"
    },
    {
      "answer": "The Palace of Versailles",
      "category": "3",
      "difficulty": 3,
      "id": 14,
      "question": "In which royal palace would you find the Hall of Mirrors?"
    },
    {
      "answer": "Agra",
      "category": "3",
      "difficulty": 2,
      "id": 15,
      "question": "The Taj Mahal is located in which Indian city?"
    }
  ],
  "success": true,
  "total_num_of_questions": 19
}
```
##### PATCH '/questions/<int:question_id>'
- General:
    - Updates a question's category ID.
    - Returns the updated question's ID.
- Request Body:
    - Category (String) - The category ID that is to be updated.
- Request Parameters: None.
- Example: `curl http://127.0.0.1:5000/questions/10 -X PATCH -H "Content-Type: application/json" -d '{"category":"2"}'`
```
{
  "question_id": 10,
  "success": true
}
```
##### POST '/questions'
- General:
    - Searches the database for questions that includes a search term.
    - Returns the search result as a list of questions.
    - Returns the total number of questions.
- Request Body:
    - Search Term (String) - The text that is to be used to search the database.
- Request Parameters: None.
- Example: `curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"search_term":"world"}'`
```
{
  "questions": [
    {
      "answer": "Uruguay",
      "category": "6",
      "difficulty": 4,
      "id": 11,
      "question": "Which country won the first ever soccer World Cup in 1930?"
    },
    {
      "answer": "Brazil",
      "category": "2",
      "difficulty": 3,
      "id": 10,
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    }
  ],
  "success": true,
  "total_questions": 19
}
```
##### POST '/trivia'
- General:
    - Retrieves a random question from the database by category.
    - Returns the random question's ID, question text, answer text, category ID, and difficulty rating.
- Request Body:
    - Category (Integer) - The category's ID that is to be used for the trivia game.
    - Previous Questions (Integer) - A list of previously displayed questions.
- Request Parameters: None.
- Example: `curl http://127.0.0.1:5000/trivia -X POST -H "Content-Type: application/json" -d '{"category": 0, "previous_questions": [1, 2, 3, 4]}'`
```
{
  "question": {
    "answer": "Brazil",
    "category": "2",
    "difficulty": 3,
    "id": 10,
    "question": "Which is the only team to play in every soccer World Cup tournament?"
  },
  "success": true
}
```