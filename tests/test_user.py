

def test_get_user_record_logged_in(test_client, reset_db,
                                   db_user, access_token):
    response = test_client.get(f"/api/users/{db_user.id}", headers={'Authorization': f'Bearer {access_token}'})
    assert response.status_code == 200

def test_get_user_record_logged_out(test_client, reset_db,
                                   db_user):
    response = test_client.get(f"/api/users/{db_user.id}")
    assert response.status_code == 401

def test_get_user_record_unauthorized(test_client):
    response = test_client.get("/api/users/fake_id")
    assert response.status_code == 401