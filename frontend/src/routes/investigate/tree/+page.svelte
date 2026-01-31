<script lang="ts">
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { analysisResult, hasAnalysis } from '$lib/stores/analysis';
	import { api } from '$lib/api/client';
	import type { ProcessTreeNode } from '$lib/api/types';
	import ProcessGraph from '$lib/components/visualization/ProcessGraph.svelte';
	import ProcessDetailsPanel from '$lib/components/visualization/ProcessDetailsPanel.svelte';
	import type { VisNode } from '$lib/components/visualization/graph-utils';

	// ==========================================================================
	// STATE
	// ==========================================================================

	let tree: ProcessTreeNode[] = $state([]);
	let loading = $state(true);
	let error = $state<string | null>(null);
	let selectedNode = $state<VisNode | null>(null);
	let isPanelCollapsed = $state(false);

	// ==========================================================================
	// LIFECYCLE
	// ==========================================================================

	onMount(async () => {
		if (!$hasAnalysis || !$analysisResult) {
			goto('/');
			return;
		}

		try {
			const response = await api.getProcessTree($analysisResult.analysis_id);
			tree = response.tree;
		} catch (e) {
			console.error('Failed to load process tree:', e);
			error = 'Failed to load process tree data';
		} finally {
			loading = false;
		}
	});

	// ==========================================================================
	// EVENT HANDLERS
	// ==========================================================================

	function handleNodeSelect(node: VisNode | null): void {
		selectedNode = node;
		if (node && isPanelCollapsed) {
			isPanelCollapsed = false;
		}
	}

	function handlePanelClose(): void {
		selectedNode = null;
	}

	function togglePanel(): void {
		isPanelCollapsed = !isPanelCollapsed;
	}
</script>

<!-- ========================================================================== -->
<!-- TEMPLATE -->
<!-- ========================================================================== -->

