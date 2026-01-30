<script lang="ts">
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { analysisResult, hasAnalysis } from '$lib/stores/analysis';
	import { api } from '$lib/api/client';
	import type { TimelineEntry } from '$lib/api/types';

	let timeline: TimelineEntry[] = [];
	let loading = true;
	let showAnomaliesOnly = true;

	$: filteredTimeline = showAnomaliesOnly 
		? timeline.filter(e => e.is_anomaly)
		: timeline;

	onMount(async () => {
		if (!$hasAnalysis || !$analysisResult) {
			goto('/');
			return;
		}

		try {
			const response = await api.getTimeline($analysisResult.analysis_id, {
				anomaliesOnly: false,
				limit: 200
			});
			timeline = response.timeline;
		} catch (e) {
			console.error('Failed to load timeline:', e);
		} finally {
			loading = false;
		}
	});

	function getRiskColorClass(score: number): string {
		if (score >= 50) return 'bg-red-500';
		if (score >= 20) return 'bg-orange-500';
		if (score > 0) return 'bg-yellow-500';
		return 'bg-gray-400';
	}
</script>

<div class="p-6">
	<div class="flex items-center justify-between mb-6">
		<div>
			<h1 class="text-2xl font-bold text-gray-900 dark:text-white">
				Timeline
			</h1>
			<p class="text-gray-600 dark:text-gray-400">
				Chronological view of process activity by risk score
			</p>
		</div>

		<label class="flex items-center gap-2 cursor-pointer">
			<input
				type="checkbox"
				bind:checked={showAnomaliesOnly}
				class="w-4 h-4 rounded border-gray-300 text-blue-600 focus:ring-blue-500"
			/>
			<span class="text-sm text-gray-700 dark:text-gray-300">
				Show anomalies only
			</span>
		</label>
	</div>

	{#if loading}
		<div class="flex items-center justify-center py-12">
			<svg class="animate-spin w-8 h-8 text-blue-600" fill="none" viewBox="0 0 24 24">
				<circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
				<path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
			</svg>
		</div>
	{:else if filteredTimeline.length === 0}
		<div class="text-center py-12 text-gray-500">
			{showAnomaliesOnly ? 'No anomalies detected' : 'No timeline data available'}
		</div>
	{:else}
		<div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm p-6">
			<div class="relative">
				<!-- Timeline line -->
				<div class="absolute left-4 top-0 bottom-0 w-0.5 bg-gray-200 dark:bg-gray-700"></div>

				<div class="space-y-6">
					{#each filteredTimeline as entry, i}
						<div class="relative flex items-start gap-4 pl-10">
							<!-- Timeline dot -->
							<div 
								class="absolute left-2.5 w-3 h-3 rounded-full border-2 border-white dark:border-gray-800 {getRiskColorClass(entry.risk_score)}"
							></div>

							<!-- Content -->
							<div class="flex-1 bg-gray-50 dark:bg-gray-700/50 rounded-lg p-4">
								<div class="flex items-start justify-between">
									<div>
										<div class="flex items-center gap-2">
											<span class="font-medium text-gray-900 dark:text-white">
												{entry.process_name}
											</span>
											<span class="text-xs text-gray-500">
												PID: {entry.pid}
											</span>
											{#if entry.is_anomaly}
												<span class="px-2 py-0.5 text-xs rounded bg-red-100 dark:bg-red-900 text-red-700 dark:text-red-300">
													Anomaly
												</span>
											{/if}
										</div>
										<p class="mt-1 text-sm text-gray-600 dark:text-gray-400">
											{entry.description}
										</p>
									</div>

									<div class="flex flex-col items-end gap-1">
										<span 
											class="px-2 py-1 text-sm font-bold rounded
												   {entry.risk_score >= 50 ? 'bg-red-100 text-red-700' : 
												    entry.risk_score >= 20 ? 'bg-orange-100 text-orange-700' : 
												    entry.risk_score > 0 ? 'bg-yellow-100 text-yellow-700' :
												    'bg-gray-100 text-gray-700'}"
										>
											Risk: {entry.risk_score}
										</span>
										{#if entry.timestamp}
											<span class="text-xs text-gray-500">
												{entry.timestamp}
											</span>
										{/if}
									</div>
								</div>
							</div>
						</div>
					{/each}
				</div>
			</div>
		</div>
	{/if}
</div>
