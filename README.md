# Code Reviewer with LLMs

A lightweight code review agent that uses **OpenAI GPT-4** to evaluate **SQL** or **PySpark** code against provided business logic and optimization standards. Ideal for data engineers and analysts who want automated validation of their data transformation logic.


## Features

- Compares SQL or PySpark code against business logic
- Suggests optimization improvements
- Returns logic match result, optimization score, and summary
- Toggle review mode: logic only, optimization only, or both
- OpenAI API integration with `.env` file support
- Includes both real and mocked unit tests
- Test coverage reporting with `pytest-cov`


