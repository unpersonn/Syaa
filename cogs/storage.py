"""Database storage layer using Tortoise-ORM."""

from __future__ import annotations

from typing import List, Tuple

from database.models import UserStats


# ----------------------------------------------------------------------
# RPS Logic
# ----------------------------------------------------------------------

async def record_win(guild_id: int, user_id: int) -> None:
    """Record a win for the given user (async)."""
    stats, _ = await UserStats.get_or_create(guild_id=guild_id, user_id=user_id)
    stats.rps_wins += 1
    await stats.save()


async def record_loss(guild_id: int, user_id: int) -> None:
    """Record a loss for the given user (async)."""
    stats, _ = await UserStats.get_or_create(guild_id=guild_id, user_id=user_id)
    stats.rps_losses += 1
    await stats.save()


def get_user_stats(guild_id: int, user_id: int) -> Tuple[int, int]:
    """Return wins and losses for ``user_id`` in ``guild_id``.
    
    Note: Since this is called from synchronous code in the current Fun cog,
    we would ideally update the Cog to be fully async. However, for now,
    the Cog methods are async so we can await proper DB calls if we refactor them.
    
    Wait! The Fun cog calls these synchronously in the original code? 
    Let's check Fun.py. It was: `wins, losses = get_user_stats(...)`
    The original get_user_stats used sqlite3 synchronously.
    
    Since we are now using async ORM, we MUST update Fun.py to await these calls.
    For this file, we will define them as `async def`.
    """
    raise NotImplementedError("This function is deprecated. Use `get_user_stats_async`.")


async def get_user_stats_async(guild_id: int, user_id: int) -> Tuple[int, int]:
    """Async version of get_user_stats."""
    stats = await UserStats.get_or_none(guild_id=guild_id, user_id=user_id)
    if not stats:
        return 0, 0
    return stats.rps_wins, stats.rps_losses


def get_leaderboard(guild_id: int, limit: int = 10) -> List[Tuple[int, int, int]]:
    """Deprecated synchronous leaderboard."""
    raise NotImplementedError("Use `get_leaderboard_async`.")


async def get_leaderboard_async(guild_id: int, limit: int = 10) -> List[Tuple[int, int, int]]:
    """Return the top rps players in ``guild_id``."""
    stats = await UserStats.filter(guild_id=guild_id).order_by("-rps_wins", "rps_losses").limit(limit)
    return [(s.user_id, s.rps_wins, s.rps_losses) for s in stats]


# ----------------------------------------------------------------------
# Hangman Logic
# ----------------------------------------------------------------------

async def record_hangman_win(guild_id: int, user_id: int) -> None:
    stats, _ = await UserStats.get_or_create(guild_id=guild_id, user_id=user_id)
    stats.hangman_wins += 1
    await stats.save()


async def record_hangman_loss(guild_id: int, user_id: int) -> None:
    stats, _ = await UserStats.get_or_create(guild_id=guild_id, user_id=user_id)
    stats.hangman_losses += 1
    await stats.save()


async def get_hangman_user_stats(guild_id: int, user_id: int) -> Tuple[int, int]:
    stats = await UserStats.get_or_none(guild_id=guild_id, user_id=user_id)
    if not stats:
        return 0, 0
    return stats.hangman_wins, stats.hangman_losses


async def get_hangman_leaderboard(guild_id: int, limit: int = 10) -> List[Tuple[int, int, int]]:
    stats = await UserStats.filter(guild_id=guild_id).order_by("-hangman_wins", "hangman_losses").limit(limit)
    return [(s.user_id, s.hangman_wins, s.hangman_losses) for s in stats]
