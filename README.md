![](https://img.shields.io/pypi/pyversions/flask.svg?logo=python&style=for-the-badge)



[![Build Status](https://travis-ci.org/Tevinthuku/Stackoverflow-lite.svg?branch=master)](https://travis-ci.org/Tevinthuku/Stackoverflow-lite)

[![Coverage Status](https://coveralls.io/repos/github/Tevinthuku/Stackoverflow-lite/badge.svg?branch=master)](https://coveralls.io/github/Tevinthuku/Stackoverflow-lite?branch=master)


[![Maintainability](https://api.codeclimate.com/v1/badges/bfa3d2f3aa7f539c2f22/maintainability)](https://codeclimate.com/github/Tevinthuku/Stackoverflow-lite/maintainability)



### Stackoverflow-lite

This app is a small mimicking version of Stackoverflow where users can create accounts, log in, post questions, answer available questions, upvote questions

#### Installation & Set up

1. Set up virtualenv

   ```bash
        virtualenv venv
   ```

2. Activate virtualenv

   ```bash
        source venv/bin/activate
   ```

3. Install dependencies

   ```bash
        pip install -r requirements.txt
   ```

4. Run the app

```bash
        python run.py
```

# Pivotal Tracker tasks

> **[Pivotal Tracker Board Stories](https://www.pivotaltracker.com/n/projects/2240990)**


## Stackoverflow-endpoints API Endpoints

| Method   | Endpoint                                           | Description                                     |
| -------- | -------------------------------------------------- | ----------------------------------------------- |
| `GET`    | `/api/v1/questions`                                | View All questions created in the app           |
| `POST`   | `/api/v1/questions`                                | Post a question                                 |
| `GET`    | `/api/v1/questions/<int:questionId>`               | Fetch a specific question                       |
| `POST`   | `/api/v1/auth/signup`                              | Register a user                                 |
| `POST`   | `/api/v1/auth/login`                               | Login a user                                    |
| `POST`   | `api/v1/questions/<int:questionId>/answers`        | Post an answer to a question                    |
| `DELETE` | `api/v1/questions/<int: questionId>`               | Deletes a question                              |
| `PUT`    | `api/v1/questions/<questionId>/answers/<answerId>` | Mark an answer as accepted or update an answer. |


### Author: TevinThuku

### Credits: Andela
