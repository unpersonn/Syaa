from tortoise import fields, models

class UserStats(models.Model):
    """Model to store user game statistics."""
    
    # Composite primary key simulation: We will use ID as PK but enforce uniqueness on guild_id + user_id
    id = fields.IntField(pk=True)
    guild_id = fields.BigIntField()
    user_id = fields.BigIntField()
    
    # RPS Stats
    rps_wins = fields.IntField(default=0)
    rps_losses = fields.IntField(default=0)
    
    # Hangman Stats
    hangman_wins = fields.IntField(default=0)
    hangman_losses = fields.IntField(default=0)

    class Meta:
        table = "user_stats"
        unique_together = (("guild_id", "user_id"),)

    def __str__(self):
        return f"UserStats(user={self.user_id}, guild={self.guild_id})"
