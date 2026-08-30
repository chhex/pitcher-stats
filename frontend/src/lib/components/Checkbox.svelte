<script lang="ts">
  import type { Snippet } from 'svelte';

  let {
    checked = false,
    onchange,
    children
  }: {
    checked?: boolean;
    onchange: () => void;
    children: Snippet;
  } = $props();
</script>

<label class="flex items-center gap-2 py-1">
  <input type="checkbox" {checked} {onchange} class="rounded border-gray-300" />
  <span>{@render children()}</span>
</label>    