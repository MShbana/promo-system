# Promo System

## About

> **Brief** — You are required to design a promo system in which users are assigned various
promos and can use the promo points in a specific task of their choosing.

## Installation & Configuration

1. Set up the PostgreSQL database
    - `sudo apt-get update && sudo apt-get install python3-pip python3-dev libpq-dev postgresql postgresql-contrib`
    - `sudo -u postgres psql`
        ```
        CREATE DATABASE <database_name>;

        CREATE USER <database_user> WITH PASSWORD '<database_use_password>';

        ALTER ROLE <database_user> SET client_encoding TO 'utf8';

        ALTER ROLE <database_user> SET default_transaction_isolation TO 'read committed';

        ALTER ROLE <database_user> SET timezone TO 'UTC';

        ALTER ROLE <database_user> CREATEDB;

        GRANT ALL PRIVILEGES ON DATABASE <database_name> TO <database_user>;

        \q
        ```


2. Set up the Django project
    - `git clone https://github.com/MShbana/promo-system.git`
    - `python3 -m venv promo-system-venv`
    - `source promo-system-venv/bin/activate`
    - `pip install -r requirements.txt`
    - `cd promo-system`
    - `nano .env`
        ```
        DEBUG=True
        SECRET_KEY=<placeholder>

        DATABASE_ENGINE=django.db.backends.postgresql
        DATABASE_NAME=<database_name>
        DATABASE_HOST=localhost
        DATABASE_PORT=5432
        DATABASE_USER=<database_user>
        DATABASE_PASSWORD=<database_use_password>
        ```
    - `python manage.py shell`
        ```
        from django.core.management.utils import get_random_secret_key
        get_random_secret_key()
        exit()
        ```
    - `nano .env`
        ```
        SECRET_KEY=<secret_key_generated_in_the_previous_step>
        ```
    - `python manage.py migrate`
    - `python manage runserver`
    - `python manage.py test`
    - `python manage.py createsuperuser`
        ```
        Username: admin
        Name: Admin Name
        Password: <password>
        Password (again): <password>

        ```
    - Create an API key to be able to register an admin user
        ```
        from rest_framework_api_key.models import APIKey
        api_key, key = APIKey.objects.create_key(name="my-remote-service")
        print(key)
        ```
    - Register an admin user, using the endpoint `POST {{base_url}}/accounts/register-admin-user/`,
    passing the generated api key (from the step above) as the authorization header.
        ```
        headers {
            Authorization: Api-Key <key>
        }
        ```
    - All available API endpoints are explained in the section below.


## Endpoints
- **Base URL**
    - Live: &nbsp;&nbsp;&nbsp; `https://promo-system.herokuapp.com/`
    - local: &nbsp;&nbsp;&nbsp; `http://127.0.0.1:8000`

- **Registration**

    1. **Register Admin User** &nbsp;&nbsp;&nbsp; `POST {{base_url}}/accounts/register-admin-user/`

        | Parameter     | Required  | type    | Notes   |
        | :------------:| :--------:| :------:| :----  |
        | Api-Key       | Yes       | string  | Sent to clients who consume the admin registration endpoint. |
        | username      | Yes       | string  |         |
        | name          | Yes       | string  |         |
        | password      | Yes       | string  |         |
        | password2     | Yes       | string  |         |
        | address       | No        | string  | Must be sent as an empty string if it doesn't have a value. |

        ```
        - Request:
            body sample: {
                "username": "AdminUserName",
                "name": "Admin Name",
                "password": "Some Password",
                "password2": "Some Password",
                "address": "Some Address" 
            }
            headers sample: {
                Authorization: Api-Key <client_api_key>
            }

        - Response:
            success response status code: 201 Created
            success response sample: {
                "id": 10,
                "username": "AdminUserName",
                "name": "Admin Name",
                "address": "Some Address",
                "auth_token": <auth_token>
            }
        ```

    2. **Register Normal User** &nbsp;&nbsp;&nbsp; `POST {{base_url}}/accounts/register-normal-user/`

        | Parameter     | Required  | type    | Notes   |
        | :------------:| :--------:| :------:| :----:  |
        | username      | Yes       | string  |         |
        | name          | Yes       | string  |         |
        | password      | Yes       | string  |         |
        | password2     | Yes       | string  |         |
        | mobile_number | Yes       | string  | Must to not exceed 15 characters long. |
        | address       | No        | string  | Must be sent as an empty string if it doesn't have a value. |

        ```
        - Request:
            body sample: {
                "username": "NormalUserName",
                "name": "Some Name",
                "password": "Some Password",
                "password2": "Some Password",
                "mobile_number": "01234567891",
                "address": "Some Address"
            }
            headers sample: {
                Authorization: Api-Key <client_api_key>
            }

        - Response:
            success response status code: 201 Created
            success response sample: {
                "id": 15,
                "username": "NormalUserName",
                "name": "Some Name",
                "mobile_number": "01234567891",
                "address": "Some Address",
                "auth_token": <auth_token>
            }
        ```

    3. **Login** &nbsp;&nbsp;&nbsp; `POST {{base_url}}/accounts/login/`

        | Parameter     | Required  | type    | Notes   |
        | :------------:| :--------:| :------:| :----:  |
        | username      | Yes       | string  |         |
        | password      | Yes       | string  |         |

        ```
        - Request:
            body sample: {
                "username": "Some username",
                "password": "Some password"
            }

        - Response:
            success response status code: 200 OK
            success response sample: {
                "auth_token": <auth_token>
            }
        ```

