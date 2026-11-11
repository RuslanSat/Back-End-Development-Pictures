# Back-End-Development-Pictures

Flask REST microservice for the IBM Back-end Application Development Capstone.
Developed by Ruslan Satvaldiev with AI assistance from the official IBM Skills Network template.

## Requirements and setup

Python 3.10 or newer (the original template used Python 3.9), pip, and venv.
This service uses the supplied JSON picture collection in memory and requires no database.

```sh
bash bin/setup.sh
source .venv/bin/activate
python -m pytest -v
python app.py
```

The development server listens on port 8080. The supplied container listens on port 3000.

## REST API

| Method | Path | Purpose |
| --- | --- | --- |
| GET | /health | Health status |
| GET | /count | Number of pictures |
| GET | /picture | List pictures |
| GET | /picture/<id> | Read one picture |
| POST | /picture | Create a picture |
| PUT | /picture/<id> | Update a picture |
| DELETE | /picture/<id> | Delete a picture |

A picture has integer `id` and the fields `pic_url`, `event_country`, `event_state`,
`event_city`, and `event_date`. Unknown IDs return 404. Invalid create data returns 400.
For compatibility with the course tests, duplicate IDs return 302. Deletion returns 204.

All 11 unmodified template tests passed in an isolated local Python 3.12 environment.
Records are held in memory; restarting restores the supplied JSON data.
