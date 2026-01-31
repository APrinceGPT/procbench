<script lang="ts">
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { analysisStore, analysisResult, hasAnalysis } from '$lib/stores/analysis';
	import { api } from '$lib/api/client';
	import type { ProcessTreeNode } from '$lib/api/types';
	import { getRiskLevel } from '$lib/api/types';

	let tree: ProcessTreeNode[] = $state([]);
	let loading = $state(true);
	let expandedNodes = $state(new Set<number>());

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
		} finally {
			loading = false;
		}
	});

	function toggleNode(pid: number) {
		if (expandedNodes.has(pid)) {
			expandedNodes.delete(pid);
		} else {
			expandedNodes.add(pid);
		}
		expandedNodes = new Set(expandedNodes); // Trigger reactivity
	}

	function getRiskBorderColor(score: number): string {
		if (score >= 50) return '#ef4444';
		if (score >= 20) return '#f97316';
		if (score > 0) return '#eab308';
		return '#374151';
	}

	function getRiskBgColor(score: number): string {
		if (score >= 50) return 'rgba(239, 68, 68, 0.1)';
		if (score >= 20) return 'rgba(249, 115, 22, 0.1)';
		if (score > 0) return 'rgba(234, 179, 8, 0.1)';
		return '#1f2937';
	}
</script>

<div style="padding: 1.5rem;">
	<div style="margin-bottom: 1.5rem;">
		<h1 style="font-size: 1.5rem; font-weight: bold; color: white; margin: 0;">
			Process Tree
		</h1>
		<p style="color: #9ca3af; margin: 0.25rem 0 0 0;">
			Hierarchical view of process relationships
		</p>
	</div>

	{#if loading}
		<div style="display: flex; align-items: center; justify-content: center; padding: 3rem 0;">
			<svg style="width: 32px; height: 32px; color: #3b82f6; animation: spin 1s linear infinite;" fill="none" viewBox="0 0 24 24">
				<circle style="opacity: 0.25;" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
				<path style="opacity: 0.75;" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
			</svg>
		</div>
	{:else if tree.length === 0}
		<div style="text-align: center; padding: 3rem 0; color: #6b7280;">
			No process tree data available
		</div>
	{:else}
		<div style="background-color: #1f2937; border-radius: 0.75rem; padding: 1rem; overflow-x: auto;">
			<div style="min-width: max-content;">
				{#each tree.slice(0, 50) as node}
					{@const hasChildren = node.children && node.children.length > 0}
					{@const isExpanded = expandedNodes.has(node.process.pid)}
					
					<div style="margin-bottom: 0.5rem; margin-left: {node.depth * 24}px;">
						<div 
							style="display: flex; align-items: center; gap: 0.5rem; padding: 0.75rem; border-radius: 0.5rem; border-left: 4px solid {getRiskBorderColor(node.process.risk_score)}; background-color: {getRiskBgColor(node.process.risk_score)};"
						>
							{#if hasChildren}
								<button
									style="padding: 0.25rem; background: none; border: none; cursor: pointer; border-radius: 4px;"
									onclick={() => toggleNode(node.process.pid)}
									aria-label="{isExpanded ? 'Collapse' : 'Expand'} {node.process.process_name} child processes"
								>
									<svg 
										style="width: 16px; height: 16px; color: #9ca3af; transition: transform 0.2s; transform: rotate({isExpanded ? '90deg' : '0deg'});"
										fill="none" 
										viewBox="0 0 24 24" 
										stroke="currentColor"
									>
										<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
									</svg>
								</button>
							{:else}
								<span style="width: 24px;"></span>
							{/if}

							<div style="flex: 1;">
								<div style="display: flex; align-items: center; gap: 0.5rem;">
									<span style="font-weight: 500; color: white;">
										{node.process.process_name}
									</span>
									<span style="font-size: 0.75rem; color: #9ca3af;">
										PID: {node.process.pid}
									</span>
								</div>
								{#if node.process.image_path}
									<p style="font-size: 0.875rem; color: #9ca3af; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; max-width: 32rem; margin: 0;">
										{node.process.image_path}
									</p>
								{/if}
							</div>

							<div style="display: flex; align-items: center; gap: 0.5rem;">
								{#each node.process.behavior_tags as tag}
									<span style="padding: 0.125rem 0.5rem; font-size: 0.75rem; border-radius: 4px; background-color: rgba(168, 85, 247, 0.2); color: #c084fc;">
										{tag}
									</span>
								{/each}

								{#if node.process.risk_score > 0}
									<span 
										style="padding: 0.25rem 0.5rem; font-size: 0.875rem; font-weight: bold; border-radius: 4px;
											   color: {node.process.risk_score >= 50 ? '#ef4444' : node.process.risk_score >= 20 ? '#f97316' : '#eab308'};
											   background-color: {node.process.risk_score >= 50 ? 'rgba(239, 68, 68, 0.2)' : node.process.risk_score >= 20 ? 'rgba(249, 115, 22, 0.2)' : 'rgba(234, 179, 8, 0.2)'};"
									>
										{node.process.risk_score}
									</span>
								{/if}
							</div>
						</div>
					</div>
				{/each}

				{#if tree.length > 50}
					<p style="text-align: center; padding: 1rem 0; color: #6b7280; margin: 0;">
						Showing 50 of {tree.length} processes. Use filters to narrow results.
					</p>
				{/if}
			</div>
		</div>
	{/if}
</div>

<style>
	@keyframes spin {
		from { transform: rotate(0deg); }
		to { transform: rotate(360deg); }
	}
</style>
