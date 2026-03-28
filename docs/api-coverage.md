# API Coverage

This page documents which Geometry Dash API endpoints are implemented in gdpy.

## Legend

| Status | Meaning |
| :--- | :--- |
| ✅ Implemented | Fully working and tested |
| ⚠️ Partial | Implemented but may be incomplete |
| ❌ Not Implemented | Not yet available |

---

## Authentication

| Endpoint | Method | Status | Notes |
| :--- | :--- | :--- | :--- |
| `accounts/loginGJAccount.php` | `login()` | ✅ | Login with username/password |
| `accounts/registerGJAccount.php` | `register()` | ✅ | Register new account |

---

## Users

| Endpoint | Method | Status | Notes |
| :--- | :--- | :--- | :--- |
| `getGJUserInfo20.php` | `get_user()` | ✅ | Get user by account ID |
| `getGJUsers20.php` | `search_users()` | ✅ | Search users by name |
| `getGJScores20.php` | `get_leaderboard()` | ✅ | Get global/creator leaderboard |
| `updateGJUserScore22.php` | - | ❌ | Update user stats |

---

## Levels

| Endpoint | Method | Status | Notes |
| :--- | :--- | :--- | :--- |
| `downloadGJLevel22.php` | `get_level()` | ✅ | Download level by ID (includes level string) |
| `getGJLevels21.php` | `search_levels()` | ✅ | Search levels |
| `getGJLevels21.php` | `get_user_levels()` | ✅ | Get user's created levels (type=5) |
| `getGJDailyLevel.php` | - | ❌ | Get daily/weekly/event level |
| `uploadGJLevel21.php` | - | ❌ | Upload level |
| `deleteGJLevelUser20.php` | - | ❌ | Delete level |
| `rateGJStars211.php` | - | ❌ | Rate level stars |
| `rateGJDemon21.php` | - | ❌ | Rate demon difficulty |
| `suggestGJStars20.php` - | ❌ | Suggest stars for level |
| `reportGJLevel.php` | - | ❌ | Report level |
| `getGJGauntlets21.php` | - | ❌ | Get gauntlets |
| `getGJMapPacks21.php` | - | ❌ | Get map packs |
| `getGJLevelScores211.php` | - | ❌ | Get level leaderboard |

---

## Comments

| Endpoint | Method | Status | Notes |
| :--- | :--- | :--- | :--- |
| `getGJComments21.php` | `get_level_comments()` | ✅ | Get level comments |
| `getGJAccountComments20.php` | - | ❌ | Get profile comments |
| `getGJCommentHistory.php` | - | ❌ | Get user's comment history |
| `uploadGJComment21.php` | - | ❌ | Post level comment |
| `uploadGJAccComment20.php` | - | ❌ | Post profile comment |
| `deleteGJComment20.php` | - | ❌ | Delete level comment |
| `deleteGJAccComment20.php` | - | ❌ | Delete profile comment |

---

## Songs

| Endpoint | Method | Status | Notes |
| :--- | :--- | :--- | :--- |
| `getGJSongInfo.php` | `get_song()` | ✅ | Get song info by ID |
| `getGJTopArtists.php` | - | ❌ | Get top artists |
| `testSong.php` | - | ❌ | Test song availability |

---

## Social

| Endpoint | Method | Status | Notes |
| :--- | :--- | :--- | :--- |
| `getGJFriendRequests20.php` | - | ❌ | Get friend requests |
| `uploadGJFriendRequest20.php` | - | ❌ | Send friend request |
| `acceptGJFriendRequest20.php` | - | ❌ | Accept friend request |
| `deleteGJFriendRequest20.php` | - | ❌ | Delete friend request |
| `removeGJFriend20.php` | - | ❌ | Remove friend |
| `getGJUserList20.php` | - | ❌ | Get friends list |
| `blockGJUser20.php` | - | ❌ | Block user |
| `unblockGJUser20.php` | - | ❌ | Unblock user |

---

## Messages

| Endpoint | Method | Status | Notes |
| :--- | :--- | :--- | :--- |
| `getGJMessages20.php` | - | ❌ | Get messages |
| `downloadGJMessage20.php` | - | ❌ | Download message content |
| `uploadGJMessage20.php` | - | ❌ | Send message |
| `deleteGJMessages20.php` | - | ❌ | Delete message(s) |

---

## Rewards

| Endpoint | Method | Status | Notes |
| :--- | :--- | :--- | :--- |
| `getGJChallenges.php` | - | ❌ | Get quests/challenges |
| `getGJRewards.php` | - | ❌ | Get rewards |

---

## Summary

| Category | Implemented | Total | Coverage |
| :--- | :--- | :--- | :--- |
| Authentication | 2 | 2 | 100% |
| Users | 4 | 4 | 100% |
| Levels | 4 | 13 | 31% |
| Comments | 1 | 7 | 14% |
| Songs | 1 | 3 | 33% |
| Social | 0 | 8 | 0% |
| Messages | 0 | 4 | 0% |
| Rewards | 0 | 2 | 0% |
| **Total** | **12** | **43** | **28%** |

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
