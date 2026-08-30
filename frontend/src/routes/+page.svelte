<script lang="ts">
	import { searchPitchers, listGames, getGameSummary } from '$lib/api.js';
	import { SvelteSet } from 'svelte/reactivity';
	import Button from '$lib/components/Button.svelte';
	import TextInput from '$lib/components/TextInput.svelte';
	import Checkbox from '$lib/components/Checkbox.svelte';
	import ErrorMessage from '$lib/components/ErrorMessage.svelte';
	import PitchTable from '$lib/components/PitchTable.svelte';
	import Modal from '$lib/components/Modal.svelte';

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
		decision: string;
	};

	let name = $state('');
	let matches = $state<Pitcher[]>([]);
	let selectedPitcherId = $state<number | null>(null);
	let selectedPitcherName = $state<string | null>(null);
	let startDate = $state('2026-01-01');
	let endDate = $state('2026-12-31');
	let games = $state<Game[]>([]);
	let selectedGamePks = new SvelteSet<number>();
	let summaries = $state<GameSummary[]>([]);
	let loading = $state(false);
	let error = $state<string | null>(null);

	let searchModalOpen = $state(false);

	function openSearchModal() {
		// Alte Ergebnisse zurücksetzen, da eine neue Suche gestartet wird
		matches = [];
		selectedPitcherId = null;
		selectedPitcherName = null;
		games = [];
		selectedGamePks.clear();
		summaries = [];
		error = null;
		searchModalOpen = true;
	}

	async function doSearch() {
		error = null;
		try {
			matches = await searchPitchers(name);
		} catch (e) {
			error = e.message;
		}
	}

	function selectPitcher(m: Pitcher) {
		selectedPitcherId = m.key_mlbam;
		selectedPitcherName = m.full_name;
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
			if (games.length === 0) {
				error = 'Keine Spiele im Zeitraum gefunden';
			} else {
				searchModalOpen = false;
			}
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
		for (const g of games) selectedGamePks.add(g.game_pk);
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
</script>

<header class="navbar bg-base-100 shadow-sm">
	<div class="navbar-start">
		<span class="text-xl font-bold">Pitcher Stats</span>
	</div>
</header>

<main class="mx-auto max-w-3xl space-y-6 p-6">
	<ErrorMessage message={error} />

	<div class="flex items-center gap-3">
		<Button onclick={openSearchModal}>Pitcher & Zeitraum wählen</Button>
		{#if selectedPitcherName}
			<span class="badge badge-lg">{selectedPitcherName} · {startDate} bis {endDate}</span>
		{/if}
	</div>

{#if games.length > 0}
  <fieldset class="fieldset rounded-box border border-base-300 bg-base-200 p-4">
    <legend class="fieldset-legend">Spiele</legend>

    <div class="mb-2 flex justify-end gap-2">
      <Button variant="secondary" onclick={selectAllGames}>Alle</Button>
      <Button variant="secondary" onclick={selectNoGames}>Keine</Button>
    </div>

    <div class="overflow-x-auto">
      <table class="table table-zebra table-sm">
        <thead>
          <tr>
            <th class="w-8"></th>
            <th>Datum</th>
            <th>Gegner</th>
            <th>Resultat</th>
          </tr>
        </thead>
        <tbody>
          {#each games as g (g.game_pk)}
            <tr class="hover cursor-pointer" onclick={() => toggleGame(g.game_pk)}>
              <th>
                <input
                  type="checkbox"
                  class="checkbox checkbox-sm"
                  checked={selectedGamePks.has(g.game_pk)}
                  onclick={(e) => e.stopPropagation()}
                  onchange={() => toggleGame(g.game_pk)}
                />
              </th>
              <td>{g.game_date}</td>
              <td>{g.opponent}</td>
              <td>
                <span
                  class="badge {g.decision === 'W'
                    ? 'badge-success'
                    : g.decision === 'L'
                      ? 'badge-error'
                      : 'badge-neutral'}"
                >
                  {g.decision}
                </span>
              </td>
            </tr>
          {/each}
        </tbody>
      </table>
    </div>

    <Button variant="success" onclick={showSelected} disabled={loading}>Anzeigen</Button>
  </fieldset>
{/if}

	{#each summaries as s (s.game_date + s.opponent)}
		<PitchTable summary={s} />
	{/each}
</main>

<Modal bind:open={searchModalOpen} title="Pitcher & Zeitraum">
  <div class="space-y-4">
    <div class="join">
      <TextInput bind:value={name} placeholder="Pitcher Name" joinItem />
      <Button onclick={doSearch} joinItem>Suchen</Button>
    </div>

    {#if matches.length > 0}
      <select
        value={selectedPitcherId}
        onchange={(e) => {
          const id = Number(e.currentTarget.value);
          const m = matches.find((m) => m.key_mlbam === id);
          if (m) selectPitcher(m);
        }}
        class="select select-bordered w-full"
      >
        <option value={null} disabled selected>Pitcher wählen</option>
        {#each matches as m (m.key_mlbam)}
          <option value={m.key_mlbam}>{m.full_name}</option>
        {/each}
      </select>
    {/if}

    <div class="join">
      <TextInput type="date" bind:value={startDate} joinItem />
      <TextInput type="date" bind:value={endDate} joinItem />
    </div>

    <Button onclick={loadGames} disabled={loading || !selectedPitcherId}>Spiele laden</Button>
  </div>
</Modal>
