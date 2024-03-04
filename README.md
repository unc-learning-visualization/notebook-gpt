# notebook-gpt-plugin

## Overview

This package creates a ChatGPT window inside a Jupyter Notebook and automatically creates a code history of using ChatGPT and the notebook.

## Install

Run the following to install the plugin.

```sh
pip3 install -i https://test.pypi.org/simple/ notebook-gpt-plugin --upgrade
```

## Usage

Import the plugin as shown below:

```python
from notebook_gpt_plugin import GPTPlugin
```

The plugin can be run with no arguments.

```python
GPTPlugin()
```

The plugin can also be given arguments for the student being tracked, the course, and problem they are working.

```python
user_id = "UniqueUserID"
course_id = "UniqueCourse"
problem = "Put the problem they are solving here."
GPTPlugin(user_id, course_id, problem)
```

## Config

This plugin requires access to the UNC GPT Endpoint. Config by creating a `.env` file with the following format:

```
API_SECRET=<API_SECRET>
```

The `.env` file should be on the same level as the notebook.
