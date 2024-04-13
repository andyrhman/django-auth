# Django Auth

<p align="center">
  <img src="https://1000logos.net/wp-content/uploads/2020/08/Django-Logo.png" width="300" height="150" />
</p>

## Introduction

This is my 1st project of django web framework, i am so exited to learn this awesome python api framework.

### First Time Set Up & Configuration

Install the Django Web Framework:

```bash
pip install django
pip install djangorestframework   
pip install django-filter   
pip install psycopg2 # For database
pip install python-decouple # Installing python-decouple for .env:
```

Create the directory:

```bash
mkdir django-auth
django-admin startproject app .
django-admin startapp core
```

Go To settings.py and add this:

```python
INSTALLED_APPS = [
  // other lists,
  "rest_framework",
  "core"
]
```

## Features

List the main features of your autth server. For example:
- User authentication and authorization
- Auth Token
- 2FA Authentication

## Installation

Provide step-by-step instructions for installing and setting up the project locally. Include commands and any additional configurations. For example:

```bash
git clone https://github.com/andyrhman/node-auth.git
cd node-auth
pip install -t requirments.txt