# Seed Web Project in Flask (Python)

## Summary

A Seed Web Project in Flask (Python) with basic functions.

## Features

- Basic Authentication
    + Password
    + CAPTCHA (With `Pillow`)
- User Management
    + Add User
    + Edit User (include Resetting Password)
    + Enable / Disable User
    + Search User
- ACL Support
- User Operation Records
    + Search Record
- Multi-Language (With `Flask-Babel`)
    + English
    + Simplified Chinese
    + Traditional Chinese
    + Japanese
- Deploy Ready (With `gunicorn`, `supervisord`)

## Dependency

See `requirements.txt`

## Envionment Variables

|        Name       |                Description                |                Default                 |
|-------------------|-------------------------------------------|----------------------------------------|
| ADMIN_EMAIL       | Admin email                               |                                        |
| SECRET_KEY        | Flask secret key                          | `h3bF9paWv9nNfAEo`                     |
| DEV_DATABASE_URL  | Database connection URL                   | `sqlite:///current-path/db-dev.sqlite` |
| PROD_DATABASE_URL | Database connection URL For Production    | `sqlite:///current-path/db.sqlite`     |
| FLASK_CONFIG      | Config name (`development`, `production`) | `default` (Same to `development`)      |

## Setup Database

```shell
python manage.py initdb
```

## Default Admin User

|     Email      |   Name  | Password |
|----------------|---------|----------|
| `$ADMIN_EMAIL` | `admin` | `admin!` |

## Run for development

```shell
./run-dev.sh
```

## Run for production

```shell
./run-deploy.sh
```

## Run for production in supervisord

```shell
supervisord
```

## Update Translation

```shell
./update-translations.sh
```

## License
[MIT](LICENSE)