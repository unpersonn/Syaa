"""Simple storage layer for game stats using SQLite."""

from __future__ import annotations

import asyncio
import sqlite3
from pathlib import Path
from typing import List, Tuple

DB_PATH = Path(__file__).with_name("rps_stats.sqlite3")


def init_db() -> None:
    """Initialise the database if it doesn't exist."""
    with sqlite3.connect(DB_PATH) as conn:
        # RPS statistics table
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS rps_stats (
                guild_id INTEGER,
                user_id INTEGER,
                wins INTEGER DEFAULT 0,
                losses INTEGER DEFAULT 0,
                PRIMARY KEY (guild_id, user_id)
            )
            """
        )

        # Hangman statistics table
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS hangman_stats (
                guild_id INTEGER,
                user_id INTEGER,
                wins INTEGER DEFAULT 0,
                losses INTEGER DEFAULT 0,
                PRIMARY KEY (guild_id, user_id)
            )
            """
        )

        conn.commit()


def record_win(guild_id: int, user_id: int) -> None:
    """Record a win for the given user."""
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            INSERT INTO rps_stats (guild_id, user_id, wins, losses)
            VALUES (?, ?, 1, 0)
            ON CONFLICT(guild_id, user_id)
            DO UPDATE SET wins = wins + 1
            """,
            (guild_id, user_id),
        )
        conn.commit()


def record_loss(guild_id: int, user_id: int) -> None:
    """Record a loss for the given user."""
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            INSERT INTO rps_stats (guild_id, user_id, wins, losses)
            VALUES (?, ?, 0, 1)
            ON CONFLICT(guild_id, user_id)
            DO UPDATE SET losses = losses + 1
            """,
            (guild_id, user_id),
        )
        conn.commit()


def get_user_stats(guild_id: int, user_id: int) -> Tuple[int, int]:
    """Return wins and losses for ``user_id`` in ``guild_id``."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.execute(
            "SELECT wins, losses FROM rps_stats WHERE guild_id = ? AND user_id = ?",
            (guild_id, user_id),
        )
        row = cursor.fetchone()
        return (row[0], row[1]) if row else (0, 0)


def get_leaderboard(guild_id: int, limit: int = 10) -> List[Tuple[int, int, int]]:
    """Return the top players in ``guild_id``."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.execute(
            """
            SELECT user_id, wins, losses
            FROM rps_stats
            WHERE guild_id = ?
            ORDER BY wins DESC, losses ASC
            LIMIT ?
            """,
            (guild_id, limit),
        )
        return cursor.fetchall()


async def record_hangman_win(guild_id: int, user_id: int) -> None:
    """Record a Hangman win for the given user without blocking."""

    def task() -> None:
        with sqlite3.connect(DB_PATH) as conn:
            conn.execute(
                """
                INSERT INTO hangman_stats (guild_id, user_id, wins, losses)
                VALUES (?, ?, 1, 0)
                ON CONFLICT(guild_id, user_id)
                DO UPDATE SET wins = wins + 1
                """,
                (guild_id, user_id),
            )
            conn.commit()

    await asyncio.to_thread(task)


async def record_hangman_loss(guild_id: int, user_id: int) -> None:
    """Record a Hangman loss for the given user without blocking."""

    def task() -> None:
        with sqlite3.connect(DB_PATH) as conn:
            conn.execute(
                """
                INSERT INTO hangman_stats (guild_id, user_id, wins, losses)
                VALUES (?, ?, 0, 1)
                ON CONFLICT(guild_id, user_id)
                DO UPDATE SET losses = losses + 1
                """,
                (guild_id, user_id),
            )
            conn.commit()

    await asyncio.to_thread(task)


async def get_hangman_user_stats(guild_id: int, user_id: int) -> Tuple[int, int]:
    """Return Hangman wins and losses for ``user_id`` in ``guild_id`` without blocking."""

    def task() -> Tuple[int, int]:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.execute(
                "SELECT wins, losses FROM hangman_stats WHERE guild_id = ? AND user_id = ?",
                (guild_id, user_id),
            )
            row = cursor.fetchone()
            return (row[0], row[1]) if row else (0, 0)

    return await asyncio.to_thread(task)


async def get_hangman_leaderboard(
    guild_id: int, limit: int = 10
) -> List[Tuple[int, int, int]]:
    """Return the top Hangman players in ``guild_id`` without blocking."""

    def task() -> List[Tuple[int, int, int]]:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.execute(
                """
                SELECT user_id, wins, losses
                FROM hangman_stats
                WHERE guild_id = ?
                ORDER BY wins DESC, losses ASC
                LIMIT ?
                """,
                (guild_id, limit),
            )
            return cursor.fetchall()

    return await asyncio.to_thread(task)


# Ensure database exists when module is imported
init_db()
