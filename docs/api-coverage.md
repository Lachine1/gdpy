# API Coverage

This page documents which Geometry Dash API endpoints are implemented in gdpy.

## Summary

| Category | Implemented | Total | Coverage |
| :--- | :---: | :---: | :---: |
| Authentication | 2 | 2 | 100% |
| Users | 4 | 4 | 100% |
| Levels | 4 | 13 | 31% |
| Comments | 1 | 7 | 14% |
| Songs | 1 | 3 | 33% |
| Social | 0 | 8 | 0% |
| Messages | 0 | 4 | 0% |
| Rewards | 0 | 2 | 0% |
| **Total** | **12** | **43** | **28%** |

## Legend

| Status | Meaning |
| :--- | :--- |
| :white_check_mark: Implemented | Fully working and tested |
| :warning: Partial | Implemented but may be incomplete |
| :x: Not Implemented | Not yet available |

---

## Authentication

| Endpoint | Method | Status | Notes |
| :--- | :--- | :--- | :--- |
| `accounts/loginGJAccount.php` | `login()` | :white_check_mark: | Login with username/password |
| `accounts/registerGJAccount.php` | `register()` | :white_check_mark: | Register new account |

---

## Users

| Endpoint | Method | Status | Notes |
| :--- | :--- | :--- | :--- |
| `getGJUserInfo20.php` | `get_user()` | :white_check_mark: | Get user by account ID |
| `getGJUsers20.php` | `search_users()` | :white_check_mark: | Search users by name |
| `getGJScores20.php` | `get_leaderboard()` | :white_check_mark: | Get global/creator leaderboard |
| `updateGJUserScore22.php` | - | :x: | Update user stats |

---

## Levels

| Endpoint | Method | Status | Notes |
| :--- | :--- | :--- | :--- |
| `downloadGJLevel22.php` | `get_level()` | :white_check_mark: | Download level by ID (includes level string) |
| `getGJLevels21.php` | `search_levels()` | :white_check_mark: | Search levels |
| `getGJLevels21.php` | `get_user_levels()` | :white_check_mark: | Get user's created levels (type=5) |
| `getGJDailyLevel.php` | - | :x: | Get daily/weekly/event level |
| `uploadGJLevel21.php` | - | :x: | Upload level |
| `deleteGJLevelUser20.php` | - | :x: | Delete level |
| `rateGJStars211.php` | - | :x: | Rate level stars |
| `rateGJDemon21.php` | - | :x: | Rate demon difficulty |
| `suggestGJStars20.php` | - | :x: | Suggest stars for level |
| `reportGJLevel.php` | - | :x: | Report level |
| `getGJGauntlets21.php` | - | :x: | Get gauntlets |
| `getGJMapPacks21.php` | - | :x: | Get map packs |
| `getGJLevelScores211.php` | - | :x: | Get level leaderboard |

---

## Comments

| Endpoint | Method | Status | Notes |
| :--- | :--- | :--- | :--- |
| `getGJComments21.php` | `get_level_comments()` | :white_check_mark: | Get level comments |
| `getGJAccountComments20.php` | - | :x: | Get profile comments |
| `getGJCommentHistory.php` | - | :x: | Get user's comment history |
| `uploadGJComment21.php` | - | :x: | Post level comment |
| `uploadGJAccComment20.php` | - | :x: | Post profile comment |
| `deleteGJComment20.php` | - | :x: | Delete level comment |
| `deleteGJAccComment20.php` | - | :x: | Delete profile comment |

---

## Songs

| Endpoint | Method | Status | Notes |
| :--- | :--- | :--- | :--- |
| `getGJSongInfo.php` | `get_song()` | :white_check_mark: | Get song info by ID |
| `getGJTopArtists.php` | - | :x: | Get top artists |
| `testSong.php` | - | :x: | Test song availability |

---

## Social

| Endpoint | Method | Status | Notes |
| :--- | :--- | :--- | :--- |
| `getGJFriendRequests20.php` | - | :x: | Get friend requests |
| `uploadGJFriendRequest20.php` | - | :x: | Send friend request |
| `acceptGJFriendRequest20.php` | - | :x: | Accept friend request |
| `deleteGJFriendRequest20.php` | - | :x: | Delete friend request |
| `removeGJFriend20.php` | - | :x: | Remove friend |
| `getGJUserList20.php` | - | :x: | Get friends list |
| `blockGJUser20.php` | - | :x: | Block user |
| `unblockGJUser20.php` | - | :x: | Unblock user |

---

## Messages

| Endpoint | Method | Status | Notes |
| :--- | :--- | :--- | :--- |
| `getGJMessages20.php` | - | :x: | Get messages |
| `downloadGJMessage20.php` | - | :x: | Download message content |
| `uploadGJMessage20.php` | - | :x: | Send message |
| `deleteGJMessages20.php` | - | :x: | Delete message(s) |

---

## Rewards

| Endpoint | Method | Status | Notes |
| :--- | :--- | :--- | :--- |
| `getGJChallenges.php` | - | :x: | Get quests/challenges |
| `getGJRewards.php` | - | :x: | Get rewards |

---

## Missing Features

### High Priority
- [ ] Get daily/weekly levels
- [ ] Get friends list
- [ ] Get/read messages
- [ ] Post comments
- [ ] Get profile comments

### Medium Priority
- [ ] Upload/delete levels
- [ ] Rate levels
- [ ] Get gauntlets
- [ ] Get map packs
- [ ] Get level leaderboard

### Low Priority
- [ ] Send friend requests
- [ ] Block users
- [ ] Get quests
- [ ] Update user stats

---

**Note:** This coverage list is based on the [gd-docs](https://github.com/Rifct/gd-docs) API documentation.
