import adapter from '@sveltejs/adapter-static';
import { vitePreprocess } from '@sveltejs/vite-plugin-svelte';

export default {
	preprocess: vitePreprocess(),
	kit: {
		adapter: adapter({
			// Fallback für Client-Side-Routing (wichtig für SPAs)
			fallback: 'index.html'
		})
	}
};
