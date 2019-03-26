# Questioner

by The dojos

[![Build Status](https://travis-ci.com/kbjude/questioner.svg?branch=develop)](https://travis-ci.com/kbjude/questioner)
[![Coverage Status](https://coveralls.io/repos/github/kbjude/questioner/badge.svg?branch=develop)](https://coveralls.io/github/kbjude/questioner?branch=develop)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/5733e79fce2049e8bb43bc0558a5b910)](https://www.codacy.com/app/kalsmic/questioner?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=kbjude/questioner&amp;utm_campaign=Badge_Grade)

## Introduction

Questioner is ...

## Installation

    - Clone this repository.

    - Setup a virtual environment and activate it.

    - Install the requirements.txt

    - Add a ".env" file that has:

        - export DJANGO_SETTINGS_MODULE="questioner.settings"

        - export DATABASE_NAME

        - export DATABASE_HOST

        - export DATABASE_USER

        - export DATABASE_PASSWORD

## Running the application

Open the directory of the application in the terminal and execute:

    python manage.py migrate
    python manage.py runserver

In a browser type the Url: http//localhost:8000.

## Login

Using postman login with endpoint: http//localhost:8000/auth/login
Provide your credentials under the body tab
{
"username": "your-username",
"password": "your-password"
}

## Endpoints

| Method        | Endpoint                          | Description                     |
|:--------------|:----------------------------------|:--------------------------------|
| **User**      |                                   |                                 |
| GET           | /                                 | Index                           |
| POST          | /accounts/login                   | login                           |
| POST          | /accounts/signup                  | signup                          |
| **Meetups**   |                                   |                                 |
| POST          | /meetups                          | Add a meetup                    |
| GET           | /meetups                          | Get all meetups                 |
| GET           | /meetups/2                        | Get meetup 2                    |
| PUT           | /meetups/2                        | Update meetup 2                 |
| DELETE        | /meetups/2                        | Delete meetup 2                 |
| **Tags**      |                                   |                                 |
| POST          | /tags                             | create a tag                    |
| GET           | /tags                             | Get all tags                    |
| DELETE        | /tags/2                           | Delete tag 2                    |
| POST          | /meetups/tags                     | Add tag 2 to meetup 2           |
| DELETE        | /meetups/2/tags/2                 | remove tag 2 from meetup 2      |
| **Questions** |                                   |                                 |
| POST          | meetups/2/questions/              | Add a question                  |
| GET           | meetups/2/questions/              | Get all questions               |
| GET           | meetups/2/questions/12            | Get question 12                 |
| PUT           | meetups/2/questions/12            | Update question 12              |
| DELETE        | meetups/2/questions/12            | Delete question 12              |
| **Votes**     |                                   |                                 |
| POST          | meetups/2/questions/12/upvote     | Upvote question 12              |
| POST          | meetups/2/questions/12/downvote   | Downvote question 12            |
| POST          | meetups/2/questions/12/answers/   | Post an answer                  |
| GET           | meetups/2/questions/12/answers/   | GET answers to a question       |
| PUT           | meetups/2/questions/12/answers/1/ | EDIT an answers to a question   |
| DELETE        | meetups/2/questions/12/answers/1/ | DELETE an answers to a question |
