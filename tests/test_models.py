import pytest
from gdpy.models import User, Level, ModLevel, LevelDifficulty, LevelLength


class TestModels:
    def test_user_model_creation(self):
        data = {
            "1": "testuser",
            "2": "12345",
            "16": "67890",
            "3": "100",
            "46": "50",
        }
        user = User.model_validate(data)
        assert user.username == "testuser"
        assert user.user_id == 12345
        assert user.account_id == 67890
        assert user.stars == 100
        assert user.diamonds == 50

    def test_user_model_defaults(self):
        data = {"1": "test", "2": "1", "16": "1"}
        user = User.model_validate(data)
        assert user.stars == 0
        assert user.diamonds == 0
        assert user.mod_level == ModLevel.NONE

    def test_level_model_creation(self):
        data = {
            "1": "12345",
            "2": "Test Level",
            "6": "999",
            "10": "1000",
            "14": "500",
        }
        level = Level.model_validate(data)
        assert level.level_id == 12345
        assert level.name == "Test Level"
        assert level.author_id == 999
        assert level.downloads == 1000
        assert level.likes == 500

    def test_enums(self):
        assert ModLevel.NONE == 0
        assert ModLevel.MODERATOR == 1
        assert ModLevel.ELDER_MOD == 2
        assert LevelDifficulty.EASY == 2
        assert LevelLength.LONG == 3
