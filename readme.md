# Gemini Telegram BOT

## Description
This project is a chatbot application that uses Google's Generative AI (Gemini) to generate responses. It is built with Python and uses Flask for the web server. The chatbot can be interacted with via a Telegram bot.


## Installation
1. Set up the Telegram bot using the BotFather on Telegram
2. Locally run and use ngork for webhook for the telegram.

## Environment Variables
The following environment variables are required for the application to run:

   | Variable             | Description                               | Default Value |
   |----------------------|-------------------------------------------|---------------|
   | `GEMINI_API_KEY`     | Your Gemini API key                       | None          |
   | `GEMINI_MODEL_NAME`  | The Gemini model name                     | `gemini-2.0-flash-lite`       |
   | `TELEGRAM_BOT_TOKEN` | Your Telegram Bot token                   | None          |
   | `OWM_API_KEY`        | Your [Open Weather Map](https://openweathermap.org/api) API Key             | None          |
   | `ENABLE_SECURE_WEBHOOK_TOKEN` | Enable validation of a secure token passed to the Telegram API webhook to prevent unauthorized access. Allowed values are 'True' or 'False'. | True |
   | `TELEGRAM_WEBHOOK_SECRET` | A secure token used to validate incoming requests to the Telegram API webhook. | None |
   
   
## Project Progress
This section tracks the progress of the project. The following features are planned or have been implemented:

- [x] Implement Gemini model
- [x] Implement a basic plugin
- [x] Implement DateTimePlugin
- [x] Implement gemini multimodal api, to recognize images and text
- [x] Chat history mode
- [x] Setup Continuous Delivery
- [x] Implement Secure Token Validation for Telegram Webhook Requests 
