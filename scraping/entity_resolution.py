"""
Entity resolution utilities for player matching across Understat, LaLiga.com and FotMob
"""
import unicodedata
import re
from difflib import SequenceMatcher

_punct_re = re.compile(r"[^a-z0-9\s]")

def normalize_name(name: str) -> str:
    if not name:
        return ""
    # NFKD decomposition to strip accents
    nfkd = unicodedata.normalize('NFKD', name)
    ascii_bytes = nfkd.encode('ascii', 'ignore')
    ascii_str = ascii_bytes.decode('ascii')
    # lowercase
    ascii_str = ascii_str.lower()
    # remove punctuation
    ascii_str = _punct_re.sub('', ascii_str)
    # collapse whitespace
    ascii_str = re.sub(r'\s+', ' ', ascii_str).strip()
    return ascii_str

def match_score(name_a: str, name_b: str) -> float:
    na = normalize_name(name_a)
    nb = normalize_name(name_b)
    if not na or not nb:
        return 0.0
    return SequenceMatcher(None, na, nb).ratio()

def normalize_team(team: str) -> str:
    return normalize_name(team)

def match_player(player_a: dict, candidates: list, team_a_field: str = 'team', team_b_field: str = 'team', name_a_field: str = 'player_name', name_b_field: str = 'player_name', threshold: float = 0.85):
    """
    Try to match player_a against candidates.
    Returns the best matching candidate dict or None.
    """
    name_a = player_a.get(name_a_field, '') or ''
    team_a_raw = player_a.get(team_a_field, '') or ''
    norm_name_a = normalize_name(name_a)
    norm_team_a = normalize_team(team_a_raw)

    # First pass: exact normalized name + team
    for cand in candidates:
        name_b = cand.get(name_b_field, '') or ''
        team_b_raw = cand.get(team_b_field, '') or ''
        if normalize_name(name_b) == norm_name_a and normalize_team(team_b_raw) == norm_team_a:
            return cand, 1.0

    # Second pass: fuzzy match within same team or similar team
    best_cand = None
    best_score = 0.0
    best_team_score = 0.0

    for cand in candidates:
        name_b = cand.get(name_b_field, '') or ''
        team_b_raw = cand.get(team_b_field, '') or ''
        norm_name_b = normalize_name(name_b)
        norm_team_b = normalize_team(team_b_raw)

        name_sim = SequenceMatcher(None, norm_name_a, norm_name_b).ratio()
        team_sim = SequenceMatcher(None, norm_team_a, norm_team_b).ratio()

        # Require team similarity at least 0.8 to consider
        if team_sim < 0.8:
            continue

        # Combined score weighted toward name
        score = 0.8 * name_sim + 0.2 * team_sim

        if score > best_score:
            best_score = score
            best_cand = cand
            best_team_score = team_sim

    if best_cand and best_score >= threshold:
        return best_cand, best_score
    return None, 0.0
