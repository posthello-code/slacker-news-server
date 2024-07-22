# Slacker News Server

Backend for a news aggregator and summarizer

Current features:

- Hosted on render.com for simplicity sake
- Render.com cron job calls `cron/stories.py` and `cron/comments.py` a few times a day (these run a single cron and too frequently in order to keep costs down for OpenAI usage)
- Summarizes articles using with OpenAI chat completions and saves them to a postgres database
- Flask server runs from `start.py` to serve stories out of the database

Front-end [here](https://slacker-news-frontend.onrender.com/)
Front-end repo [here](https://github.com/posthello-code/slacker-news-frontend)

# Getting Started

Install with `install.sh`

If you add new dependencies freeze them by running `freeze.sh`

Run all python files as modules since they use relative imports i.e. `python -m cron.stories`.

To run production server use `gunicorn start:app`
