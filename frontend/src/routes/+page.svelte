<script lang="ts">
	import { listGames, getGameSummary } from '$lib/api.js';

	import PitcherSearch from '$lib/components/PitcherSearch.svelte';
	import GameList from '$lib/components/GameList.svelte';
	import GameDetails from '$lib/components/GameDetails.svelte';
	import TrendAnalysis from '$lib/components/TrendAnalysis.svelte';
	import ErrorAlert from '$lib/components/ErrorAlert.svelte';
	import type { GameSummary } from '$lib/types/pitcher';

	type Game = {
		game_pk: number;
		game_date: string;
		opponent: string;
		decision: string;
	};

	type View = 'games' | 'details' | 'trends';
	type LoadingState = null | 'games' | 'details' | 'trends';

	let currentPitcherId = $state<number | null>(null);
	let currentPitcherName = $state<string | null>(null);

	let currentStartDate = $state('');
	let currentEndDate = $state('');

	let games = $state<Game[]>([]);
	let gameSummary = $state<GameSummary | null>(null);
	let trendSummaries = $state<GameSummary[]>([]);

	let view = $state<View>('games');
	let loading = $state<LoadingState>(null);
	let error = $state<string | null>(null);

	function resetForNewSearch() {
		currentPitcherId = null;
		currentPitcherName = null;

		currentStartDate = '';
		currentEndDate = '';

		games = [];
		gameSummary = null;
		trendSummaries = [];

		view = 'games';
		loading = null;
		error = null;
	}

	async function loadGames(
		pitcherId: number,
		pitcherName: string,
		startDate: string,
		endDate: string
	) {
		currentPitcherId = pitcherId;
		currentPitcherName = pitcherName;

		currentStartDate = startDate;
		currentEndDate = endDate;

		games = [];
		gameSummary = null;
		trendSummaries = [];

		view = 'games';
		error = null;
		loading = 'games';

		try {
			games = await listGames(pitcherId, startDate, endDate);

			if (games.length === 0) {
				error = 'No games found for the selected period.';
			}
		} catch (e) {
			error = e instanceof Error ? e.message : 'Failed to load games.';
		} finally {
			loading = null;
		}
	}

	async function viewGame(gamePk: number) {
		if (currentPitcherId === null) return;

		loading = 'details';
		error = null;

		try {
			gameSummary = await getGameSummary(
				currentPitcherId,
				gamePk,
				currentStartDate,
				currentEndDate
			);

			trendSummaries = [];
			view = 'details';
		} catch (e) {
			error = e instanceof Error ? e.message : 'Failed to load game details.';
		} finally {
			loading = null;
		}
	}

	async function analyzeTrends(gamePks: number[]) {
		if (currentPitcherId === null) return;

		loading = 'trends';
		error = null;
		trendSummaries = [];

		try {
			const summaries: GameSummary[] = [];
			const batchSize = 4;

			for (let index = 0; index < gamePks.length; index += batchSize) {
				const batch = gamePks.slice(index, index + batchSize);

				const results = await Promise.all(
					batch.map((gamePk) =>
						getGameSummary(currentPitcherId!, gamePk, currentStartDate, currentEndDate)
					)
				);

				summaries.push(...results);
			}

			trendSummaries = summaries;
			gameSummary = null;
			view = 'trends';
		} catch (e) {
			error = e instanceof Error ? e.message : 'Failed to load trend data.';
		} finally {
			loading = null;
		}
	}

	function backToGames() {
		gameSummary = null;
		trendSummaries = [];

		view = 'games';
		error = null;
	}
</script>

<svelte:head>
	<title>Pitcher Watch – MLB Pitcher Analytics & Pitch Trends</title>

	<meta
		name="description"
		content="Analyze MLB pitchers game by game. Explore pitch mix, velocity, workload, strikeouts, hits, earned runs and performance trends."
	/>

	<meta property="og:title" content="Pitcher Watch – MLB Pitcher Analytics & Pitch Trends" />

	<meta
		property="og:description"
		content="Analyze MLB pitchers game by game. Explore pitch mix, velocity, workload and performance trends."
	/>

	<meta property="og:type" content="website" />

	<meta property="og:url" content="https://pitcher.watch/" />
</svelte:head>

<header class="navbar border-b border-base-300 bg-base-100">
	<div class="mx-auto w-full max-w-7xl px-4 md:px-6">
		<div class="navbar-start">
			<span class="text-xl font-bold">Pitcher Stats</span>
		</div>
	</div>
</header>

<main class="mx-auto max-w-7xl space-y-6 p-4 md:p-6">
	<div>
		<h1 class="text-3xl font-bold tracking-tight">MLB Pitcher Analysis</h1>

		<p class="mt-1 text-base-content/60">
			Analyze pitching performance, pitch mix and game trends.
		</p>
	</div>

	<PitcherSearch onFindGames={loadGames} onNewSearch={resetForNewSearch} />

	<ErrorAlert message={error} />

	{#if currentPitcherName && currentStartDate && currentEndDate}
		<div class="flex flex-wrap items-center gap-2">
			<span class="badge badge-lg badge-primary">
				{currentPitcherName}
			</span>

			<span class="text-sm text-base-content/60">
				{currentStartDate} – {currentEndDate}
			</span>
		</div>
	{/if}

	{#if loading}
		<div class="flex min-h-48 flex-col items-center justify-center gap-3">
			<span class="loading loading-lg loading-spinner"></span>

			<div class="text-center" role="status" aria-live="polite">
				{#if loading === 'games'}
					<p class="font-medium">Loading games…</p>

					<p class="mt-1 text-sm text-base-content/50">
						Larger date ranges may take a little while.
					</p>
				{:else if loading === 'details'}
					<p class="font-medium">Loading game details…</p>

					<p class="mt-1 text-sm text-base-content/50">Fetching pitch data for this game.</p>
				{:else if loading === 'trends'}
					<p class="font-medium">Analyzing trends…</p>

					<p class="mt-1 text-sm text-base-content/50">
						Loading pitch data for the selected games. This may take a little while.
					</p>
				{/if}
			</div>
		</div>
	{:else if view === 'games' && games.length > 0}
		{#key `${currentPitcherId}-${currentStartDate}-${currentEndDate}`}
			<GameList {games} onViewGame={viewGame} onAnalyzeTrends={analyzeTrends} />
		{/key}
	{:else if view === 'details' && gameSummary}
		<div class="space-y-4">
			<button class="btn btn-ghost" onclick={backToGames}> ← Back to Games </button>

			<GameDetails summary={gameSummary} pitcherName={currentPitcherName ?? ''} />
		</div>
	{:else if view === 'trends' && trendSummaries.length > 0}
		<div class="space-y-4">
			<button class="btn btn-ghost" onclick={backToGames}> ← Back to Games </button>

			<TrendAnalysis summaries={trendSummaries} pitcherName={currentPitcherName ?? ''} />
		</div>
	{/if}
</main>
