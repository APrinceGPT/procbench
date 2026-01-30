<script lang="ts">
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { analysisStore, analysisResult, hasAnalysis } from '$lib/stores/analysis';
	import { api } from '$lib/api/client';
	import type { ProcessTreeNode } from '$lib/api/types';
	import { getRiskLevel } from '$lib/api/types';

	let tree: ProcessTreeNode[] = [];
	let loading = true;
	let expandedNodes = new Set<number>();

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
		expandedNodes = expandedNodes; // Trigger reactivity
	}

	function getRiskColorClass(score: number): string {
		if (score >= 50) return 'border-red-500 bg-red-50 dark:bg-red-900/20';
		if (score >= 20) return 'border-orange-500 bg-orange-50 dark:bg-orange-900/20';
		if (score > 0) return 'border-yellow-500 bg-yellow-50 dark:bg-yellow-900/20';
		return 'border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800';
	}
</script>

<div class="p-6">
	<div class="mb-6">
		<h1 class="text-2xl font-bold text-gray-900 dark:text-white">
			Process Tree
		</h1>
		<p class="text-gray-600 dark:text-gray-400">
			Hierarchical view of process relationships
		</p>
	</div>

	{#if loading}
		<div class="flex items-center justify-center py-12">
			<svg class="animate-spin w-8 h-8 text-blue-600" fill="none" viewBox="0 0 24 24">
				<circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
				<path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
			</svg>
		</div>
	{:else if tree.length === 0}
		<div class="text-center py-12 text-gray-500">
			No process tree data available
		</div>
	{:else}
		<div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm p-4 overflow-x-auto">
			<div class="min-w-max">
				{#each tree.slice(0, 50) as node}
					{@const hasChildren = node.children && node.children.length > 0}
					{@const isExpanded = expandedNodes.has(node.process.pid)}
					
					<div class="mb-2" style="margin-left: {node.depth * 24}px">
						<div 
							class="flex items-center gap-2 p-3 rounded-lg border-l-4 {getRiskColorClass(node.process.risk_score)}"
						>
							{#if hasChildren}
								<button
									class="p-1 hover:bg-gray-200 dark:hover:bg-gray-700 rounded"
									on:click={() => toggleNode(node.process.pid)}
								>
									<svg 
										class="w-4 h-4 text-gray-500 transition-transform {isExpanded ? 'rotate-90' : ''}"
										fill="none" 
										viewBox="0 0 24 24" 
										stroke="currentColor"
									>
										<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
									</svg>
								</button>
							{:else}
								<span class="w-6"></span>
							{/if}

							<div class="flex-1">
								<div class="flex items-center gap-2">
									<span class="font-medium text-gray-900 dark:text-white">
										{node.process.process_name}
									</span>
									<span class="text-xs text-gray-500">
										PID: {node.process.pid}
									</span>
								</div>
								{#if node.process.image_path}
									<p class="text-sm text-gray-500 dark:text-gray-400 truncate max-w-lg">
										{node.process.image_path}
									</p>
								{/if}
							</div>

							<div class="flex items-center gap-2">
								{#each node.process.behavior_tags as tag}
									<span class="px-2 py-0.5 text-xs rounded bg-purple-100 dark:bg-purple-900 text-purple-700 dark:text-purple-300">
										{tag}
									</span>
								{/each}

								{#if node.process.risk_score > 0}
									<span 
										class="px-2 py-1 text-sm font-bold rounded
											   {node.process.risk_score >= 50 ? 'bg-red-100 text-red-700' : 
											    node.process.risk_score >= 20 ? 'bg-orange-100 text-orange-700' : 
											    'bg-yellow-100 text-yellow-700'}"
									>
										{node.process.risk_score}
									</span>
								{/if}
							</div>
						</div>

						<!-- Children would be rendered here in a full implementation -->
					</div>
				{/each}

				{#if tree.length > 50}
					<p class="text-center py-4 text-gray-500">
						Showing 50 of {tree.length} processes. Use filters to narrow results.
					</p>
				{/if}
			</div>
		</div>
	{/if}
</div>
