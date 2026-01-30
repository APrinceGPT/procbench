<script lang="ts">
	import './layout.css';
	import Sidebar from '$lib/components/navigation/Sidebar.svelte';
	import { isSidebarOpen } from '$lib/stores/ui';

	let { children } = $props();
</script>

<svelte:head>
	<title>ProcBench - Process Monitor Analysis</title>
	<meta name="description" content="AI-powered Process Monitor log analysis for SOC analysts" />
</svelte:head>

<div class="min-h-screen bg-gray-100 dark:bg-gray-900">
	<Sidebar />

	<main
		class="transition-all duration-300"
		style="margin-left: {$isSidebarOpen ? '16rem' : '4rem'}"
	>
		{@render children()}
	</main>
</div>
