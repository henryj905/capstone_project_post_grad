def dict(stat):
    dict = {}
    if stat == "PASSING":
        dict = {
            "passing_yards": "sum",
            "completions": "sum",
            "attempts": "sum",
            "passing_tds": "sum",
            "interceptions": "sum",
            "passer_rating": "mean"  # average passer rating
        }
    elif stat == "RUSHING":
        dict = {
            "carries": "sum",
            "rushing_yards": "sum",
            "rushing_tds": "sum",
            "rushing_fumbles": "sum",
            "efficiency": "mean"
        }
    elif stat == "RECEIVING":
        dict = {
            "receptions": "sum",
            "targets": "sum",
            "receiving_yards": "sum",
            "receiving_tds": "sum",
        }
    elif stat == "SACKS":
        dict = {
            "sacks": "sum",
            "sack_yards": "sum",
            "sack_fumbles": "sum",
        }
    return dict