- **Promos adminstrating**

    | Parameter      | Required     | type              | Notes     |
    | :------------: | :------:     | :------:          |  :------: |
    | normal_user    | Yes          | integer           | ID of the normal user to whom the promo is assigned.          |
    | promo_code     | Yes          | string            |           |
    | promo_type     | Yes          | string            |           |
    | promo_amount   | Yes          | integer           |           |
    | description    | Yes          | string            |           |
    | start_time     | Yes          | dateTimeField     |           |
    | end_time       | Yes          | dateTimeField     |           |
    | is_active      | No           | boolean           | Defaults to true if not sent.          |


    1. **Create a promo** &nbsp;&nbsp;&nbsp; `POST {{base_url}}/promos/admin-user/`
        
        ```
        - Request:
            body sample: {
                "normal_user": 2,
                "promo_code": "SomePromoCode14",
                "promo_type": "Some Type",
                "promo_amount": 400,
                "description": "Some Description",
                "start_time": "2021-03-31T19:50:08",
                "end_time": "2021-05-24T19:50:08"
            }
            headers = {
                "Authorization": Token <admin_user_token>
            }

        - Response:
            success response HTTP Status Code: 201 Created
            success response sample: {
                "id": 14,
                "promo_code": "SomePromoCode14",
                "promo_type": "Some Type",
                "promo_amount": 400,
                "description": "Some Description",
                "creation_time": "2021-04-02T01:14:50.628092Z",
                "start_time": "2021-03-31T19:50:08Z",
                "end_time": "2021-05-24T19:50:08Z",
                "is_active": true,
                "normal_user": 2
            }
    2. **List all existing promos** &nbsp;&nbsp;&nbsp; `GET {{base_url}}/promos/admin-user/`

        *Each page returns 5 objects, response.next returns the next 5 objects.*
        ```
        - Request:
            headers = {
                "Authorization": Token <admin_user_token>
            }

        - Response:
            success response status code: 200 OK
            success response sample: {
                "count": 3,
                "next": "{{base_url}}/promos/admin-user/?page=2",
                "previous": null,
                "results": [
                    {
                        "id": 1,
                        "promo_code": "SomePromoCode1",
                        "promo_type": "Some Type",
                        "promo_amount": 100,
                        "description": "Some Description",
                        "creation_time": "2021-04-01T00:42:54.433292Z",
                        "start_time": "2021-03-31T19:50:08Z",
                        "end_time": "2021-05-24T19:50:08Z",
                        "is_active": true,
                        "normal_user": 3
                    },
                    {
                        "id": 2,
                        "promo_code": "SomePromoCode2",
                        "promo_type": "Some Type",
                        "promo_amount": 200,
                        "description": "Some Description",
                        "creation_time": "2021-04-01T00:44:25.731714Z",
                        "start_time": "2021-03-31T19:50:08Z",
                        "end_time": "2021-05-24T19:50:08Z",
                        "is_active": true,
                        "normal_user": 3
                    },
                ...
                ]
            }
        ```
    
    3. **Retreive a promo** &nbsp;&nbsp;&nbsp; `GET {{base_url}}/promos/admin-user/<promo_id>`

        ```
        - Request:
            headers = {
                "Authorization": Token <admin_user_token>
            }

        - Response:
            success response status code: 200 OK
            success response sample: {
                "id": 1,
                "promo_code": "SomePromoCode1",
                "promo_type": "Some Type",
                "promo_amount": 100,
                "description": "Some Description",
                "creation_time": "2021-04-01T00:42:54.433292Z",
                "start_time": "2021-03-31T19:50:08Z",
                "end_time": "2021-05-24T19:50:08Z",
                "is_active": true,
                "normal_user": 3
            }

        ```
    4. **Update a promo** &nbsp;&nbsp;&nbsp; `PATCH {{base_url}}/promos/admin-user/<promo_id>`

        *You can send one or more values to change.*

        ```
        - Request:
            body sample: {
                "promo_type": "Promo Type Updated",
                "is_active": false
            }
            headers = {
                "Authorization": Token <admin_user_token>
            }

        - Response:
            success response HTTP Status Code: 200 OK
            success response sample: {
                "id": 1,
                "promo_code": "SomePromoCode1",
                "promo_type": "Promo Type Updated",
                "promo_amount": 100,
                "description": "Some Description",
                "creation_time": "2021-04-01T00:42:54.433292Z",
                "start_time": "2021-03-31T19:50:08Z",
                "end_time": "2021-05-24T19:50:08Z",
                "is_active": false,
                "normal_user": 3
            }

        ```
    5. **Delete a promo** &nbsp;&nbsp;&nbsp; `DELETE {{base_url}}/promos/admin-user/<promo_id>`

        ```
        - Request:
            headers = {
                "Authorization": Token <admin_user_token>
            }

        - Response:
            success response HTTP Status Code: 204 No Content
            success response sample: None
        ```

- **User promos**
    1. **List all existing promos** &nbsp;&nbsp;&nbsp; `GET {{base_url}}/promos/normal-user/`
        *Each page returns 5 objects, response.next returns the next 5 objects.*
        
        ```
        - Request:
            headers = {
                "Authorization": Token <normal_user_token>
            }

        - Response:
            success response status code: 200 OK
            success response sample: {
                "count": 1,
                "next": null,
                "previous": null,
                "results": [
                    {
                        "id": 5,
                        "promo_code": "SomePromoCode5",
                        "promo_type": "Some Type",
                        "promo_amount": 500,
                        "description": "Some Description",
                        "start_time": "2021-03-31T19:50:08Z",
                        "end_time": "2021-05-24T20:08:07.127325Z"
                    },
                    {
                        "id": 6,
                        "promo_code": "SomePromoCode6",
                        "promo_type": "Some Type",
                        "promo_amount": 600,
                        "description": "Some Description",
                        "start_time": "2021-03-31T19:50:08Z",
                        "end_time": "2021-05-24T20:08:07.127325Z"
                    },
                    ...
                ]
            }
        ```
    
    2. **Retreive a promo** &nbsp;&nbsp;&nbsp; `GET {{base_url}}/promos/normal-user/<promo_id>`

        ```
        - Request:
            headers = {
                "Authorization": Token <normal_user_token>
            }

        - Response:
            success response status code: 200 OK
            success response sample:     {
                "id": 5,
                "promo_code": "SomePromoCode5",
                "promo_type": "Some Type",
                "promo_amount": 500,
                "description": "Some Description",
                "start_time": "2021-03-31T19:50:08Z",
                "end_time": "2021-05-24T20:08:07.127325Z"
            }

        ```

    3. **Deduct some points of a promo** &nbsp;&nbsp;&nbsp; `PATCH {{base_url}}/promos/normal-user/<promo_id>`

        | Parameter          | type              | Notes    |
        | :------------:     | :------:          | :------:    |
        | amt_to_deduct      | integer           | Must be an integer with a value that's greater than the promo_amount.    |

        ```
        - Request:
            body sample: {
                "amt_to_deduct": 200
            }
            headers = {
                "Authorization": Token <normal_user_token>
            }

        - Response:
            success response HTTP Status Code: 200 OK
            success response sample: {
                promo_amount: 300
            }

        ```
