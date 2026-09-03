<script lang="ts">
	type PitchStat = {
		pitch_name: string;
		count: number;
		avg_speed: number;
		pct: number;
	};

	let { pitches }: { pitches: PitchStat[] } = $props();
</script>

<div class="card bg-base-100 shadow-sm">
	<div class="card-body gap-4">
		<div>
			<h3 class="card-title text-base">
				Pitch Mix
			</h3>

			<p class="text-sm text-base-content/60">
				Usage and average velocity by pitch type.
			</p>
		</div>

		<div class="space-y-4">
			{#each pitches as pitch (pitch.pitch_name)}
				<div class="space-y-2">
					<div class="flex items-center justify-between gap-4">
						<div>
							<div class="font-medium">
								{pitch.pitch_name}
							</div>

							<div class="text-xs text-base-content/50">
								{pitch.count} pitches ·
								{pitch.avg_speed.toFixed(1)} mph
							</div>
						</div>

						<div class="font-mono text-sm font-semibold">
							{pitch.pct}%
						</div>
					</div>

					<progress
						class="progress progress-primary w-full"
						value={pitch.pct}
						max="100"
					></progress>
				</div>
			{/each}
		</div>

		<div class="divider my-1"></div>

		<div class="overflow-x-auto">
			<table class="table table-sm">
				<thead>
					<tr>
						<th>Pitch</th>
						<th class="text-right">Count</th>
						<th class="text-right">Avg. Velocity</th>
						<th class="text-right">Usage</th>
					</tr>
				</thead>

				<tbody>
					{#each pitches as pitch (pitch.pitch_name)}
						<tr>
							<td class="font-medium">
								{pitch.pitch_name}
							</td>

							<td class="text-right">
								{pitch.count}
							</td>

							<td class="text-right tabular-nums">
								{pitch.avg_speed.toFixed(1)} mph
							</td>

							<td class="text-right tabular-nums">
								{pitch.pct}%
							</td>
						</tr>
					{/each}
				</tbody>
			</table>
		</div>
	</div>
</div>