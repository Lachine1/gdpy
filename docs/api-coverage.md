# API Coverage

This page documents which Geometry Dash API endpoints are implemented in gdpy.

## Summary

| Category | Implemented | Total | Coverage |
| :--- | :---: | :---: | :---: |
| Authentication | 2 | 2 | 100% |
| Users | 4 | 4 | 100% |
| Levels | 7 | 13 | 54% |
| Comments | 3 | 7 | 43% |
| Songs | 2 | 3 | 67% |
| Social | 0 | 8 | 0% |
| Messages | 0 | 4 | 0% |
| Rewards | 0 | 2 | 0% |
| **Total** | **18** | **43** | **42%** |

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
| `updateGJUserScore22.php` | - | :x: | Update user stats (requires auth) |

---

## Levels

| Endpoint | Method | Status | Notes |
| :--- | :--- | :--- | :--- |
| `downloadGJLevel22.php` | `get_level()` | :white_check_mark: | Download level by ID (includes level string) |
| `getGJLevels21.php` | `search_levels()` | :white_check_mark: | Search levels |
| `getGJLevels21.php` | `get_user_levels()` | :white_check_mark: | Get user's created levels (type=5) |
| `getGJDailyLevel.php` | `get_daily_level()` | :white_check_mark: | Get daily/weekly/event level |
| `getGJGauntlets21.php` | `get_gauntlets()` | :white_check_mark: | Get gauntlets |
| `getGJMapPacks21.php` | `get_map_packs()` | :white_check_mark: | Get map packs |
| `uploadGJLevel21.php` | - | :x: | Upload level (requires auth) |
| `deleteGJLevelUser20.php` | - | :x: | Delete level (requires auth) |
| `rateGJStars211.php` | - | :x: | Rate level stars (requires auth) |
| `rateGJDemon21.php` | - | :x: | Rate demon difficulty (requires auth) |
| `suggestGJStars20.php` | - | :x: | Suggest stars for level (requires auth) |
| `reportGJLevel.php` | - | :x: | Report level (requires auth) |
| `getGJLevelScores211.php` | - | :x: | Get level leaderboard (requires auth) |

---

## Comments

| Endpoint | Method | Status | Notes |
| :--- | :--- | :--- | :--- |
| `getGJComments21.php` | `get_level_comments()` | :white_check_mark: | Get level comments |
| `getGJAccountComments20.php` | `get_account_comments()` | :white_check_mark: | Get profile comments |
| `getGJCommentHistory.php` | `get_comment_history()` | :white_check_mark: | Get user's comment history |
| `uploadGJComment21.php` | - | :x: | Post level comment (requires auth) |
| `uploadGJAccComment20.php` | - | :x: | Post profile comment (requires auth) |
| `deleteGJComment20.php` | - | :x: | Delete level comment (requires auth) |
| `deleteGJAccComment20.php` | - | :x: | Delete profile comment (requires auth) |

---

## Songs

| Endpoint | Method | Status | Notes |
| :--- | :--- | :--- | :--- |
| `getGJSongInfo.php` | `get_song()` | :white_check_mark: | Get song info by ID |
| `getGJTopArtists.php` | `get_top_artists()` | :white_check_mark: | Get top artists |
| `testSong.php` | - | :x: | Test song availability |

---

## Social

| Endpoint | Method | Status | Notes |
| :--- | :--- | :--- | :--- |
| `getGJFriendRequests20.php` | - | :x: | Get friend requests (requires auth) |
| `uploadGJFriendRequest20.php` | - | :x: | Send friend request (requires auth) |
| `acceptGJFriendRequest20.php` | - | :x: | Accept friend request (requires auth) |
| `deleteGJFriendRequest20.php` | - | :x: | Delete friend request (requires auth) |
| `removeGJFriend20.php` | - | :x: | Remove friend (requires auth) |
| `getGJUserList20.php` | - | :x: | Get friends list (requires auth) |
| `blockGJUser20.php` | - | :x: | Block user (requires auth) |
| `unblockGJUser20.php` | - | :x: | Unblock user (requires auth) |

---

## Messages

| Endpoint | Method | Status | Notes |
| :--- | :--- | :--- | :--- |
| `getGJMessages20.php` | - | :x: | Get messages (requires auth) |
| `downloadGJMessage20.php` | - | :x: | Download message content (requires auth) |
| `uploadGJMessage20.php` | - | :x: | Send message (requires auth) |
| `deleteGJMessages20.php` | - | :x: | Delete message(s) (requires auth) |

---

## Rewards

| Endpoint | Method | Status | Notes |
| :--- | :--- | :--- | :--- |
| `getGJChallenges.php` | - | :x: | Get quests/challenges (requires auth) |
| `getGJRewards.php` | - | :x: | Get rewards (requires auth) |

---

## Missing Features

### Requires Authentication
- [ ] Upload/delete levels
- [ ] Rate levels
- [ ] Post/delete comments
- [ ] Get/post profile comments
- [ ] Get friends list
- [ ] Send/accept friend requests
- [ ] Block/unblock users
- [ ] Get/read/send messages
- [ ] Get quests/rewards
- [ ] Get level leaderboard
- [ ] Update user stats

### No Auth Required (Lower Priority)
- [ ] Test song availability

---

**Note:** This coverage list is based on the [Geometry Dash API documentation](https://boomlings.dev).
