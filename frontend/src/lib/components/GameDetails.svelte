<script lang="ts">
	import type { GameSummary } from '$lib/types/pitcher';
	import PitchMix from './PitchMix.svelte';


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
			<div class="flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between">
				<div>
					<div class="flex flex-wrap items-center gap-3">
						<h2 class="card-title text-2xl">
							{pitcherName}
						</h2>

						<span class="badge {decisionBadge[summary.decision] ?? 'badge-neutral'}">
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
				class="stats stats-vertical bg-base-100 shadow-none
		sm:grid sm:grid-cols-3
		lg:grid-cols-6"
			>
				<div class="stat">
					<div class="stat-title">Innings</div>
					<div class="stat-value text-2xl">
						{summary.innings_pitched}
					</div>
				</div>

				<div class="stat">
					<div class="stat-title">Hits</div>
					<div class="stat-value text-2xl">
						{summary.hits}
					</div>
				</div>

				<div class="stat">
					<div class="stat-title">Earned Runs</div>
					<div class="stat-value text-2xl">
						{summary.earned_runs}
					</div>
				</div>

				<div class="stat">
					<div class="stat-title">Strikeouts</div>
					<div class="stat-value text-2xl">
						{summary.strikeouts}
					</div>
				</div>

				<div class="stat">
					<div class="stat-title">ERA</div>
					<div class="stat-value text-2xl">
						{summary.era}
					</div>
				</div>

				<div class="stat">
					<div class="stat-title">Total Pitches</div>
					<div class="stat-value text-2xl">
						{summary.total_pitches}
					</div>
				</div>
			</div>
		</div>
	</div>

	<PitchMix pitches={summary.pitch_stats} />
</div>
