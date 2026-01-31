<script lang="ts">
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { analysisResult, hasAnalysis } from '$lib/stores/analysis';
	import { api } from '$lib/api/client';
	import type { TimelineEntry } from '$lib/api/types';

	let timeline: TimelineEntry[] = $state([]);
	let loading = $state(true);
	let showAnomaliesOnly = $state(true);

	const filteredTimeline = $derived(
		showAnomaliesOnly 
			? timeline.filter(e => e.is_anomaly)
			: timeline
	);

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

	function getRiskDotColor(score: number): string {
		if (score >= 50) return '#ef4444';
		if (score >= 20) return '#f97316';
		if (score > 0) return '#eab308';
		return '#6b7280';
	}
</script>

<div style="padding: 1.5rem;">
	<div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 1.5rem;">
		<div>
			<h1 style="font-size: 1.5rem; font-weight: bold; color: white; margin: 0;">
				Timeline
			</h1>
			<p style="color: #9ca3af; margin: 0.25rem 0 0 0;">
				Chronological view of process activity by risk score
			</p>
		</div>

		<label style="display: flex; align-items: center; gap: 0.5rem; cursor: pointer;">
			<input
				type="checkbox"
				bind:checked={showAnomaliesOnly}
				style="width: 16px; height: 16px; accent-color: #3b82f6;"
			/>
			<span style="font-size: 0.875rem; color: #d1d5db;">
				Show anomalies only
			</span>
		</label>
	</div>

	{#if loading}
		<div style="display: flex; align-items: center; justify-content: center; padding: 3rem 0;">
			<svg style="width: 32px; height: 32px; color: #3b82f6; animation: spin 1s linear infinite;" fill="none" viewBox="0 0 24 24">
				<circle style="opacity: 0.25;" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
				<path style="opacity: 0.75;" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
			</svg>
		</div>
	{:else if filteredTimeline.length === 0}
		<div style="text-align: center; padding: 3rem 0; color: #6b7280;">
			{showAnomaliesOnly ? 'No anomalies detected' : 'No timeline data available'}
		</div>
	{:else}
		<div style="background-color: #1f2937; border-radius: 0.75rem; padding: 1.5rem;">
			<div style="position: relative;">
				<!-- Timeline line -->
				<div style="position: absolute; left: 16px; top: 0; bottom: 0; width: 2px; background-color: #374151;"></div>

				<div style="display: flex; flex-direction: column; gap: 1.5rem;">
					{#each filteredTimeline as entry, i}
						<div style="position: relative; display: flex; align-items: flex-start; gap: 1rem; padding-left: 40px;">
							<!-- Timeline dot -->
							<div 
								style="position: absolute; left: 10px; width: 12px; height: 12px; border-radius: 50%; border: 2px solid #1f2937; background-color: {getRiskDotColor(entry.risk_score)};"
							></div>

							<!-- Content -->
							<div style="flex: 1; background-color: rgba(55, 65, 81, 0.5); border-radius: 0.5rem; padding: 1rem;">
								<div style="display: flex; align-items: flex-start; justify-content: space-between;">
									<div>
										<div style="display: flex; align-items: center; gap: 0.5rem; flex-wrap: wrap;">
											<span style="font-weight: 500; color: white;">
												{entry.process_name}
											</span>
											<span style="font-size: 0.75rem; color: #9ca3af;">
												PID: {entry.pid}
											</span>
											{#if entry.is_anomaly}
												<span style="padding: 0.125rem 0.5rem; font-size: 0.75rem; border-radius: 4px; background-color: rgba(239, 68, 68, 0.2); color: #f87171;">
													Anomaly
												</span>
											{/if}
										</div>
										<p style="margin: 0.25rem 0 0 0; font-size: 0.875rem; color: #9ca3af;">
											{entry.description}
										</p>
									</div>

									<div style="display: flex; flex-direction: column; align-items: flex-end; gap: 0.25rem; flex-shrink: 0; margin-left: 1rem;">
										<span 
											style="padding: 0.25rem 0.5rem; font-size: 0.875rem; font-weight: bold; border-radius: 4px;
												   color: {entry.risk_score >= 50 ? '#ef4444' : entry.risk_score >= 20 ? '#f97316' : entry.risk_score > 0 ? '#eab308' : '#9ca3af'};
												   background-color: {entry.risk_score >= 50 ? 'rgba(239, 68, 68, 0.2)' : entry.risk_score >= 20 ? 'rgba(249, 115, 22, 0.2)' : entry.risk_score > 0 ? 'rgba(234, 179, 8, 0.2)' : 'rgba(156, 163, 175, 0.2)'};"
										>
											Risk: {entry.risk_score}
										</span>
										{#if entry.timestamp}
											<span style="font-size: 0.75rem; color: #6b7280;">
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

<style>
	@keyframes spin {
		from { transform: rotate(0deg); }
		to { transform: rotate(360deg); }
	}
</style>
