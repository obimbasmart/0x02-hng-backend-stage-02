# from app.crude import get_org_by_id, get get_org_by_id




def test_get_user_organisations_logged_in(test_client, reset_db,
                                          db_user, access_token):
    response = test_client.get("/api/organisations", headers={'Authorization': f'Bearer {access_token}'})

    assert response.status_code == 200

    response_json = response.json()
    assert response_json['status'] == 'success'
    assert response_json['message'] == '<message>'

    assert 'organisations' in response_json['data']
    assert response_json['data']['organisations'][0]['name']
    assert response_json['data']['organisations'][0]['orgId']
    assert response_json['data']['organisations'][0]['description'] is None

def test_create_organisation(test_client, access_token):
    response = test_client.post("/api/organisations",
                                json={"name": "MSFT's Organisation", "description": "Nice place to be"},
                                headers={'Authorization': f'Bearer {access_token}'})
    
    assert response.status_code == 201
    
def test_get_single_organisation_record_logged_in(test_client, reset_db,
                                                  db_user, access_token):
    
    response = test_client.get("/api/organisations/", headers={'Authorization': f'Bearer {access_token}'})

def test_add_user_to_organisation(test_client, reset_db, db_org, db_user):
    response = test_client.post(f"/api/organisations/{db_org.id}/users", json={"id": db_user.id})
    assert response.status_code == 200
    assert response.json()['status'] ==  'success'
    assert response.json()['message'] == 'User added to organisation successfully'