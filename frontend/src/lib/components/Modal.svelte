<script lang="ts">
  import type { Snippet } from 'svelte';

  let {
    open = $bindable(false),
    title,
    children
  }: {
    open?: boolean;
    title: string;
    children: Snippet;
  } = $props();

  let dialogEl: HTMLDialogElement;

  $effect(() => {
    if (!dialogEl) return;
    if (open) {
      dialogEl.showModal();
    } else {
      dialogEl.close();
    }
  });

  function handleClose() {
    open = false;
  }
</script>

<dialog bind:this={dialogEl} onclose={handleClose} class="modal">
  <div class="modal-box">
    <form method="dialog">
      <button class="btn btn-sm btn-circle btn-ghost absolute right-2 top-2">✕</button>
    </form>
    <h3 class="text-lg font-bold mb-4">{title}</h3>
    {@render children()}
  </div>
  <form method="dialog" class="modal-backdrop">
    <button>close</button>
  </form>
</dialog>