<script lang="ts">
	import { listGames, getGameSummary } from '$lib/api';

	import PitcherSearch from '$lib/components/PitcherSearch.svelte';
	import GameList from '$lib/components/GameList.svelte';
	import ErrorAlert from '$lib/components/ErrorAlert.svelte';
	import GameDetails from '$lib/components/GameDetails.svelte';
	import TrendAnalysis from '$lib/components/TrendAnalysis.svelte';

	type Game = {
		game_pk: number;
		game_date: string;
		opponent: string;
		result: string;
		decision: string;
	};

	type GameSummary = {
		game_date: string;
		opponent: string;
		result: string;
		innings_pitched: number;
		era: number;
		strikeouts: number;
		pitches: number;
		pitch_mix: {
			pitch_type: string;
			count: number;
			avg_speed: number;
			percentage: number;
		}[];
	};

	let pitcherId = $state<number | null>(null);
	let pitcherName = $state('');

	let startDate = $state('');
	let endDate = $state('');

	let games = $state<Game[]>([]);
	let selectedGameSummary = $state<GameSummary | null>(null);
	let trendGamePks = $state<number[]>([]);

	let loading = $state(false);
	let error = $state('');

	let view = $state<'games' | 'details' | 'trends'>('games');

	function startNewPitcherSearch() {
		pitcherId = null;
		pitcherName = '';

		startDate = '';
		endDate = '';

		games = [];
		selectedGameSummary = null;
		trendGamePks = [];
		trendSummaries = [];

		view = 'games';
		error = '';
	}

	async function loadGames(id: number, name: string, start: string, end: string) {
		/*
		 * Nicht startNewPitcherSearch() aufrufen:
		 * wir wollen die gerade gewählte neue Auswahl
		 * jetzt in den Seiten-State übernehmen.
		 */

		pitcherId = id;
		pitcherName = name;

		startDate = start;
		endDate = end;

		games = [];
		selectedGameSummary = null;
		trendGamePks = [];

		view = 'games';
		error = '';
		loading = true;

		try {
			games = await listGames(id, start, end);

			if (games.length === 0) {
				error = 'No games found for the selected period.';
			}
		} catch (e) {
			error = e instanceof Error ? e.message : 'Failed to load games.';
		} finally {
			loading = false;
		}
	}

	async function viewGame(gamePk: number) {
		if (pitcherId === null) return;

		loading = true;
		error = '';

		try {
			selectedGameSummary = await getGameSummary(pitcherId, gamePk, startDate, endDate);

			view = 'details';
		} catch (e) {
			error = e instanceof Error ? e.message : 'Fehler beim Laden der Spieldetails.';
		} finally {
			loading = false;
		}
	}

	let trendSummaries = $state<GameSummary[]>([]);

	async function analyzeTrends(gamePks: number[]) {
		if (pitcherId === null) return;

		loading = true;
		error = '';

		try {
			trendSummaries = await Promise.all(
				gamePks.map((gamePk) => getGameSummary(pitcherId!, gamePk, startDate, endDate))
			);

			view = 'trends';
		} catch (e) {
			error = e instanceof Error ? e.message : 'Failed to load trend data.';
		} finally {
			loading = false;
		}
	}

	function backToGames() {
		view = 'games';
		error = '';
	}
</script>

<svelte:head>
	<title>Pitcher Stats</title>
	<meta name="description" content="Analyze MLB pitcher performance and pitch data." />
</svelte:head>

<div class="mx-auto max-w-7xl space-y-6 p-4 md:p-6">
	<header>
		<h1 class="text-3xl font-bold tracking-tight">Pitcher Stats</h1>

		<p class="mt-1 text-base-content/60">
			Analyze pitching performance, pitch mix and game trends.
		</p>
	</header>

	<PitcherSearch onFindGames={loadGames} onNewSearch={startNewPitcherSearch} />

	{#if error}
		<ErrorAlert message={error} />
	{/if}

	{#if loading}
		<div class="flex justify-center py-12">
			<span class="loading loading-lg loading-spinner"></span>
		</div>
	{:else if view === 'games' && games.length > 0}
		{#key `${pitcherId}-${startDate}-${endDate}`}
			<GameList {games} onViewGame={viewGame} onAnalyzeTrends={analyzeTrends} />
		{/key}
	{:else if view === 'games' && pitcherId !== null && !error}
		<div class="alert">
			<span>
				No games found for {pitcherName} in the selected period.
			</span>
		</div>
	{/if}

	{#if view === 'details' && selectedGameSummary}
		<div class="space-y-4">
			<button class="btn btn-ghost" onclick={backToGames}> ← Back to Games </button>

			<GameDetails summary={selectedGameSummary} {pitcherName} />
		</div>
	{/if}

	{#if view === 'trends' && trendSummaries.length > 0}
		<div class="space-y-4">
			<button class="btn btn-ghost" onclick={backToGames}> ← Back to Games </button>

			<TrendAnalysis summaries={trendSummaries} {pitcherName} />
		</div>
	{/if}
</div>
