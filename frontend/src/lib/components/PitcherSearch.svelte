<script lang="ts">
	import { searchPitchers } from '$lib/api.js';

	type Pitcher = {
		key_mlbam: number;
		full_name: string;
	};

	type Props = {
		onFindGames: (
			pitcherId: number,
			pitcherName: string,
			startDate: string,
			endDate: string
		) => void;
		onNewSearch: () => void;
	};

	let { onFindGames, onNewSearch }: Props = $props();

	let name = $state('');
	let matches = $state<Pitcher[]>([]);

	let selectedPitcherId = $state<number | null>(null);
	let selectedPitcherName = $state<string | null>(null);

	let startDate = $state('2026-01-01');
	let endDate = $state('2026-12-31');

	let searching = $state(false);
	let error = $state<string | null>(null);

	function resetPitcherSelection() {
		selectedPitcherId = null;
		selectedPitcherName = null;
	}

	async function search() {
		const query = name.trim();

		if (!query) return;

		/*
		 * Eine neue Pitchersuche startet einen komplett
		 * neuen Analyse-Workflow.
		 */
		onNewSearch();

		resetPitcherSelection();
		matches = [];
		error = null;
		searching = true;

		try {
			matches = await searchPitchers(query);

			/*
			 * Bei genau einem Treffer ist keine zusätzliche
			 * Dropdown-Auswahl nötig.
			 */
			if (matches.length === 1) {
				selectPitcher(matches[0]);
			}
		} catch (e) {
			error = e instanceof Error ? e.message : 'Pitcher search failed';
		} finally {
			searching = false;
		}
	}

	function selectPitcher(pitcher: Pitcher) {
		selectedPitcherId = pitcher.key_mlbam;
		selectedPitcherName = pitcher.full_name;
	}

	function findGames() {
		if (selectedPitcherId === null || selectedPitcherName === null) {
			return;
		}

		onFindGames(selectedPitcherId, selectedPitcherName, startDate, endDate);
	}
</script>

<div class="card bg-base-200 shadow-sm">
	<div class="card-body gap-5">
		<div>
			<h2 class="card-title">Analyze a Pitcher</h2>
			<p class="text-sm text-base-content/60">
				Search for a pitcher and choose the period you want to analyze.
			</p>
		</div>

		<fieldset class="fieldset">
			<legend class="fieldset-legend">Pitcher</legend>

			<div class="join w-full">
				<input
					class="input join-item w-full"
					placeholder="Search pitcher..."
					bind:value={name}
					onkeydown={(event) => {
						if (event.key === 'Enter') {
							search();
						}
					}}
				/>

				<button
					class="btn join-item btn-primary"
					onclick={search}
					disabled={searching || !name.trim()}
				>
					{#if searching}
						<div class="flex min-h-48 flex-col items-center justify-center gap-3">
							<span class="loading loading-lg loading-spinner"></span>

							<div class="text-center">
								<p class="font-medium">Loading games…</p>

								<p class="mt-1 text-sm text-base-content/50">
									Larger date ranges may take a little while.
								</p>
							</div>  
						</div>
					{:else}
						Search
					{/if}
				</button>
			</div>

			<p class="mt-2 text-xs text-base-content/50">
				You don't need to enter the full name. If multiple pitchers match, you can select the
				correct one from the results.
			</p>
		</fieldset>

		{#if matches.length > 1}
			<fieldset class="fieldset">
				<legend class="fieldset-legend"> Select pitcher </legend>

				<select
					class="select w-full"
					value={selectedPitcherId ?? ''}
					onchange={(event) => {
						const id = Number(event.currentTarget.value);

						const pitcher = matches.find((p) => p.key_mlbam === id);

						if (pitcher) {
							selectPitcher(pitcher);
						}
					}}
				>
					<option value="" disabled> Select a pitcher... </option>

					{#each matches as pitcher (pitcher.key_mlbam)}
						<option value={pitcher.key_mlbam}>
							{pitcher.full_name}
						</option>
					{/each}
				</select>
			</fieldset>
		{:else if !searching && matches.length === 0 && error === null && name.trim()}
			<!--
				Absichtlich nichts:
				Vor der ersten Suche soll hier kein
				"No pitchers found" erscheinen.
			-->
		{/if}

		{#if selectedPitcherName}
			<div class="flex items-center gap-3">
				<span class="text-sm text-base-content/60"> Selected pitcher </span>

				<span class="badge badge-lg badge-primary">
					{selectedPitcherName}
				</span>
			</div>
		{/if}

		<div class="divider my-0"></div>

		<fieldset class="fieldset">
			<legend class="fieldset-legend">Date range</legend>

			<div class="grid gap-4 sm:grid-cols-2">
				<label class="fieldset">
					<span class="fieldset-label">From</span>

					<input type="date" class="input w-full" bind:value={startDate} />
				</label>

				<label class="fieldset">
					<span class="fieldset-label">To</span>

					<input type="date" class="input w-full" bind:value={endDate} />
				</label>
			</div>
		</fieldset>

		{#if error}
			<div class="alert alert-error">
				<span>{error}</span>
			</div>
		{/if}

		<div class="card-actions justify-end">
			<button
				class="btn btn-primary"
				onclick={findGames}
				disabled={searching || selectedPitcherId === null || !startDate || !endDate}
			>
				Find Games
			</button>
		</div>
	</div>
</div>
