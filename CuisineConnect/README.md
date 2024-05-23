# CuisineConnect

CuisineConnect is a web application that allows users to share, browse, and discover recipes from around the world. The backend is built with Flask, while the frontend is powered by React.

## Installation

### Prerequisites

* Python 3.10+.
* Node.js and npm.
* MySQL database.

## Backend Setup

1. **Clone the repository:**

    * HTTPS:

        ```git clone https://github.com/Damicable/Portfolio_project.git```

    * SSH:

        `git clone git@github.com:Damicable/Portfolio_project.git`

2. **Set up a virtual enviroment and activate:**
        `python3 -m venv venv`
        `source venv/bin/activate`

3. **Install backend dependencies:**
        `pip install -r requirements.txt`

4. **Run the backend server:**
        `flask run`
        or
        `python3 run.py`

## API Endpoints

### Authentication

* Register a new user

  * Endpoint: `POST /auth/register`
  * Description: Allows a new user to register by providing a username, email, and password.

* Log in a user

  * Endpoint: `POST /auth/login`
  * Description: Allows a registered user to log in by providing their username and password.

* Log out a user

  * Endpoint: `POST /auth/logout`
  * Description: Allows a logged-in user to log out.

### Recipe

* Create a new recipe

  * Endpoint: `POST /recipes`
  * Description: Allows a logged-in user to create a new recipe.

* Update an existing recipe

  * Endpoint: `PUT /recipes/{id}`
  * Description: Allows a logged-in user to update their own recipe.

* Delete an existing recipe

  * Endpoint: `DELETE /recipes/{id}`
  * Description: Allows a logged-in user to delete their own recipe.

* Retrieve details of a specific recipe

  * Endpoint: `GET /recipes/{id}`
  * Description: Retrieve the details of a specific recipe by its ID.

* Retrieve details of all recipes

  * Endpoint: `GET /recipes`
  * Description: Retrieve the details of all recipes.

### Like

* Like a recipe

  * Endpoint: `POST /recipes/{recipe_id}/like`
  * Description: Allows a logged-in user to like a specific recipe.

* Unlike a recipe

  * Endpoint: `DELETE /recipes/{recipe_id}/unlike`
  * Description: Allows a logged-in user to unlike a specific recipe.

### Comment

* Add a comment to a recipe

  * Endpoint: `POST /recipes/{recipe_id}/comments`
  * Description: Allows a logged-in user to add a comment to a specific recipe.

* Retrieve all comments for a recipe

  * Endpoint: `GET /recipes/{recipe_id}/comments`
  * Description: Retrieve all comments for a specific recipe.
