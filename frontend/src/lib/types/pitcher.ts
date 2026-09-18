export type PitchStat = {
	pitch_name: string;
	count: number;
	avg_speed: number;
	pct: number;
};

export type GameSummary = {
	game_date: string;
	opponent: string;
	decision: string;
	innings_pitched: string;
	era: string;
	earned_runs: number;
	strikeouts: number;
	balls: number;
	strikes: number;
	hits: number;
	total_pitches: number;
	pitch_stats: PitchStat[];
};