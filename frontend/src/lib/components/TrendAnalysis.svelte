<script lang="ts">
	import LineChart from './LineChart.svelte';

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

	type ChartSeries = {
		name: string;
		values: Array<number | null>;
	};

	type Props = {
		summaries: GameSummary[];
		pitcherName: string;
	};

	let { summaries, pitcherName }: Props = $props();

	let sortedSummaries = $derived(
		[...summaries].sort((a, b) => new Date(a.game_date).getTime() - new Date(b.game_date).getTime())
	);

	let labels = $derived(sortedSummaries.map((summary) => summary.game_date));

	let pitchTypes = $derived.by(() => {
		// eslint-disable-next-line svelte/prefer-svelte-reactivity
		const names = new Set<string>();

		for (const summary of sortedSummaries) {
			for (const pitch of summary.pitch_stats) {
				names.add(pitch.pitch_name);
			}
		}

		return [...names];
	});

	let workloadSeries = $derived<ChartSeries[]>([
		{
			name: 'Total Pitches',
			values: sortedSummaries.map((summary) => summary.total_pitches)
		}
	]);

	let usageSeries = $derived.by((): ChartSeries[] => {
		return pitchTypes.map((pitchName) => ({
			name: pitchName,

			values: sortedSummaries.map((summary) => {
				const pitch = summary.pitch_stats.find((item) => item.pitch_name === pitchName);

				return pitch?.count ?? 0;
			})
		}));
	});

	let velocitySeries = $derived.by((): ChartSeries[] => {
		return pitchTypes.map((pitchName) => ({
			name: pitchName,

			values: sortedSummaries.map((summary) => {
				const pitch = summary.pitch_stats.find((item) => item.pitch_name === pitchName);

				return pitch?.avg_speed ?? null;
			})
		}));
	});

	let pitchesPerInningSeries = $derived<ChartSeries[]>([
		{
			name: 'Pitches / Inning',
			values: sortedSummaries.map((summary) => {
				const innings = inningsToNumber(summary.innings_pitched);

				return innings > 0 ? summary.total_pitches / innings : null;
			})
		}
	]);

	function inningsToNumber(value: string) {
		const [whole, fraction] = value.split('.');

		const innings = Number(whole);

		if (fraction === '1') return innings + 1 / 3;
		if (fraction === '2') return innings + 2 / 3;

		return innings;
	}
</script>

<div class="space-y-6">
	<div>
		<h2 class="text-2xl font-semibold">Trend Analysis</h2>

		<p class="mt-1 text-sm text-base-content/60">
			{pitcherName} · {summaries.length} selected games
		</p>
	</div>

	<!-- Workload -->
<div class="grid gap-6 lg:grid-cols-2">
	<!-- Pitch Count -->
	<div class="card bg-base-100 shadow-sm">
		<div class="card-body gap-4">
			<div>
				<h3 class="card-title">
					Pitch Count
				</h3>

				<p class="text-sm text-base-content/60">
					Total pitches thrown per game.
				</p>
			</div>

			<LineChart
				labels={labels}
				series={workloadSeries}
				yLabel="Pitches"
			/>
		</div>
	</div>

	<!-- Pitches / Inning -->
	<div class="card bg-base-100 shadow-sm">
		<div class="card-body gap-4">
			<div>
				<h3 class="card-title">
					Pitches / Inning
				</h3>

				<p class="text-sm text-base-content/60">
					Average number of pitches thrown per inning.
				</p>
			</div>

			<LineChart
				labels={labels}
				series={pitchesPerInningSeries}
				yLabel="Pitches / Inning"
			/>
		</div>
	</div>
</div>

	<!-- Pitch Usage -->

	<div class="card bg-base-100 shadow-sm">
		<div class="card-body gap-4">
			<div>
				<h3 class="card-title">Pitch Usage</h3>

				<p class="text-sm text-base-content/60">Number of pitches thrown by pitch type.</p>
			</div>

			<LineChart {labels} series={usageSeries} yLabel="Pitches" />
		</div>
	</div>

	<!-- Velocity -->

	<div class="card bg-base-100 shadow-sm">
		<div class="card-body gap-4">
			<div>
				<h3 class="card-title">Velocity</h3>

				<p class="text-sm text-base-content/60">Average velocity by pitch type.</p>
			</div>

			<LineChart {labels} series={velocitySeries} yLabel="Velocity" valueSuffix=" mph" />
		</div>
	</div>

	<!-- Exact data -->

	<div class="card bg-base-100 shadow-sm">
		<div class="card-body gap-4">
			<div>
				<h3 class="card-title">Game Data</h3>

				<p class="text-sm text-base-content/60">Values for the selected games.</p>
			</div>

			<div class="overflow-x-auto">
				<table class="table table-zebra table-sm">
					<thead>
						<tr>
							<th>Date</th>
							<th>Opponent</th>
							<th>Decision</th>
							<th class="text-right">IP</th>
							<th class="text-right">ERA</th>
							<th class="text-right">K</th>
							<th class="text-right">Pitches</th>
							<th class="text-right"> Pitches / Inning </th>
						</tr>
					</thead>

					<tbody>
						{#each sortedSummaries as summary}
							<tr>
								<td>{summary.game_date}</td>
								<td>{summary.opponent}</td>
								<td>{summary.decision}</td>

								<td class="text-right tabular-nums">
									{summary.innings_pitched}
								</td>

								<td class="text-right tabular-nums">
									{summary.era}
								</td>

								<td class="text-right tabular-nums">
									{summary.strikeouts}
								</td>

								<td class="text-right tabular-nums">
									{summary.total_pitches}
								</td>
								<td class="text-right tabular-nums">
									{(summary.total_pitches / inningsToNumber(summary.innings_pitched)).toFixed(1)}
								</td>
							</tr>
						{/each}
					</tbody>
				</table>
			</div>
		</div>
	</div>
</div>
