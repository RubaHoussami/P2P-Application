import os
import pytest
from config import config
from unittest.mock import patch


@pytest.mark.parametrize(
    "environment",
    [
        "default",
        "development",
        "production",
        "testing",
    ]
)
def test_config(environment: str):
    with patch.dict(os.environ, {
        "APP_NAME": "test-name",
        "APP_DESCRIPTION": "test-description",
        "APP_VERSION": "test-version",
        "SQLALCHEMY_DATABASE_URI": "test-uri",
        "SQLALCHEMY_DATABASE_URI_TEST": "testing-uri",
        "JWT_SECRET_KEY": "test-secret-key",
        "JWT_ACCESS_TOKEN_EXPIRES": "3600",
        "JWT_REFRESH_TOKEN_EXPIRES": "7200",
        "JWT_BLOCKLIST_ENABLED": "True",
        "JWT_BLOCKLIST_TOKEN_CHECKS": "access,refresh",
        "FLASK_ENV": environment,
    }):
        conf = config[environment]()
        assert conf.APP_NAME == 'test-name'
        assert conf.APP_DESCRIPTION == 'test-description'
        assert conf.APP_VERSION == 'test-version'
        if environment == 'production':
            assert not conf.FLASK_DEBUG
        else:
            assert conf.FLASK_DEBUG
        if environment == 'testing':
            assert conf.SQLALCHEMY_DATABASE_URI == 'testing-uri'
        else:
            assert conf.SQLALCHEMY_DATABASE_URI == 'test-uri'
        assert conf.JWT_SECRET_KEY == 'test-secret-key'
        assert conf.JWT_ACCESS_TOKEN_EXPIRES.total_seconds() == 3600
        assert conf.JWT_REFRESH_TOKEN_EXPIRES.total_seconds() == 7200
        assert conf.JWT_BLOCKLIST_ENABLED
        assert conf.JWT_BLOCKLIST_TOKEN_CHECKS == ['access', 'refresh']
