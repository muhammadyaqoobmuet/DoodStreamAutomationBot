# Deployment Guide

This guide explains how to deploy the DoodStream Bot using Docker. This allows the bot to run 24/7 on any server (VPS) without needing a physical monitor.

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/) installed on your server or local machine.
- [Docker Compose](https://docs.docker.com/compose/install/) installed.

## Deployment Steps

1.  **Build and Run with Docker Compose**

    Run the following command in the project directory:

    ```bash
    docker-compose up -d --build
    ```

    - `-d`: Runs the container in detached mode (background).
    - `--build`: Rebuilds the image if you changed the Dockerfile.

2.  **View Logs**

    To see what the bot is doing:

    ```bash
    docker-compose logs -f
    ```

3.  **Stop the Bot**

    ```bash
    docker-compose down
    ```

## How it Works

- The `Dockerfile` uses the official Playwright Python image, which includes all necessary browser dependencies.
- It installs `xvfb` (X Virtual Framebuffer) to simulate a display.
- The command `Xvfb :99 ... & python main_bot.py` starts the virtual display and then runs your bot. This allows `headless=False` to work inside the container.

## VPS Recommendations

To run this 24/7, you can rent a Virtual Private Server (VPS) from providers like:

- DigitalOcean
- AWS (EC2)
- Google Cloud (Compute Engine)
- Hetzner
- Vultr

**Minimum Specs:**

- 2 CPU Cores
- 4GB RAM (Browsers are memory intensive)

## Deploying to Heroku

Since you have Heroku, you can deploy using the **Container Registry** (Docker) method. This is required because the bot needs a specific browser environment and `Xvfb` for the "headed" mode.

1.  **Install Heroku CLI**
    Download and install the [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli).

2.  **Login to Heroku**

    ```bash
    heroku login
    heroku container:login
    ```

3.  **Create an App**

    ```bash
    heroku create your-app-name
    ```

4.  **Set Stack to Container**
    Tell Heroku to use the `heroku.yml` and Docker configuration:

    ```bash
    heroku stack:set container
    ```

5.  **Deploy**
    Push your code to Heroku:

    ```bash
    git push heroku main
    ```

    _Note: Ensure you are in the `aiChallenge` directory or that your git root is set up correctly._

6.  **Scale the Worker**
    The bot runs as a background worker, not a web server.

    ```bash
    heroku ps:scale worker=1
    ```

7.  **View Logs**
    ```bash
    heroku logs --tail
    ```
