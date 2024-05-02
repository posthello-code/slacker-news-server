# Slacker News Server

Backend for a news aggregator and summarizer

Current features:

- Hosted on render.com for simplicity sake
- Render.com cron job calls `cron.stories.py` once per hour
- Summarizes them via with OpenAI gpt-3-turbo and saves them to a postgres database
- A restful server can be run from `start.py` to serve stories out of the database

Will be adding a front-end to go along with the project soon.

# Getting Started

Install with `install.sh`

If you add new dependencies freeze them by running `freeze.sh`

Cron tasks are in the cron folder that will be called by render cron jobs (see render.yaml).
They require to be run as a module to use relative imports. Run them with `python -m cron.{filename}`.

There's a flask server here too but that's a work in progress.
