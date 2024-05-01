# Getting Started

Install with `install.sh`

If you add new dependencies freeze them by running `freeze.sh`

Cron tasks are in the cron folder that will be called by render cron jobs (see render.yaml).
They require to be run as a module to use relative imports. Run them with `python -m cron.{filename}`.

There's a flask server here too but that's a work in progress.

# Explanation

This server is going to eventually be the backend for a site that gets tech news around the web and summarizes it.
