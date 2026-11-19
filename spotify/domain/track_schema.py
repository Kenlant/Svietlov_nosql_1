class TrackSchema:
    BOOL_COLUMNS = ("explicit",)
    INT_COLUMNS = ("popularity", "duration_ms", "key", "mode", "time_signature")
    FLOAT_COLUMNS = (
        "danceability",
        "energy",
        "loudness",
        "speechiness",
        "acousticness",
        "instrumentalness",
        "liveness",
        "valence",
        "tempo",
    )
    REQUIRED_COLUMNS = ("artists", "track_name")
