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
  class="input input-bordered"
/>