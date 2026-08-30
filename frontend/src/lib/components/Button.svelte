<script lang="ts">
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
    primary: 'bg-blue-600 hover:bg-blue-700 text-white',
    success: 'bg-green-600 hover:bg-green-700 text-white',
    secondary: 'bg-gray-200 hover:bg-gray-300 text-gray-800',
  };
</script>

<button
  {onclick}
  {disabled}
  class="{variants[variant]} px-4 py-2 rounded font-medium disabled:opacity-50"
>
  {@render children()}
</button>