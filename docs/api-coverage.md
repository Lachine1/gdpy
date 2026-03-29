# API Coverage

This page documents which Geometry Dash API endpoints are implemented in gdpy.

## Summary

| Category | Implemented | Total | Coverage |
| :--- | :---: | :---: | :---: |
| Accounts | 2 | 5 | 40% |
| Users | 3 | 4 | 75% |
| Levels | 6 | 14 | 43% |
| Comments | 3 | 7 | 43% |
| Songs | 2 | 6 | 33% |
| Social | 0 | 12 | 0% |
| Messages | 0 | 2 | 0% |
| Rewards | 0 | 3 | 0% |
| Lists | 0 | 3 | 0% |
| Misc | 0 | 6 | 0% |
| **Total** | **16** | **62** | **26%** |

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
| `updateGJAccSettings20.php` | - | :x: | Update account settings (requires auth) |

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
| `updateGJDesc20.php` | - | :x: | Update level description (requires auth) |

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
| `getCustomContentURL.php` | - | :x: | Get custom content URL |
| `musiclibrary_02.dat` | - | :x: | Music library |
| `sfxlibrary.dat` | - | :x: | SFX library |

---

## Social

| Endpoint | Method | Status | Notes |
| :--- | :--- | :--- | :--- |
| `getGJFriendRequests20.php` | - | :x: | Get friend requests (requires auth) |
| `uploadFriendRequest20.php` | - | :x: | Send friend request (requires auth) |
| `acceptGJFriendRequest20.php` | - | :x: | Accept friend request (requires auth) |
| `deleteGJFriendRequests20.php` | - | :x: | Delete friend request (requires auth) |
| `readGJFriendRequest20.php` | - | :x: | Mark friend request as read (requires auth) |
| `removeGJFriend20.php` | - | :x: | Remove friend (requires auth) |
| `getGJUserList20.php` | - | :x: | Get friends list (requires auth) |
| `blockGJUser20.php` | - | :x: | Block user (requires auth) |
| `unblockGJUser20.php` | - | :x: | Unblock user (requires auth) |
| `getGJMessages20.php` | - | :x: | Get messages (requires auth) |
| `downloadGJMessage20.php` | - | :x: | Download message content (requires auth) |
| `uploadGJMessage20.php` | - | :x: | Send message (requires auth) |

---

## Rewards

| Endpoint | Method | Status | Notes |
| :--- | :--- | :--- | :--- |
| `getGJChallenges.php` | - | :x: | Get quests/challenges (requires auth) |
| `getGJRewards.php` | - | :x: | Get rewards (requires auth) |
| `getGJSecretReward.php` | - | :x: | Get secret reward (requires auth) |

---

## Lists

| Endpoint | Method | Status | Notes |
| :--- | :--- | :--- | :--- |
| `getGJLevelLists.php` | - | :x: | Get level lists |
| `uploadGJLevelList.php` | - | :x: | Upload level list (requires auth) |
| `deleteGJLevelList.php` | - | :x: | Delete level list (requires auth) |

---

## Misc

| Endpoint | Method | Status | Notes |
| :--- | :--- | :--- | :--- |
| `getAccountURL.php` | - | :x: | Get account server URL |
| `getSaveData.php` | - | :x: | Get save data (requires auth) |
| `getTop1000.php` | - | :x: | Get top 1000 users |
| `likeGJItem211.php` | - | :x: | Like an item (requires auth) |
| `requestUserAccess.php` | - | :x: | Request user access |
| `restoreGJItems.php` | - | :x: | Restore deleted items (requires auth) |

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
- [ ] Backup/sync account

### No Auth Required (Lower Priority)

- [ ] Test song availability
- [ ] Get top 1000 users
- [ ] Get level lists

---

**Note:** This coverage list is based on the [Geometry Dash API documentation](https://github.com/Rifct/gd-docs).
