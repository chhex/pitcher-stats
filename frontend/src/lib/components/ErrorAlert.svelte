<script lang="ts">
	type Props = {
		message: string | null;
	};

	let { message }: Props = $props();
</script>

{#if message}
	<div class="alert alert-error">
		<span>{message}</span>
	</div>
{/if}