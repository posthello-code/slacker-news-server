# Slacker News Server

Backend for a news aggregator and summarizer

Current features:

- Hosted on render.com for simplicity sake
- Render.com cron job calls `cron/stories.py` once per hour
- Rewrites articles via with OpenAI gpt-3-turbo and saves them to a postgres database
- A restful server can be run from `start.py` to serve stories out of the database

Will be adding a front-end to go along with the project soon.

# Getting Started

Install with `install.sh`

If you add new dependencies freeze them by running `freeze.sh`

Run all python files as modules since they use relative imports i.e. `python -m cron.stories`.

To run production server use `gunicorn start:app`
