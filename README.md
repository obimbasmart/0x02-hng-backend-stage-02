# 0x02 - HNG Internship - Backend - Stage 02
> A robust REST API built with FastAPI and PostgreSQL, implementing authentication, authorization, and endpoints for user and organization management

> [View project description and requirement](https://fabulous-yogurt-1a4.notion.site/0X02-HNG-Internship-Backend-Stage-02-2829f7df22ce490e9b4777524dfb1c8f)

## API Documentation

- ### Authentication
    -  Registers a new user and creates a default organisation: `POST .../auth/register`
    -  Logs in a user: `POST .../auth/login`

- ### User
    - Gets a user record in same organisations: `GET /api/users/<user_id>`
    - Retrieves a User object: `GET /api/v1/users/<user_id>`

- ### Organisation
    - Retrieves all orgs the logged-in user belongs to or has createds: `<protected>`:  `GET .../api/organisation`
    - Creates a new organisation: `<protected>` `POST /api/organisation`
    - Adds a user to a particular organisation: `DELETE /api/organisation/<org_id>/users`
    - Gets a single organisation record: `<protected`: `GET /api/organisation/<org_id>`





## Examples of use
```bash
obimbasmart@MyXubuntu:~$ curl -X POST localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "firstName": "John",
    "lastName": "Doe",
    "email": "john.doe@example.com",
    "password": "password123",
    "phone": "+1234567890"
  }'
{
  "status": "success",
  "message": "Registration successful",
  "data": {
    "accessToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "user": {
      "userId": "987654321",
      "firstName": "John",
      "lastName": "Doe",
      "email": "john.doe@example.com",
      "phone": "+1234567890"
    }
  }
}
obimbasmart@MyXubuntu:~$ curl -X POST localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john.doe@example.com",
    "password": "password123"
  }'
{
  "status": "success",
  "message": "Login successful",
  "data": {
    "accessToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "user": {
      "userId": "987654321",
      "firstName": "John",
      "lastName": "Doe",
      "email": "john.doe@example.com",
      "phone": "+1234567890"
    }
  }
}
obimbasmart@MyXubuntu:~$ curl -X GET localhost:8000/api/v1/users/987654321 -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."

{
  "status": "success",
  "message": "User profile retrieved successfully",
  "data": {
    "userId": "987654321",
    "firstName": "John",
    "lastName": "Doe",
    "email": "john.doe@example.com",
    "phone": "+1234567890"
  }
}
obimbasmart@MyXubuntu:~$
.
.
.
```

### Tools: `FastAPI`,  `Postgress DB`