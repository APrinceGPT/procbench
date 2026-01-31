<script lang="ts">
	import './layout.css';
	import Sidebar from '$lib/components/navigation/Sidebar.svelte';
	import { isSidebarOpen } from '$lib/stores/ui';
	import { colors, animation } from '$lib/styles/design-tokens';

	let { children } = $props();

	const mainContentMargin = $derived($isSidebarOpen ? '16rem' : '4rem');
</script>

<svelte:head>
	<title>ProcBench - Process Monitor Analysis</title>
	<meta name="description" content="AI-powered Process Monitor log analysis for SOC analysts" />
</svelte:head>

<div style="
	display: flex;
	min-height: 100vh;
	background: linear-gradient(135deg, {colors.background.primary} 0%, {colors.background.secondary} 50%, {colors.background.primary} 100%);
	background-attachment: fixed;
">
	<!-- Sidebar -->
	<Sidebar />

	<!-- Main Content Area -->
	<main style="
		flex: 1;
		margin-left: {mainContentMargin};
		transition: margin-left {animation.duration.normal} {animation.easing.easeInOut};
		min-height: 100vh;
	">
		{@render children()}
	</main>
</div>
