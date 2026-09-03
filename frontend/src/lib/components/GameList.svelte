<script lang="ts">
	type Game = {
		game_pk: number;
		game_date: string;
		opponent: string;
		decision: string;
	};

	type Props = {
		games: Game[];
		onViewGame: (gamePk: number) => void;
		onAnalyzeTrends: (gamePks: number[]) => void;
	};

	let {
		games,
		onViewGame,
		onAnalyzeTrends
	}: Props = $props();

	let selectedGamePks = $state<number[]>([]);

	let selectedCount = $derived(selectedGamePks.length);

	function isSelected(gamePk: number) {
		return selectedGamePks.includes(gamePk);
	}

	function toggleGame(gamePk: number) {
		if (isSelected(gamePk)) {
			selectedGamePks = selectedGamePks.filter(
				(pk) => pk !== gamePk
			);
		} else {
			selectedGamePks = [
				...selectedGamePks,
				gamePk
			];
		}
	}

	function selectAll() {
		selectedGamePks = games.map(
			(game) => game.game_pk
		);
	}

	function selectNone() {
		selectedGamePks = [];
	}

	function resultBadge(decision: string) {
		if (decision === 'W') return 'badge-success';
		if (decision === 'L') return 'badge-error';

		return 'badge-neutral';
	}
</script>

<div class="card bg-base-200 shadow-sm">
	<div class="card-body p-0">
		<div
			class="flex flex-wrap items-center justify-between gap-4 p-6 pb-3"
		>
			<div>
				<h2 class="card-title">Games</h2>

				<p class="text-sm text-base-content/60">
					{games.length}
					{games.length === 1 ? ' game' : ' games'}
					available
				</p>
			</div>

			<div class="flex items-center gap-3">
				<span class="badge badge-neutral">
					{selectedCount} selected
				</span>

				<div class="join">
					<button
						class="btn btn-sm join-item"
						onclick={selectAll}
						disabled={games.length === 0}
					>
						All
					</button>

					<button
						class="btn btn-sm join-item"
						onclick={selectNone}
						disabled={selectedCount === 0}
					>
						None
					</button>
				</div>
			</div>
		</div>

		<div class="overflow-x-auto">
			<table class="table table-zebra">
				<thead>
					<tr>
						<th class="w-12"></th>
						<th>Date</th>
						<th>Opponent</th>
						<th>Result</th>
					</tr>
				</thead>

				<tbody>
					{#each games as game (game.game_pk)}
						<tr
							class="hover cursor-pointer"
							onclick={() =>
								toggleGame(game.game_pk)}
						>
							<td>
								<input
									type="checkbox"
									class="checkbox checkbox-primary checkbox-sm"
									checked={isSelected(game.game_pk)}
									onclick={(event) =>
										event.stopPropagation()}
									onchange={() =>
										toggleGame(game.game_pk)}
								/>
							</td>

							<td>
								{game.game_date}
							</td>

							<td class="font-medium">
								{game.opponent}
							</td>

							<td>
								<span
									class={`badge ${resultBadge(
										game.decision
									)}`}
								>
									{game.decision}
								</span>
							</td>
						</tr>
					{/each}
				</tbody>
			</table>
		</div>

		<div
			class="flex flex-col gap-4 border-t border-base-300 p-6 sm:flex-row sm:items-center sm:justify-between"
		>
			<div class="text-sm text-base-content/60">
				{#if selectedCount === 0}
					Select games to continue
				{:else if selectedCount === 1}
					1 game selected
				{:else}
					{selectedCount} games selected
				{/if}
			</div>

			<div class="flex flex-col gap-2 sm:flex-row">
				<button
					class="btn btn-primary"
					disabled={selectedCount !== 1}
					onclick={() =>
						onViewGame(selectedGamePks[0])}
				>
					View Game Details
				</button>

				<button
					class="btn btn-secondary"
					disabled={selectedCount < 2}
					onclick={() =>
						onAnalyzeTrends(selectedGamePks)}
				>
					Analyze Trends
				</button>
			</div>
		</div>
	</div>
</div>