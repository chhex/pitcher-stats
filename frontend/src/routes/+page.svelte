<script lang="ts">
	import { searchPitchers, listGames, getGameSummary } from '$lib/api.js';
	import { SvelteSet } from 'svelte/reactivity';
	import Button from '$lib/components/Button.svelte';
	import TextInput from '$lib/components/TextInput.svelte';
	import Checkbox from '$lib/components/Checkbox.svelte';
	import ErrorMessage from '$lib/components/ErrorMessage.svelte';
	import PitchTable from '$lib/components/PitchTable.svelte';

	type GameSummary = {
		game_date: string;
		opponent: string;
		decision: string;
		innings_pitched: string;
		era: string;
		strikeouts: number;
		total_pitches: number;
		pitch_stats: Array<{
			pitch_name: string;
			count: number;
			avg_speed: number;
			pct: number;
		}>;
	};

	type Pitcher = {
		key_mlbam: number;
		full_name: string;
	};

	type Game = {
		game_pk: number;
		game_date: string;
		opponent: string;
	};

	let name = $state('');
	let matches = $state<Pitcher[]>([]);
	let selectedPitcherId = $state<number | null>(null);
	let startDate = $state('2026-01-01');
	let endDate = $state('2026-12-31');
	let games = $state<Game[]>([]);
	// svelte-ignore non_reactive_update
	let selectedGamePks = new SvelteSet<number>();
	let summaries = $state<GameSummary[]>([]);
	let loading = $state(false);
	let error = $state<string | null>(null);

	async function doSearch() {
		error = null;
		try {
			matches = await searchPitchers(name);
		} catch (e) {
			error = e.message;
		}
	}

	async function loadGames() {
		if (!selectedPitcherId) {
			error = 'Bitte zuerst Pitcher auswählen';
			return;
		}
		loading = true;
		error = null;
		try {
			games = await listGames(selectedPitcherId, startDate, endDate);
			if (games.length === 0) error = 'Keine Spiele im Zeitraum gefunden';
		} catch (e) {
			error = e.message;
		} finally {
			loading = false;
		}
	}

	function toggleGame(gamePk: number) {
		if (selectedGamePks.has(gamePk)) {
			selectedGamePks.delete(gamePk);
		} else {
			selectedGamePks.add(gamePk);
		}
	}

	function selectAllGames() {
		selectedGamePks.clear();
		for (const g of games) {
			selectedGamePks.add(g.game_pk);
		}
	}

	function selectNoGames() {
		selectedGamePks.clear();
	}

	async function showSelected() {
		if (selectedGamePks.size === 0) {
			error = 'Keine Spiele ausgewählt';
			return;
		}
		loading = true;
		error = null;
		try {
			summaries = await Promise.all(
				[...selectedGamePks].map((pk) => getGameSummary(selectedPitcherId, pk, startDate, endDate))
			);
		} catch (e) {
			error = e.message;
		} finally {
			loading = false;
		}
	}

	function clearAll() {
		name = '';
		matches = [];
		selectedPitcherId = null;
		games = [];
		selectedGamePks.clear(); // statt: selectedGamePks = new SvelteSet();
		summaries = [];
		error = null;
	}
</script>

<main class="mx-auto max-w-3xl space-y-8 p-6 text-gray-900">
	<div class="flex items-center justify-between">
		<h1 class="text-3xl font-bold">Pitcher Stats</h1>
		<Button variant="secondary" onclick={clearAll}>Zurücksetzen</Button>
	</div>

	<ErrorMessage message={error} />

	<section class="flex flex-wrap items-center gap-2">
		<TextInput bind:value={name} placeholder="Pitcher Name" disabled={games.length > 0} />
		<Button onclick={doSearch} disabled={games.length > 0}>Suchen</Button>

		{#if matches.length > 0}
			<select
				bind:value={selectedPitcherId}
				disabled={games.length > 0}
				class="rounded border border-gray-300 px-3 py-2 disabled:bg-gray-100 disabled:opacity-50"
			>
				<option value={null} disabled selected>Pitcher wählen</option>
				{#each matches as m (m.key_mlbam)}
					<option value={m.key_mlbam}>{m.full_name}</option>
				{/each}
			</select>
		{/if}
	</section>

	<section class="flex flex-wrap items-center gap-2">
		<TextInput
			type="date"
			bind:value={startDate}
			disabled={!selectedPitcherId || games.length > 0}
		/>
		<TextInput type="date" bind:value={endDate} disabled={!selectedPitcherId || games.length > 0} />
		<Button onclick={loadGames} disabled={loading || !selectedPitcherId || games.length > 0}>
			Spiele laden
		</Button>
	</section>

	{#if games.length > 0}
		<section class="space-y-2">
			<div class="flex items-center justify-between">
				<h2 class="text-lg font-semibold">Spiele</h2>
				<div class="flex gap-2">
					<Button variant="secondary" onclick={selectAllGames}>Alle</Button>
					<Button variant="secondary" onclick={selectNoGames}>Keine</Button>
				</div>
			</div>
			{#each games as g (g.game_pk)}
				<Checkbox checked={selectedGamePks.has(g.game_pk)} onchange={() => toggleGame(g.game_pk)}>
					{g.game_date} — {g.opponent}
				</Checkbox>
			{/each}
			<Button variant="success" onclick={showSelected} disabled={loading}>Anzeigen</Button>
		</section>
	{/if}

	{#each summaries as s (s.game_date + s.opponent)}
		<PitchTable summary={s} />
	{/each}
</main>
