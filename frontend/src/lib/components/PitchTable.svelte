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

  const decisionBadge: Record<string, string> = {
    W: 'badge-success',
    L: 'badge-error',
    ND: 'badge-neutral',
  };
</script>

<div class="card bg-base-100 shadow-sm">
  <div class="card-body gap-3">
    <h3 class="card-title text-base">
      {summary.game_date} — {summary.opponent}
      <span class="badge {decisionBadge[summary.decision] ?? 'badge-neutral'}">
        {summary.decision}
      </span>
    </h3>

    <div class="stats stats-horizontal shadow-none bg-base-200">
      <div class="stat py-2 px-4">
        <div class="stat-title text-xs">IP</div>
        <div class="stat-value text-lg">{summary.innings_pitched}</div>
      </div>
      <div class="stat py-2 px-4">
        <div class="stat-title text-xs">ERA</div>
        <div class="stat-value text-lg">{summary.era}</div>
      </div>
      <div class="stat py-2 px-4">
        <div class="stat-title text-xs">K</div>
        <div class="stat-value text-lg">{summary.strikeouts}</div>
      </div>
      <div class="stat py-2 px-4">
        <div class="stat-title text-xs">Pitches</div>
        <div class="stat-value text-lg">{summary.total_pitches}</div>
      </div>
    </div>

    <div class="overflow-x-auto">
      <table class="table table-zebra table-sm">
        <thead>
          <tr>
            <th>Pitch</th>
            <th>Anzahl</th>
            <th>Ø Speed</th>
            <th>%</th>
          </tr>
        </thead>
        <tbody>
          {#each summary.pitch_stats as p (p.pitch_name)}
            <tr>
              <td>{p.pitch_name}</td>
              <td>{p.count}</td>
              <td>{p.avg_speed.toFixed(1)}</td>
              <td>{p.pct}%</td>
            </tr>
          {/each}
        </tbody>
      </table>
    </div>
  </div>
</div>