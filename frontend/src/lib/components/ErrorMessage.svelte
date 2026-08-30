<script lang="ts">
  let { message }: { message: string | null } = $props();
</script>

{#if message}
  <p class="text-red-600 bg-red-50 border border-red-200 rounded px-3 py-2">{message}</p>
{/if}