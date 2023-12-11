# notebook-gpt-plugin

## Overview

This package creates a ChatGPT window inside a Jupyter Notebook and automatically creates a code history of using ChatGPT and the notebook.

## Usage

See the [_Example Notebook.ipynb_](./Example%20Notebook.ipynb) for usage.

## Config

This plugin requires access to the UNC GPT Endpoint. Config by creating a `.env` file with the following format:

```
API_SECRET=<API_SECRET>
```

The `.env` file should be on the same level as the notebook.
