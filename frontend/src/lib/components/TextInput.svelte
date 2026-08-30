<script lang="ts">
  let {
    value = $bindable(),
    type = 'text',
    placeholder = '',
    disabled = false
  }: {
    value: string;
    type?: 'text' | 'date';
    placeholder?: string;
    disabled?: boolean;
  } = $props();
</script>

<input
  {type}
  bind:value
  {placeholder}
  {disabled}
  autocomplete="off"
  data-lpignore="true"
  data-1p-ignore
  class="border border-gray-300 rounded px-3 py-2 disabled:opacity-50 disabled:bg-gray-100"
/>