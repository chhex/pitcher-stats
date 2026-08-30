<script lang="ts">
	import type { Snippet } from "svelte";

  let {
    variant = 'primary',
    disabled = false,
    onclick,
    children
  }: {
    variant?: 'primary' | 'success' | 'secondary';
    disabled?: boolean;
    onclick: () => void;
    children: Snippet;
  } = $props();

 const variants = {
  primary: 'btn-primary',
  success: 'btn-success',
  secondary: 'btn-secondary',
};
</script>

<button
  {onclick}
  {disabled}
  class=" btn {variants[variant]}"
>
  {@render children()}
</button>