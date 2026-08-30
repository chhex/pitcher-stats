<script lang="ts">
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

  let { summary }: { summary: GameSummary } = $props();
</script>

<section class="border-t border-gray-200 pt-4 space-y-2">
  <h3 class="text-lg font-semibold">
    {summary.game_date} — {summary.opponent}
    <span class="text-sm font-normal text-gray-500">({summary.decision})</span>
  </h3>
  <p class="text-sm text-gray-600">
    IP: {summary.innings_pitched} · ERA: {summary.era} ·
    K: {summary.strikeouts} · Pitches: {summary.total_pitches}
  </p>
  <table class="w-full text-sm border-collapse">
    <thead>
      <tr class="border-b border-gray-300 text-left">
        <th class="py-1 pr-4">Pitch</th>
        <th class="py-1 pr-4">Anzahl</th>
        <th class="py-1 pr-4">Ø Speed</th>
        <th class="py-1">%</th>
      </tr>
    </thead>
    <tbody>
      {#each summary.pitch_stats as p (p.pitch_name)}
        <tr class="border-b border-gray-100">
          <td class="py-1 pr-4">{p.pitch_name}</td>
          <td class="py-1 pr-4">{p.count}</td>
          <td class="py-1 pr-4">{p.avg_speed.toFixed(1)}</td>
          <td class="py-1">{p.pct}%</td>
        </tr>
      {/each}
    </tbody>
  </table>
</section>