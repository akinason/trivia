## Backend Guidelines and API Reference

The `backend` directory contains a fully functional API Flask application powered with SQLAlchemy ORM. In order to spin
it up successfully, you will need to:

1. Create and Initialize the database
2. Create a virtual environment `venv` folder and install python `requirements`
3. Configure your `.env` file
4. Export `FLASK_APP` so it's available in your virtual environment and run the flask app
5. Run tests

### 1. Create and Initialize database

With postgres running, create a `trivia` database

```angular2html
createdb trivia
```

Populate the database using `trivia.sql` file provided. In the `backend` folder, run

```angular2html
psql trivia < trivia.sql
```

### 2. Create virtual environment

Follow python3.7 or latest version to install python in your machine, then run the following command to create a
virtualenv while in your backend folder

```angular2html
python -m venv venv 
```

Activate virtualenv and install dependencies

```angular2html
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Configure your .env configuration file

You will find `.env.template` in your `backend` folder. Make a copy of the file and rename it to `.env` then open and
fill up the missing configurations with your specific values. Some are already prefilled and should be good enough to
get you started.

### 4. Run flask app

While in your backend folder, run the following commands on your terminal

```angular2html
export FLASK_APP=flaskr
export FLASK_DEBUG=True

flask run
```

You should now see the app running at `http:\\127.0.0.1:5000`

**NB**: If you encounter any error, please search the web.

> View the [Frontend README](../frontend/README.md) for details on how to run the frontend app

### 5. Running Tests
To run tests, while in your backend directory, type:
> pytest test_flaskr.py

## API Reference

### Getting Started

- **Base URL**: The current app is hosted locally at the default flask url `http://127.0.0.1:5000/`
- **Authentication**: This version does not require any authentication.

### Response Format

The response format is standardized and is the same for both `successful` and `failed` requests.

```json
{
  "success": true,
  "data": {},
  "status_code": 200,
  "message": ""
}
```

- **success: _bool_** : `true` if the request was successful and `false` otherwise.
- **data: _Any_** : Either `int`, `string`, `list`, `dict` depending on the endpoint. This contains the requested data.
- **status_code: _int_** : The status code of the request. Can be one of `200, 201, 204, 400, 404, 422, 500`
- **message: _string_** : The error message returned when an error response is sent.

**Status Codes**

* 2xx: Successful
* 400: Bad request
* 404: Resource Not Found
* 422: Not Processable

**Sample Failed Response**

```json
{
  "data": {},
  "message": "The resource you are looking for does not exist.",
  "status_code": 404,
  "success": false
}
```

### Endpoints

#### GET /categories

- General
    - Returns a list of question categories
- Sample: `curl http://127.0.0.1:5000/categories`

```json
{
  "data": [
    {
      "id": 2,
      "type": "Art"
    },
    {
      "id": 5,
      "type": "Entertainment"
    },
    {
      "id": 3,
      "type": "Geography"
    },
    {
      "id": 4,
      "type": "History"
    },
    {
      "id": 1,
      "type": "Science"
    },
    {
      "id": 6,
      "type": "Sports"
    }
  ],
  "message": "",
  "status_code": 200,
  "success": true
}
```

#### GET /categories/{category_id}/questions

- General
    - Returns a paginated list of questions belonging to the specified category.
    - Returns `404 - Not Found` if the category_id is invalid or if `page` is has no results.
    - `total_questions` is the total number of questions in the database and not the total number of questions in the
      category.
- Sample `curl http://127.0.0.1:5000/categories/1/questions?page=1`

```json
{
  "data": {
    "categories": [
      {
        "id": 1,
        "type": "Science"
      },
      {
        "id": 2,
        "type": "Art"
      },
      {
        "id": 3,
        "type": "Geography"
      },
      {
        "id": 4,
        "type": "History"
      },
      {
        "id": 5,
        "type": "Entertainment"
      },
      {
        "id": 6,
        "type": "Sports"
      }
    ],
    "current_category": {
      "id": 1,
      "type": "Science"
    },
    "questions": [
      {
        "answer": "The Liver",
        "category": "Science",
        "difficulty": 4,
        "id": 20,
        "question": "What is the heaviest organ in the human body?"
      },
      {
        "answer": "Alexander Fleming",
        "category": "Science",
        "difficulty": 3,
        "id": 21,
        "question": "Who discovered penicillin?"
      },
      {
        "answer": "Blood",
        "category": "Science",
        "difficulty": 4,
        "id": 22,
        "question": "Hematology is a branch of medicine involving the study of what?"
      }
    ],
    "total_questions": 19
  },
  "message": "",
  "status_code": 200,
  "success": true
}
```

#### GET /questions

- General
    - Returns the list of paginated questions. The maximum number of questions per page is 10.
- Sample: `curl http://127.0.0.1:5000/questions?page=2`

