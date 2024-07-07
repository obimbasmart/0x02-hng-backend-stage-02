from app.utils import get_settings

settings = get_settings()

def test_app_main_test_configs(test_client):
    assert settings.APP_STATE == "testing"
    assert "test" in settings.database_url