from gdpy.models import Level, LevelDifficulty, LevelLength, ModLevel, User


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

    def test_difficulty_easy(self):
        data = {"1": "1", "2": "Easy Level", "6": "1", "9": "10"}
        level = Level.model_validate(data)
        assert level.difficulty == LevelDifficulty.EASY

    def test_difficulty_normal(self):
        data = {"1": "1", "2": "Normal Level", "6": "1", "9": "20"}
        level = Level.model_validate(data)
        assert level.difficulty == LevelDifficulty.NORMAL

    def test_difficulty_hard(self):
        data = {"1": "1", "2": "Hard Level", "6": "1", "9": "30"}
        level = Level.model_validate(data)
        assert level.difficulty == LevelDifficulty.HARD

    def test_difficulty_harder(self):
        data = {"1": "1", "2": "Harder Level", "6": "1", "9": "40"}
        level = Level.model_validate(data)
        assert level.difficulty == LevelDifficulty.HARDER

    def test_difficulty_insane(self):
        data = {"1": "1", "2": "Insane Level", "6": "1", "9": "50"}
        level = Level.model_validate(data)
        assert level.difficulty == LevelDifficulty.INSANE

    def test_difficulty_auto(self):
        data = {"1": "1", "2": "Auto Level", "6": "1", "25": "1"}
        level = Level.model_validate(data)
        assert level.difficulty == LevelDifficulty.AUTO

    def test_difficulty_easy_demon(self):
        data = {"1": "1", "2": "Easy Demon", "6": "1", "17": "1", "43": "3"}
        level = Level.model_validate(data)
        assert level.difficulty == LevelDifficulty.EASY_DEMON

    def test_difficulty_medium_demon(self):
        data = {"1": "1", "2": "Medium Demon", "6": "1", "17": "1", "43": "4"}
        level = Level.model_validate(data)
        assert level.difficulty == LevelDifficulty.MEDIUM_DEMON

    def test_difficulty_hard_demon(self):
        data = {"1": "1", "2": "Hard Demon", "6": "1", "17": "1", "43": "0"}
        level = Level.model_validate(data)
        assert level.difficulty == LevelDifficulty.HARD_DEMON

    def test_difficulty_insane_demon(self):
        data = {"1": "1", "2": "Insane Demon", "6": "1", "17": "1", "43": "5"}
        level = Level.model_validate(data)
        assert level.difficulty == LevelDifficulty.INSANE_DEMON

    def test_difficulty_extreme_demon(self):
        data = {"1": "1", "2": "Extreme Demon", "6": "1", "17": "1", "43": "6"}
        level = Level.model_validate(data)
        assert level.difficulty == LevelDifficulty.EXTREME_DEMON

    def test_difficulty_unspecified(self):
        data = {"1": "1", "2": "Unrated Level", "6": "1"}
        level = Level.model_validate(data)
        assert level.difficulty == LevelDifficulty.UNSPECIFIED
