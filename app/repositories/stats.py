from __future__ import annotations

import textwrap
from typing import Any
from typing import Optional

import app.state.services

# +--------------+-----------------+------+-----+---------+----------------+
# | Field        | Type            | Null | Key | Default | Extra          |
# +--------------+-----------------+------+-----+---------+----------------+
# | id           | int             | NO   | PRI | NULL    | auto_increment |
# | mode         | tinyint(1)      | NO   | PRI | NULL    |                |
# | tscore       | bigint unsigned | NO   |     | 0       |                |
# | rscore       | bigint unsigned | NO   |     | 0       |                |
# | pp           | int unsigned    | NO   |     | 0       |                |
# | plays        | int unsigned    | NO   |     | 0       |                |
# | playtime     | int unsigned    | NO   |     | 0       |                |
# | acc          | float(6,3)      | NO   |     | 0.000   |                |
# | max_combo    | int unsigned    | NO   |     | 0       |                |
# | total_hits   | int unsigned    | NO   |     | 0       |                |
# | replay_views | int unsigned    | NO   |     | 0       |                |
# | xh_count     | int unsigned    | NO   |     | 0       |                |
# | x_count      | int unsigned    | NO   |     | 0       |                |
# | sh_count     | int unsigned    | NO   |     | 0       |                |
# | s_count      | int unsigned    | NO   |     | 0       |                |
# | a_count      | int unsigned    | NO   |     | 0       |                |
# +--------------+-----------------+------+-----+---------+----------------+

READ_PARAMS = textwrap.dedent(
    """\
        id, mode, tscore, rscore, pp, plays, playtime, acc, max_combo, total_hits,
        replay_views, xh_count, x_count, sh_count, s_count, a_count
    """,
)


async def create(
    player_id: int,
    mode: int,
    # TODO: should we allow init with values?
) -> dict[str, Any]:
    """Create a new player stats entry in the database."""
    query = f"""\
        INSERT INTO stats (id, mode)
        VALUES (:id, :mode)
    """
    params = {
        "id": player_id,
        "mode": mode,
    }
    rec_id = await app.state.services.database.execute(query, params)

    query = f"""\
        SELECT {READ_PARAMS}
          FROM stats
         WHERE id = :id
    """
    params = {
        "id": rec_id,
    }
    rec = await app.state.services.database.fetch_one(query, params)
    return rec


async def fetch_one(
    player_id: int,
    mode: int,
) -> Optional[dict[str, Any]]:
    """Fetch a player stats entry from the database."""
    query = f"""\
        SELECT {READ_PARAMS}
          FROM stats
         WHERE id = :id
           AND mode = :mode
    """
    params = {
        "id": player_id,
        "mode": mode,
    }
    rec = await app.state.services.database.fetch_one(query, params)
    return rec


async def fetch_count() -> int:
    query = f"""\
        SELECT COUNT(*) AS count
          FROM stats
    """
    params = None

    rec = await app.state.services.database.fetch_one(query, params)
    return rec["count"]


async def fetch_many(
    page: Optional[int] = None,
    page_size: Optional[int] = None,
) -> list[dict[str, Any]]:
    query = f"""\
        SELECT {READ_PARAMS}
          FROM stats
    """
    params = {}

    if page is not None and page_size is not None:
        query += """\
            LIMIT :limit
           OFFSET :offset
        """
        params["limit"] = page_size
        params["offset"] = (page - 1) * page_size

    recs = await app.state.services.database.fetch_all(query, params)
    return recs


async def update(
    player_id: int,
    mode: int,
    tscore: Optional[int] = None,
    rscore: Optional[int] = None,
    pp: Optional[int] = None,
    plays: Optional[int] = None,
    playtime: Optional[int] = None,
    acc: Optional[float] = None,
    max_combo: Optional[int] = None,
    total_hits: Optional[int] = None,
    replay_views: Optional[int] = None,
    xh_count: Optional[int] = None,
    x_count: Optional[int] = None,
    sh_count: Optional[int] = None,
    s_count: Optional[int] = None,
    a_count: Optional[int] = None,
):
    """Update a player stats entry in the database."""
    query = f"""\
        UPDATE stats
           SET tscore = COALESCE(:tscore, tscore),
               rscore = COALESCE(:rscore, rscore),
               pp = COALESCE(:pp, pp),
               plays = COALESCE(:plays, plays),
               playtime = COALESCE(:playtime, playtime),
               acc = COALESCE(:acc, acc),
               max_combo = COALESCE(:max_combo, max_combo),
               total_hits = COALESCE(:total_hits, total_hits),
               replay_views = COALESCE(:replay_views, replay_views),
               xh_count = COALESCE(:xh_count, xh_count),
               x_count = COALESCE(:x_count, x_count),
               sh_count = COALESCE(:sh_count, sh_count),
               s_count = COALESCE(:s_count, s_count),
               a_count = COALESCE(:a_count, a_count)
         WHERE id = :id
           AND mode = :mode
    """
    params = {
        "id": player_id,
        "mode": mode,
        "tscore": tscore,
        "rscore": rscore,
        "pp": pp,
        "plays": plays,
        "playtime": playtime,
        "acc": acc,
        "max_combo": max_combo,
        "total_hits": total_hits,
        "replay_views": replay_views,
        "xh_count": xh_count,
        "x_count": x_count,
        "sh_count": sh_count,
        "s_count": s_count,
        "a_count": a_count,
    }
    await app.state.services.database.execute(query, params)

    query = f"""\
        SELECT {READ_PARAMS}
          FROM stats
         WHERE id = :id
           AND mode = :mode
    """
    params = {
        "id": player_id,
        "mode": mode,
    }
    rec = await app.state.services.database.fetch_one(query, params)
    return rec


# TODO: delete?
