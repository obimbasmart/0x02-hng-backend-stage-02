from app.schemas import UserInCreate


def test_auth_register_success(test_client,
                               user_data_create: UserInCreate,
                               reset_db):
    response = test_client.post('/auth/register', json=user_data_create.model_dump())
    assert response.status_code == 201
    response_json = response.json()
    assert response_json['status'] == "success"
    assert response_json['message'] == "Registration successful"

    assert response_json['data']['accessToken'] is not None
    
    assert response_json['data']['user']['userId']
    assert response_json['data']['user']['firstName'] == user_data_create.firstName
    assert response_json['data']['user']['lastName'] == user_data_create.lastName
    assert response_json['data']['user']['email'] == user_data_create.email
    assert response_json['data']['user']['phone'] == user_data_create.phone
    assert 'password' not in response_json['data']['user']

def test_auth_login_success(test_client,
                            user_data_out,
                            user_data_login):
    
    login_response = test_client.post('/auth/login', json=user_data_login.model_dump())
    assert login_response.status_code == 200

    login_response_json = login_response.json()
    assert login_response_json['data']['accessToken'] is not None
    assert login_response_json['status'] ==  "success"
    assert login_response_json['message'] ==  "Login successful"

    assert login_response_json['data']['user']['userId']
    assert login_response_json['data']['user']['firstName'] == user_data_out.firstName
    assert login_response_json['data']['user']['lastName'] == user_data_out.lastName
    assert login_response_json['data']['user']['email'] == user_data_out.email
    assert login_response_json['data']['user']['phone'] == user_data_out.phone


def test_auth_register_failure(test_client,
                               user_data_create: UserInCreate):
    response = test_client.post('/auth/register', json=user_data_create.model_dump())
    assert response.status_code == 400

    response_json = response.json()
    assert response_json['status'] == "Bad request"
    assert response_json['message'] == "Registration unsuccessful"
    assert response_json['statusCode'] == 400

def test_auth_login_failure(test_client):
    response = test_client.post('/auth/login', json={
        "email": "oleg@gmail.com", "password": "wrong_password"})
    
    assert response.status_code == 401

    response_json = response.json()
    assert response_json['status'] == "Bad request"
    assert response_json['message'] == "Authentication failed"
    assert response_json['statusCode'] == 401

def test_auth_validation_error(test_client):
    response = test_client.post('/auth/register', json={"emal" : "notcorrect@gmail.com", "password": "1234"})
    assert response.status_code == 422

def test_auth_validation_error(test_client):
    response = test_client.post('/auth/login', json={"emal" : "notcorrect@gmail.com", "password": "1234"})
    assert response.status_code == 422


    