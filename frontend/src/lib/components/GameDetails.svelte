<script lang="ts">
	import PitchMix from './PitchMix.svelte';

	type PitchStat = {
		pitch_name: string;
		count: number;
		avg_speed: number;
		pct: number;
	};

	type GameSummary = {
		game_date: string;
		opponent: string;
		decision: string;
		innings_pitched: string;
		era: string;
		strikeouts: number;
		total_pitches: number;
		pitch_stats: PitchStat[];
	};

	let {
		summary,
		pitcherName
	}: {
		summary: GameSummary;
		pitcherName: string;
	} = $props();

	const decisionBadge: Record<string, string> = {
		W: 'badge-success',
		L: 'badge-error',
		ND: 'badge-neutral'
	};
</script>

<div class="space-y-6">
	<div class="card bg-base-200 shadow-sm">
		<div class="card-body gap-5">
			<div
				class="flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between"
			>
				<div>
					<div class="flex flex-wrap items-center gap-3">
						<h2 class="card-title text-2xl">
							{pitcherName}
						</h2>

						<span
							class="badge {decisionBadge[summary.decision] ??
								'badge-neutral'}"
						>
							{summary.decision}
						</span>
					</div>

					<p class="mt-1 text-base-content/60">
						{summary.game_date}
						· vs {summary.opponent}
					</p>
				</div>
			</div>

			<div
				class="stats stats-vertical bg-base-100 shadow-none sm:stats-horizontal"
			>
				<div class="stat">
					<div class="stat-title">
						Innings
					</div>

					<div class="stat-value text-2xl">
						{summary.innings_pitched}
					</div>
				</div>

				<div class="stat">
					<div class="stat-title">
						ERA
					</div>

					<div class="stat-value text-2xl">
						{summary.era}
					</div>
				</div>

				<div class="stat">
					<div class="stat-title">
						Strikeouts
					</div>

					<div class="stat-value text-2xl">
						{summary.strikeouts}
					</div>
				</div>

				<div class="stat">
					<div class="stat-title">
						Total Pitches
					</div>

					<div class="stat-value text-2xl">
						{summary.total_pitches}
					</div>
				</div>
			</div>
		</div>
	</div>

	<PitchMix pitches={summary.pitch_stats} />
</div>