# Team

**App:** Kids App
**ID format:** `team-{N}` (e.g. `team-1`)
**Storage:** SQLite (`TEAMS`, `TEAM_MEMBERS`)

## TEAMS Fields

| Field | Type | Notes |
|-------|------|-------|
| `team_id` | TEXT PK | Format: `team-{N}` |
| `name` | TEXT | Team display name |
| `total_points` | INTEGER | Sum of all member points (cached) |
| `created_at` | TIMESTAMP | |

## TEAM_MEMBERS Fields

| Field | Type | Notes |
|-------|------|-------|
| `member_id` | TEXT PK | Shared with `USER_PROFILES.member_id` |
| `team_id` | TEXT FK → Team | |
| `name` | TEXT | Member display name |
| `avatar` | TEXT | Avatar identifier |
| `points` | INTEGER | Individual points total |

## Relationships

- `TEAM_MEMBERS` — a team has many members (1:many)
- `USER_PROFILES` — each member has a profile (1:1, shared `member_id`)
- [[Challenge]] — members earn points by completing challenges

## Notes

- `total_points` is a cached sum — needs recalculation when member points change
- `TEAM_MEMBERS` and `USER_PROFILES` use the same `member_id` as their PK — they are effectively 1:1 with different data concerns (team membership vs profile info)
- Teams drive the leaderboard / ranking visible on the kids dashboard
