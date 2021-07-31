# Backend - Full Stack Trivia API

### Installing Dependencies for the Backend

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)


2. **Virtual Enviornment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)


3. **PIP Dependencies** - Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:
```bash
pip install -r requirements.txt
```
This will install all of the required packages we selected within the `requirements.txt` file.


4. **Key Dependencies**
 - [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

 - [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py.

 - [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server.

### Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

### Running the server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## ToDo Tasks
These are the files you'd want to edit in the backend:

1. *./backend/flaskr/`__init__.py`*
2. *./backend/test_flaskr.py*


One note before you delve into your tasks: for each endpoint, you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior.

1. Use Flask-CORS to enable cross-domain requests and set response headers.


2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories.


3. Create an endpoint to handle GET requests for all available categories.


4. Create an endpoint to DELETE question using a question ID.


5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score.


6. Create a POST endpoint to get questions based on category.


7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question.


8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions.


9. Create error handlers for all expected errors including 400, 404, 422 and 500.



## Review Comment to the Students
```
This README is missing documentation of your endpoints. Below is an example for your endpoint to get all categories. Please use it as a reference for creating your documentation and resubmit your code.

Endpoints
GET '/api/v1.0/categories'
GET ...
POST ...
DELETE ...

GET '/api/v1.0/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs.
{'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"}

```

## Endpoints

- GET `/questions`
- GET `/categories`
- GET `/categories/<category_id>/questions`
- DELETE `/questions/<question_id>`
- POST `/questions`
- POST `/quizzes`

---

### GET /questions  
Get a paged list of all questions

#### Endpoint URL
`GET http://localhost:5000/questions`

#### Parameters

| Name      | Type | Description |
| ----------- | ----------- | ----------- |
| page      | int       | Page number to return (up to 10 questions per page)      |

#### Request arguments
An example of the request structure.
```
?page=2
```

#### Request body
n/a

#### Response
Returns: An object with keys:  
- **"categories"** contains an object of `category_id`: `category<string>` *key:value* pairs
- **"current_category"** contains `category_id<int>`
- **"questions"** a list that contains objects
  -  containing `answer`:`answer<string>`, `category`: `category_id<int>`,  `difficulty`: `difficulty_level<int>`, `id`:`question_id<int>`, `question`:`question<string>` *key:value* pairs
- **"success"** contains the boolean value `true`
- **"total_questions"** contain an integer value

This is an example of the response JSON. Results will vary depending on your data.

```
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "current_category": 1,
  "questions": [
    {
      "answer": "Agra",
      "category": 3,
      "difficulty": 2,
      "id": 15,
      "question": "The Taj Mahal is located in which Indian city?"
    },
    {
      "answer": "Escher",
      "category": 2,
      "difficulty": 1,
      "id": 16,
      "question": "Which Dutch graphic artist – initials M C was a creator of optical illusions?"
    }
  ],
  "success": true,
  "total_questions": 18
}
```

---

### GET /categories  
Get a list of all categories

#### Endpoint URL
`GET http://localhost:5000/categories`

#### Parameters
n/a

#### Request arguments
n/a

#### Request body
n/a

#### Response
Returns: An object with keys:  
- **"categories"** contains an object of `category_id`: `category<string>` *key:value* pairs
- **"success"** contains the boolean value `true`

This is an example of the response JSON. Results will vary depending on your data.

```
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "success": true
}
```
---

### GET /categories/<category_id>/questions
Get a paged list of questions filtered by category

#### Endpoint URL
`GET http://localhost:5000/categories/<category_id>/questions`

#### Parameters
n/a

#### Request arguments
n/a

#### Request body
n/a

#### Response
Returns: An object with keys:
- **"current_category"** contains `category_id<int>`
- **"questions"** a list that contains objects
  -  containing `answer`:`answer<string>`, `category`: `category_id<int>`,  `difficulty`: `difficulty_level<int>`, `id`:`question_id<int>`, `question`:`question<string>` *key:value* pairs
- **"success"** contains the boolean value `true`
- **"total_questions"** contain an integer value

This is an example of the response JSON. Results will vary depending on your data.
```
{
  "current_category": 1,
  "questions": [
    {
      "answer": "The Liver",
      "category": 1,
      "difficulty": 4,
      "id": 20,
      "question": "What is the heaviest organ in the human body?"
    },
    {
      "answer": "Alexander Fleming",
      "category": 1,
      "difficulty": 3,
      "id": 21,
      "question": "Who discovered penicillin?"
    },
    {
      "answer": "Blood",
      "category": 1,
      "difficulty": 4,
      "id": 22,
      "question": "Hematology is a branch of medicine involving the study of what?"
    }
  ],
  "success": true,
  "total_questions": 3
}
```

---

### DELETE /questions/<question_id>
Delete a question by id

#### Endpoint URL
`GET http://localhost:5000/questions/<question_id>`

#### Parameters
n/a

#### Request arguments
n/a

#### Request body
n/a

#### Response
Returns: An object with keys:
- **"success"** contains the boolean value `true`
- **"deleted"** contains the `question_id<int>` deleted

This is an example of the response JSON. Results will vary depending on your data.

```
{
  "success": true,
  "deleted": 3
}
```

---

### POST /questions  
Add a new question

#### Endpoint URL
`POST http://localhost:5000/questions`

#### Parameters
n/a

#### Request arguments
n/a

#### Request body
An example of the request structure.
```
{
  "question": "What is 1+1?",
  "answer": "2!",
  "difficulty": 1,
  "category": 1
}
```

#### Response

Returns: An object with keys:
- **"success"** contains the boolean value `true`
- **"created"** contains the `question_id<int>` created
- **"total_questions"** contain an integer value

This is an example of the response JSON. Results will vary depending on your data.

```
{
  "success": true,
  "created": 19
  "total_questions": 18
}
```

---

### POST /questions  
Get questions based on a search term. It will return any questions for whom the search term is a substring of the question.

#### Endpoint URL
`POST http://localhost:5000/questions`

#### Parameters
n/a

#### Request arguments
n/a

#### Request body
```
{
  "searchTerm": "title"
}
```

#### Response
Returns: An object with keys:
- **"current_category"** contains `category_id<int>`
- **"questions"** a list that contains objects
  -  containing `answer`:`answer<string>`, `category`: `category_id<int>`,  `difficulty`: `difficulty_level<int>`, `id`:`question_id<int>`, `question`:`question<string>` *key:value* pairs
- **"success"** contains the boolean value `true`
- **"total_questions"** contain an integer value

This is an example of the response JSON. Results will vary depending on your data.

```
{
  "current_category": 1,
  "questions": [
      {
          "answer": "Maya Angelou",
          "category": 4,
          "difficulty": 2,
          "id": 5,
          "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
      },
      {
          "answer": "Edward Scissorhands",
          "category": 5,
          "difficulty": 3,
          "id": 6,
          "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
      }
    ],
    "success": true,
    "total_questions": 2
}
```

---

### POST /quizzes  
Get questions to play the quiz. Returns a random questions within the given category, if provided, and that is not one of the previous questions answered.

#### Endpoint URL
`POST http://localhost:5000/quizzes`

#### Parameters
n/a

#### Request body
n/a

#### Request body
An example of the request structure.
```
{
  "previous_questions": [15, 16],
  "quiz_category": {
    "type": "Science",
    "id": "1"
  }
}
```

#### Response
Returns: An object with keys:
- **"question"** an object containing `answer`:`answer<string>`, `category`: `category_id<int>`,  `difficulty`: `difficulty_level<int>`, `id`:`question_id<int>`, `question`:`question<string>` *key:value* pairs
- **"success"** contains the boolean value `true`

This is an example of the response JSON. Results will vary depending on your data.

```
{
  "question": {
      "answer": "Blood", 
      "category": 1,
      "difficulty": 4,
      "id": 22,
      "question": "Hematology is a branch of medicine involving the study of what?"
  }
  "success": true
}
```

## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
