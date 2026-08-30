<script lang="ts">
  let {
    value = $bindable(),
    type = 'text',
    placeholder = ''
  }: {
    value: string;
    type?: 'text' | 'date';
    placeholder?: string;
  } = $props();
</script>

<input
  {type}
  bind:value
  {placeholder}
  autocomplete="off"
  data-lpignore="true"
  data-1p-ignore
  class="border border-gray-300 rounded px-3 py-2"
/>