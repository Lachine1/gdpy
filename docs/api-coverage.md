# API Coverage

This page documents which Geometry Dash API endpoints are implemented in gdpy.

## Summary

| Category | Implemented | Total | Coverage |
| :--- | :---: | :---: | :---: |
| Accounts | 3 | 5 | 60% |
| Users | 4 | 4 | 100% |
| Levels | 10 | 11 | 91% |
| Comments | 7 | 7 | 100% |
| Songs | 3 | 6 | 50% |
| Social | 12 | 12 | 100% |
| Messages | 4 | 4 | 100% |
| Rewards | 2 | 3 | 67% |
| Lists | 1 | 3 | 33% |
| Misc | 2 | 2 | 100% |
| **Total** | **48** | **57** | **84%** |

## Legend

| Status | Meaning |
| :--- | :--- |
| :white_check_mark: Implemented | Fully working and tested |
| :warning: Partial | Implemented but may be incomplete |
| :x: Not Implemented | Not yet available |

---

## Accounts

| Endpoint | Method | Status | Notes |
| :--- | :--- | :--- | :--- |
| `accounts/loginGJAccount.php` | `login()` | :white_check_mark: | Login with username/password |
| `accounts/registerGJAccount.php` | `register()` | :warning: | Pre-2.2 API; rejects temp emails |
| `accounts/backupGJAccountNew.php` | - | :x: | Backup account (requires auth) |
| `accounts/syncGJAccountNew.php` | - | :x: | Sync account (requires auth) |
| `updateGJAccSettings20.php` | `update_account_settings()` | :white_check_mark: | Update account settings (requires auth) |

---

## Users

| Endpoint | Method | Status | Notes |
| :--- | :--- | :--- | :--- |
| `getGJUserInfo20.php` | `get_user()` | :white_check_mark: | Get user by account ID |
| `getGJUsers20.php` | `search_users()` | :white_check_mark: | Search users by name |
| `getGJScores20.php` | `get_leaderboard()` | :white_check_mark: | Get global/creator leaderboard |
| `updateGJUserScore22.php` | `update_user_stats()` | :white_check_mark: | Update user stats (requires auth) |

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
| `uploadGJLevel21.php` | `upload_level()` | :white_check_mark: | Upload level (requires auth) |
| `deleteGJLevelUser20.php` | `delete_level()` | :white_check_mark: | Delete level (requires auth) |
| `reportGJLevel.php` | `report_level()` | :white_check_mark: | Report level |
| `getGJLevelScores211.php` | `get_level_scores()` | :white_check_mark: | Get level leaderboard (requires auth) |
| `updateGJDesc20.php` | `update_level_description()` | :white_check_mark: | Update level description (requires auth) |

---

## Comments

| Endpoint | Method | Status | Notes |
| :--- | :--- | :--- | :--- |
| `getGJComments21.php` | `get_level_comments()` | :white_check_mark: | Get level comments |
| `getGJAccountComments20.php` | `get_account_comments()` | :white_check_mark: | Get profile comments |
| `getGJCommentHistory.php` | `get_comment_history()` | :white_check_mark: | Get user's comment history |
| `uploadGJComment21.php` | `post_level_comment()` | :white_check_mark: | Post level comment (requires auth) |
| `uploadGJAccComment20.php` | `post_profile_comment()` | :white_check_mark: | Post profile comment (requires auth) |
| `deleteGJComment20.php` | `delete_level_comment()` | :white_check_mark: | Delete level comment (requires auth) |
| `deleteGJAccComment20.php` | `delete_profile_comment()` | :white_check_mark: | Delete profile comment (requires auth) |

---

## Songs

| Endpoint | Method | Status | Notes |
| :--- | :--- | :--- | :--- |
| `getGJSongInfo.php` | `get_song()` | :white_check_mark: | Get song info by ID |
| `getGJTopArtists.php` | `get_top_artists()` | :white_check_mark: | Get top artists |
| `testSong.php` | `test_song()` | :white_check_mark: | Test song availability |
| `getCustomContentURL.php` | - | :x: | Get custom content URL |
| `musiclibrary_02.dat` | - | :x: | Music library |
| `sfxlibrary.dat` | - | :x: | SFX library |

