# Research checklist (every leg, every run)

Stephen's rule (2026-10-15): look at everything that helps pick the winner, including individual player stats, not just prices.
Every leg on a board gets this treatment, and its `why` field records what was found. If a checklist item can't be found, write "n/a". Don't skip it silently.

## Step 1: the anchor
A consensus sportsbook line (several books, or one sharp book) with the vig removed. This is the starting probability.
If no book prices the event (small ITF/Challenger events often aren't priced), say so; the stats then carry more weight.

## Step 2: the stats, by sport

### Tennis (singles)
- Current ranking and trend (rising or falling over the last 6 months); age.
- Season W-L, and the W-L on this surface (hard/clay/grass/indoor) this season and career.
- The last 10 matches: who they beat and lost to, and the opponents' level.
- Head-to-head: overall and on this surface.
- This week: matches already played, time on court, three-setters (fatigue). Travel, time zones.
- Level gap: tour regular vs qualifier or wildcard; college players (rankings understate them: check the college record).
- Retirements or injuries in the last month.

### Tennis (doubles)
- Each player's doubles ranking; combined team ranking.
- Do they play together regularly? Titles and finals as a team.
- Doubles specialists vs singles players paired up for one week (specialists win far more often than the rankings suggest).
- Results this week. Remember that Challenger and ITF doubles use a match tiebreak instead of a third set, so upsets are common: keep probabilities closer to 50/50 than the gap suggests.

### NFL / college football
- Injuries and inactives: QB first, then OL, top WR/RB, pass rush and CB. Practice reports (DNP/limited).
- Efficiency: EPA per play or success rate on offense and defense; points per drive; turnover margin (mostly luck: discount it).
- Matchups: pass rush vs pass protection, run defense vs run game, red-zone rates.
- Situation: rest (short week, coming off a bye), travel and time zones, altitude, home field.
- Weather for totals: wind above 15 mph lowers scoring; heavy rain and snow too.
- Line movement since open and what caused it.
- Player props: snap share, targets or carries per game, the opponent's defense against that position, and the game's projected script.

### NBA / college basketball
- Injuries and load management (check status about 30 minutes before tip).
- Back-to-backs, rest days, travel.
- Offensive and defensive rating, pace (for totals), last 10 games.
- Matchup: three-point volume vs three-point defense, rebounding.

### Everything else (MLB, NHL, soccer, MMA)
- Starters (pitcher, goalie, lineup), injuries, rest and travel.
- The 1-2 standard efficiency stats for that sport (e.g. xG for soccer, FIP for pitchers).
- Recent form vs season form.

## Step 3: set the probability
- Start at the anchor. Move only for specific findings above, and write each one in `why` with its source.
- Max move from the anchor: 4 points with a sharp anchor, 8 points without one (small events).
- Live matches: skip them unless the live score is known; the market sees the score before we do.
