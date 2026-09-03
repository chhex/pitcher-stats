<script lang="ts">
	type Series = {
		name: string;
		values: Array<number | null>;
	};

	type Props = {
		labels: string[];
		series: Series[];
		yLabel?: string;
		valueSuffix?: string;
	};

	let { labels, series, yLabel = '', valueSuffix = '' }: Props = $props();

	const width = 800;
	const height = 320;

	const margin = {
		top: 20,
		right: 25,
		bottom: 85,
		left: 55
	};

	const plotWidth = width - margin.left - margin.right;
	const plotHeight = height - margin.top - margin.bottom;

	let allValues = $derived(
		series.flatMap((item) => item.values).filter((value): value is number => value !== null)
	);

	let maxValue = $derived(allValues.length > 0 ? Math.max(...allValues) : 0);

	let minValue = $derived(allValues.length > 0 ? Math.min(...allValues) : 0);

	let padding = $derived(Math.max((maxValue - minValue) * 0.15, 1));

	let yMin = $derived(Math.max(0, Math.floor(minValue - padding)));

	let yMax = $derived(Math.ceil(maxValue + padding));

	let yRange = $derived(Math.max(yMax - yMin, 1));

	let ticks = $derived(
		Array.from({ length: 5 }, (_, index) => {
			return yMin + (yRange * index) / 4;
		}).reverse()
	);

	function x(index: number) {
		if (labels.length <= 1) {
			return margin.left + plotWidth / 2;
		}

		return margin.left + (index / (labels.length - 1)) * plotWidth;
	}

	function y(value: number) {
		return margin.top + (1 - (value - yMin) / yRange) * plotHeight;
	}

	function path(values: Array<number | null>) {
		let result = '';
		let drawing = false;

		values.forEach((value, index) => {
			if (value === null) {
				drawing = false;
				return;
			}

			const command = drawing ? 'L' : 'M';

			result += `${command} ${x(index)} ${y(value)} `;
			drawing = true;
		});

		return result.trim();
	}

	function color(index: number) {
		return `hsl(${(index * 67) % 360} 65% 50%)`;
	}

	function formatDate(value: string) {
		const date = new Date(`${value}T00:00:00`);

		return new Intl.DateTimeFormat('en', {
			month: 'short',
			day: 'numeric'
		}).format(date);
	}
</script>

<div class="w-full">
	<div class="overflow-x-auto">
		<svg
			viewBox={`0 0 ${width} ${height}`}
			class="w-full"
			role="img"
			aria-label={yLabel}
		>
			<!-- horizontal grid + Y labels -->
			{#each ticks as tick}
				{@const tickY = y(tick)}

				<line
					x1={margin.left}
					y1={tickY}
					x2={width - margin.right}
					y2={tickY}
					stroke="currentColor"
					stroke-opacity="0.1"
				/>

				<text
					x={margin.left - 10}
					y={tickY + 4}
					text-anchor="end"
					class="fill-current text-[11px] opacity-50"
				>
					{tick.toFixed(0)}
				</text>
			{/each}

			<!-- X axis labels -->
			{#each labels as label, index}
				<text
					x={x(index)}
					y={height - 32}
					text-anchor="end"
					transform={`rotate(-55 ${x(index)} ${height - 32})`}
					class="fill-current text-[11px] opacity-50"
				>
					{formatDate(label)}
				</text>
			{/each}

			<!-- data -->
			{#each series as item, seriesIndex}
				<path
					d={path(item.values)}
					fill="none"
					stroke={color(seriesIndex)}
					stroke-width="2.5"
					stroke-linecap="round"
					stroke-linejoin="round"
				/>

				{#each item.values as value, index}
					{#if value !== null}
						<circle cx={x(index)} cy={y(value)} r="4" fill={color(seriesIndex)}>
							<title>
								{item.name}
								· {labels[index]}
								· {value.toFixed(1)}{valueSuffix}
							</title>
						</circle>
					{/if}
				{/each}
			{/each}
		</svg>
	</div>

	{#if series.length > 1}
		<div class="mt-3 flex flex-wrap gap-x-5 gap-y-2">
			{#each series as item, index}
				<div class="flex items-center gap-2 text-sm">
					<span class="h-2.5 w-2.5 rounded-full" style={`background-color: ${color(index)}`}></span>

					<span class="text-base-content/70">
						{item.name}
					</span>
				</div>
			{/each}
		</div>
	{/if}
</div>
