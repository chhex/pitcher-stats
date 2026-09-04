export async function searchPitchers(name) {
  const res = await fetch(`/api/pitchers/search?name=${encodeURIComponent(name)}`);
  if (!res.ok) throw new Error(`Search failed: ${res.status}`);
  return res.json();
}

export async function listGames(pitcherId, start, end) {
  const params = new URLSearchParams({ start, end });
  const res = await fetch(`/api/pitchers/${pitcherId}/games?${params}`);
  if (!res.ok) throw new Error(`Games fetch failed: ${res.status}`);
  return res.json();
}

export async function getGameSummary(pitcherId, gamePk, start, end) {
  const params = new URLSearchParams({ start, end });
  const res = await fetch(`/api/pitchers/${pitcherId}/games/${gamePk}?${params}`);
  if (!res.ok) throw new Error(`Game summary fetch failed: ${res.status}`);
  return res.json();
}