---

## Social

| Endpoint | Method | Status | Notes |
| :--- | :--- | :--- | :--- |
| `getGJFriendRequests20.php` | `get_friend_requests()` | :white_check_mark: | Get friend requests (requires auth) |
| `uploadFriendRequest20.php` | `send_friend_request()` | :white_check_mark: | Send friend request (requires auth) |
| `acceptGJFriendRequest20.php` | `accept_friend_request()` | :white_check_mark: | Accept friend request (requires auth) |
| `deleteGJFriendRequests20.php` | `delete_friend_request()` | :white_check_mark: | Delete friend request (requires auth) |
| `readGJFriendRequest20.php` | `read_friend_request()` | :white_check_mark: | Mark friend request as read (requires auth) |
| `removeGJFriend20.php` | `remove_friend()` | :white_check_mark: | Remove friend (requires auth) |
| `getGJUserList20.php` | `get_friends()`, `get_blocked_users()` | :white_check_mark: | Get friends/blocked list (requires auth) |
| `blockGJUser20.php` | `block_user()` | :white_check_mark: | Block user (requires auth) |
| `unblockGJUser20.php` | `unblock_user()` | :white_check_mark: | Unblock user (requires auth) |
| `getGJMessages20.php` | `get_messages()` | :white_check_mark: | Get messages (requires auth) |
| `downloadGJMessage20.php` | `get_message()` | :white_check_mark: | Download message content (requires auth) |
| `uploadGJMessage20.php` | `send_message()` | :white_check_mark: | Send message (requires auth) |

---

## Rewards

| Endpoint | Method | Status | Notes |
| :--- | :--- | :--- | :--- |
| `getGJChallenges.php` | `get_challenges()` | :white_check_mark: | Get daily quests (requires auth) |
| `getGJRewards.php` | `get_chest_rewards()` | :white_check_mark: | Get chest rewards (requires auth) |
| `getGJSecretReward.php` | - | :x: | Secret vault reward (requires auth) |

---

## Lists

| Endpoint | Method | Status | Notes |
| :--- | :--- | :--- | :--- |
| `getGJLevelLists.php` | `get_level_lists()` | :white_check_mark: | Get level lists |
| `uploadGJLevelList.php` | - | :x: | Upload level list (requires auth) |
| `deleteGJLevelList.php` | - | :x: | Delete level list (requires auth) |

---

## Misc

| Endpoint | Method | Status | Notes |
| :--- | :--- | :--- | :--- |
| `getTop1000.php` | `get_top_1000()` | :white_check_mark: | Get top 1000 users |
| `likeGJItem211.php` | `like_level()`, `like_comment()` | :white_check_mark: | Like an item (requires auth) |

---

## Rewards

| Endpoint | Method | Status | Notes |
| :--- | :--- | :--- | :--- |
| `getGJChallenges.php` | `get_challenges()` | :white_check_mark: | Get daily quests (requires auth) |
| `getGJRewards.php` | `get_chest_rewards()` | :white_check_mark: | Get chest rewards (requires auth) |
| `getGJSecretReward.php` | - | :x: | Secret vault reward (requires auth) |

---

## Missing Features

### Requires Authentication

- [x] Post/delete comments
- [x] Get/post profile comments
- [x] Get friends list
- [x] Send/accept friend requests
- [x] Block/unblock users
- [x] Get/read/send messages
- [x] Like levels/comments
- [x] Mark friend request as read
- [x] Update user stats
- [x] Get level leaderboard
- [x] Update level description
- [x] Update account settings
- [x] Get daily quests
- [x] Get chest rewards
- [x] Upload/delete levels
- [x] Report levels
- [ ] Secret vault reward
- [ ] Backup/sync account

### No Auth Required (Lower Priority)

- [x] Test song availability
- [x] Get top 1000 users
- [x] Get level lists

---

**Note:** This coverage list is based on the [Geometry Dash API documentation](https://github.com/Rifct/gd-docs).
