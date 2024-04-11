# Django Auth

<p align="center">
  <img src="https://1000logos.net/wp-content/uploads/2020/08/Django-Logo.png" />
</p>

## Introduction

This is my 1st project of django web framework, i am so exited to learn this awesome python api framework.

### First Time Set Up & Configuration

Install the Django Web Framework:

```bash
pip install django
pip install djangorestframework   
pip install django-filter   
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

Typescript configuration:

```bash
tsc --init
```

Create a file called `nodemon.json` and copy this code

```json
{
    "ignore": [
      ".git",
      "node_modules/",
      "dist/",
      "coverage/"
    ],
    "watch": [
      "src/*"
    ],
    "ext": "js,json,ts"
  }
```

## Features

List the main features of your admin server. For example:
- User authentication and authorization
- CRUD operations for managing resources
- Logging and monitoring
- Order & Checkout

## Requirements

Outline the prerequisites and dependencies needed to run your admin server. For example:
- Node.js (version)
- npm or yarn
- Database (if applicable)

## Installation

Provide step-by-step instructions for installing and setting up the project locally. Include commands and any additional configurations. For example:

```bash
git clone https://github.com/andyrhman/node-shop.git
cd node-admin
npm install