<div class="tree-page">
	<!-- Header -->
	<header class="page-header">
		<div class="header-content">
			<div class="header-icon">
				<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
					<circle cx="12" cy="12" r="3"></circle>
					<path d="M12 2v4m0 12v4M4.93 4.93l2.83 2.83m8.48 8.48l2.83 2.83M2 12h4m12 0h4M4.93 19.07l2.83-2.83m8.48-8.48l2.83-2.83"></path>
				</svg>
			</div>
			<div>
				<h1 class="page-title">Process Graph</h1>
				<p class="page-subtitle">Interactive visualization of process relationships</p>
			</div>
		</div>

		<div class="header-actions">
			{#if selectedNode}
				<button class="toggle-panel-btn" onclick={togglePanel}>
					<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
						{#if isPanelCollapsed}
							<path d="M15 18l-6-6 6-6"></path>
						{:else}
							<path d="M9 18l6-6-6-6"></path>
						{/if}
					</svg>
					{isPanelCollapsed ? 'Show' : 'Hide'} Details
				</button>
			{/if}
		</div>
	</header>

	<!-- Main Content -->
	<div class="main-content">
		{#if loading}
			<div class="loading-state">
				<div class="loading-spinner"></div>
				<p>Loading process tree...</p>
			</div>
		{:else if error}
			<div class="error-state">
				<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
					<circle cx="12" cy="12" r="10"></circle>
					<line x1="12" y1="8" x2="12" y2="12"></line>
					<line x1="12" y1="16" x2="12.01" y2="16"></line>
				</svg>
				<p>{error}</p>
				<button class="retry-btn" onclick={() => location.reload()}>
					Retry
				</button>
			</div>
		{:else if tree.length === 0}
			<div class="empty-state">
				<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
					<circle cx="12" cy="12" r="3"></circle>
					<path d="M12 2v4m0 12v4M4.93 4.93l2.83 2.83m8.48 8.48l2.83 2.83M2 12h4m12 0h4M4.93 19.07l2.83-2.83m8.48-8.48l2.83-2.83"></path>
				</svg>
				<h2>No Process Data</h2>
				<p>No process tree data is available for this analysis.</p>
			</div>
		{:else}
			<div class="graph-layout" class:panel-collapsed={isPanelCollapsed}>
				<div class="graph-section">
					<ProcessGraph {tree} onNodeSelect={handleNodeSelect} />
				</div>

				{#if !isPanelCollapsed}
					<aside class="details-section">
						<ProcessDetailsPanel node={selectedNode} onClose={handlePanelClose} />
					</aside>
				{/if}
			</div>
		{/if}
	</div>
</div>

<!-- ========================================================================== -->
<!-- STYLES -->
<!-- ========================================================================== -->

<style>
	.tree-page {
		display: flex;
		flex-direction: column;
		height: 100%;
		min-height: calc(100vh - 64px);
		padding: 24px;
		gap: 20px;
	}

	.page-header {
		display: flex;
		justify-content: space-between;
		align-items: center;
		flex-wrap: wrap;
		gap: 16px;
	}

	.header-content {
		display: flex;
		align-items: center;
		gap: 16px;
	}

	.header-icon {
		display: flex;
		align-items: center;
		justify-content: center;
		width: 48px;
		height: 48px;
		background: linear-gradient(135deg, rgba(59, 130, 246, 0.2), rgba(139, 92, 246, 0.2));
		border-radius: 12px;
		border: 1px solid rgba(59, 130, 246, 0.3);
	}

	.header-icon svg {
		width: 24px;
		height: 24px;
		color: #3b82f6;
	}

	.page-title {
		margin: 0;
		font-size: 1.5rem;
		font-weight: 600;
		color: white;
	}

	.page-subtitle {
		margin: 4px 0 0 0;
		font-size: 0.875rem;
		color: rgba(255, 255, 255, 0.5);
	}

	.header-actions {
		display: flex;
		gap: 12px;
	}

	.toggle-panel-btn {
		display: flex;
		align-items: center;
		gap: 8px;
		padding: 8px 16px;
		background: rgba(255, 255, 255, 0.05);
		border: 1px solid rgba(255, 255, 255, 0.1);
		border-radius: 8px;
		color: rgba(255, 255, 255, 0.8);
		font-size: 13px;
		font-weight: 500;
		cursor: pointer;
		transition: all 0.2s ease;
	}

	.toggle-panel-btn:hover {
		background: rgba(255, 255, 255, 0.1);
		color: white;
	}

	.toggle-panel-btn svg {
		width: 16px;
		height: 16px;
	}

	.main-content {
		flex: 1;
		display: flex;
		flex-direction: column;
		min-height: 0;
	}

	.graph-layout {
		flex: 1;
		display: grid;
		grid-template-columns: 1fr 320px;
		gap: 20px;
		min-height: 500px;
	}

	.graph-layout.panel-collapsed {
		grid-template-columns: 1fr;
	}

	.graph-section {
		min-height: 500px;
	}

	.details-section {
		min-height: 500px;
	}

	/* Loading State */
	.loading-state {
		flex: 1;
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		gap: 16px;
		color: rgba(255, 255, 255, 0.6);
	}

	.loading-spinner {
		width: 48px;
		height: 48px;
		border: 3px solid rgba(255, 255, 255, 0.1);
		border-top-color: #3b82f6;
		border-radius: 50%;
		animation: spin 1s linear infinite;
	}

	@keyframes spin {
		to { transform: rotate(360deg); }
	}

	/* Error State */
	.error-state {
		flex: 1;
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		gap: 16px;
		padding: 48px;
	}

	.error-state svg {
		width: 64px;
		height: 64px;
		color: #ef4444;
		opacity: 0.6;
	}

	.error-state p {
		margin: 0;
		font-size: 1rem;
		color: rgba(255, 255, 255, 0.6);
	}

	.retry-btn {
		padding: 10px 24px;
		background: #3b82f6;
		border: none;
		border-radius: 8px;
		color: white;
		font-size: 14px;
		font-weight: 500;
		cursor: pointer;
		transition: background 0.2s ease;
	}

	.retry-btn:hover {
		background: #2563eb;
	}

	/* Empty State */
	.empty-state {
		flex: 1;
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		gap: 16px;
		padding: 48px;
	}

	.empty-state svg {
		width: 80px;
		height: 80px;
		color: rgba(255, 255, 255, 0.15);
	}

	.empty-state h2 {
		margin: 0;
		font-size: 1.25rem;
		font-weight: 600;
		color: rgba(255, 255, 255, 0.8);
	}

	.empty-state p {
		margin: 0;
		font-size: 0.875rem;
		color: rgba(255, 255, 255, 0.4);
	}

	/* Responsive */
	@media (max-width: 1024px) {
		.graph-layout {
			grid-template-columns: 1fr;
			grid-template-rows: 1fr auto;
		}

		.details-section {
			min-height: 300px;
		}
	}

	@media (max-width: 640px) {
		.tree-page {
			padding: 16px;
		}

		.header-content {
			flex-direction: column;
			align-items: flex-start;
			gap: 12px;
		}
	}
</style>
