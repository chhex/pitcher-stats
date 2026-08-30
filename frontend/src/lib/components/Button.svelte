<script lang="ts">
  import type { Snippet } from 'svelte';

  let {
    variant = 'primary',
    disabled = false,
    onclick,
    children
  }: {
    variant?: 'primary' | 'success';
    disabled?: boolean;
    onclick: () => void;
    children: Snippet;
  } = $props();

  const variants = {
    primary: 'bg-blue-600 hover:bg-blue-700',
    success: 'bg-green-600 hover:bg-green-700',
  };
</script>

<button
  {onclick}
  {disabled}
  class="{variants[variant]} text-white px-4 py-2 rounded font-medium disabled:opacity-50"
>
  {@render children()}
</button>