```json
{
  "data": {
    "categories": [
      {
        "id": 1,
        "type": "Science"
      },
      {
        "id": 2,
        "type": "Art"
      },
      {
        "id": 3,
        "type": "Geography"
      },
      {
        "id": 4,
        "type": "History"
      },
      {
        "id": 5,
        "type": "Entertainment"
      },
      {
        "id": 6,
        "type": "Sports"
      }
    ],
    "current_category": "",
    "questions": [
      {
        "answer": "Escher",
        "category": "Art",
        "difficulty": 1,
        "id": 16,
        "question": "Which Dutch graphic artist–initials M C was a creator of optical illusions?"
      },
      {
        "answer": "Mona Lisa",
        "category": "Art",
        "difficulty": 3,
        "id": 17,
        "question": "La Giaconda is better known as what?"
      },
      {
        "answer": "One",
        "category": "Art",
        "difficulty": 4,
        "id": 18,
        "question": "How many paintings did Van Gogh sell in his lifetime?"
      },
      {
        "answer": "Jackson Pollock",
        "category": "Art",
        "difficulty": 2,
        "id": 19,
        "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
      },
      {
        "answer": "The Liver",
        "category": "Science",
        "difficulty": 4,
        "id": 20,
        "question": "What is the heaviest organ in the human body?"
      },
      {
        "answer": "Alexander Fleming",
        "category": "Science",
        "difficulty": 3,
        "id": 21,
        "question": "Who discovered penicillin?"
      },
      {
        "answer": "Blood",
        "category": "Science",
        "difficulty": 4,
        "id": 22,
        "question": "Hematology is a branch of medicine involving the study of what?"
      },
      {
        "answer": "Scarab",
        "category": "History",
        "difficulty": 4,
        "id": 23,
        "question": "Which dung beetle was worshipped by the ancient Egyptians?"
      },
      {
        "answer": "Samuel Etoo",
        "category": "Sports",
        "difficulty": 2,
        "id": 24,
        "question": "Who is the best footballer in Cameroon?"
      }
    ],
    "total_questions": 19
  },
  "message": "",
  "status_code": 200,
  "success": true
}
```

#### DELETE /question/{question_id}

- General
    - Deletes the question with specified id from the database.
    - Returns `status_code=204` when the delete operation is successful.
    - Returns `404 - Not Found` if the question_id is invalid.
    - This endpoint will not return any data when successful, you should watch out for the `status_code 204`
- Sample: `curl -X DELETE http://127.0.0.1:5000/questions/3`

#### POST /questions

- General
    - Creates a new question.
    - Returns status_code 400 if request data is not properly formatted and 201 if successful.

**Request data:**

```json
{
  "question": string,
  "answer": string,
  "category_id": int,
  "difficulty": int
}
```

- Sample request - response

```json
// Request data
{
  "question": "In what age did Micheal Jackson die?",
  "answer": "50",
  "category_id": 5,
  "difficulty": 2
}


// Response
{
  "data": {
    "answer": "50",
    "category": "Entertainment",
    "difficulty": 2,
    "id": 25,
    "question": "In what age did Micheal Jackson die?"
  },
  "message": "",
  "status_code": 201,
  "success": true
}
```

#### POST /questions/search

- General
    - Returns a paginated list of questions based on search_term.
    - `total_questions` refers to the total number of questions in the database.
    - Returns `status_code 404` if no match is found and `status_code 200` if successful.
-

Sample: `curl -X POST http://127.0.0.1:5000/questions/search -H "Content-Type: application/json" -d '{"search_term": "box"}'`

```json
{
  "data": {
    "categories": [
      {
        "id": 1,
        "type": "Science"
      },
      {
        "id": 2,
        "type": "Art"
      },
      {
        "id": 3,
        "type": "Geography"
      },
      {
        "id": 4,
        "type": "History"
      },
      {
        "id": 5,
        "type": "Entertainment"
      },
      {
        "id": 6,
        "type": "Sports"
      }
    ],
    "current_category": "",
    "questions": [
      {
        "answer": "Muhammad Ali",
        "category": "History",
        "difficulty": 1,
        "id": 9,
        "question": "What boxer's original name is Cassius Clay?"
      }
    ],
    "total_questions": 19
  },
  "message": "",
  "status_code": 200,
  "success": true
}
```

#### POST /quizzes

- General
    - In the `Play` tab in the frontend, when a user selects `All` or a category, one question at a time is displayed.
      The
      next question is random within the selected category but a question never repeats.
    - Returns `status_code 200` on success and `404 - Not Found` if category is not found or if there are no more
      questions in the selected category.

- Sample: curl -X POST http://127.0.0.1:5000/quizzes -H "Content-Type: application/json" -d '{"quiz_category" : {"id":  1, "type": "Science"},"previous_questions": [20, 22]}'

```json
// Request body
{
  "quiz_category" : {"id":  1, "type": "Science"},
  "previous_questions": [20, 22]
}

// Response
{
    "data": {
        "answer": "Alexander Fleming",
        "category": "Science",
        "difficulty": 3,
        "id": 21,
        "question": "Who discovered penicillin?"
    },
    "message": "",
    "status_code": 200,
    "success": true
}
```

## Acknowledgments
I would like to acknowledge the following open source resources/libraries used in this project:
- [Github](https://github.com)
- [Flask](https://flask.palletsprojects.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- and more found in [requirements.txt](./requirements.txt)

## License
MIT License