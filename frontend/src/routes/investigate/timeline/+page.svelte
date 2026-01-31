<script lang="ts">
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { analysisResult, hasAnalysis } from '$lib/stores/analysis';
	import { api } from '$lib/api/client';
	import type { TimelineEntry } from '$lib/api/types';
	import TimelineChart from '$lib/components/visualization/TimelineChart.svelte';
	import TimelineEntryCard from '$lib/components/visualization/TimelineEntryCard.svelte';

	// ==========================================================================
	// STATE
	// ==========================================================================

	let timeline: TimelineEntry[] = $state([]);
	let loading = $state(true);
	let error = $state<string | null>(null);
	let showAnomaliesOnly = $state(false);
	let selectedEntry = $state<TimelineEntry | null>(null);
	let viewMode = $state<'chart' | 'list'>('chart');

	// ==========================================================================
	// DERIVED STATE
	// ==========================================================================

	const filteredTimeline = $derived(
		showAnomaliesOnly ? timeline.filter((e) => e.is_anomaly) : timeline
	);

	const anomalyCount = $derived(timeline.filter((e) => e.is_anomaly).length);
	const highRiskCount = $derived(timeline.filter((e) => e.risk_score >= 50).length);

	// ==========================================================================
	// LIFECYCLE
	// ==========================================================================

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
			error = 'Failed to load timeline data';
		} finally {
			loading = false;
		}
	});

	// ==========================================================================
	// EVENT HANDLERS
	// ==========================================================================

	function handleEntrySelect(entry: TimelineEntry | null): void {
		selectedEntry = entry;
	}

	function handleCardClose(): void {
		selectedEntry = null;
	}

	function getRiskDotColor(score: number): string {
		if (score >= 50) return '#ef4444';
		if (score >= 20) return '#f97316';
		if (score > 0) return '#eab308';
		return '#6b7280';
	}
</script>

<!-- ========================================================================== -->
<!-- TEMPLATE -->
<!-- ========================================================================== -->

<div class="timeline-page">
	<!-- Header -->
	<header class="page-header">
		<div class="header-content">
			<div class="header-icon">
				<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
					<rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>
					<line x1="16" y1="2" x2="16" y2="6"></line>
					<line x1="8" y1="2" x2="8" y2="6"></line>
					<line x1="3" y1="10" x2="21" y2="10"></line>
				</svg>
			</div>
			<div>
				<h1 class="page-title">Activity Timeline</h1>
				<p class="page-subtitle">Chronological view of process events by risk score</p>
			</div>
		</div>

		<div class="header-stats">
			<div class="stat-item">
				<span class="stat-value">{timeline.length}</span>
				<span class="stat-label">Events</span>
			</div>
			<div class="stat-item warning">
				<span class="stat-value">{anomalyCount}</span>
				<span class="stat-label">Anomalies</span>
			</div>
			<div class="stat-item danger">
				<span class="stat-value">{highRiskCount}</span>
				<span class="stat-label">High Risk</span>
			</div>
		</div>
	</header>

	<!-- Controls -->
	<div class="controls-bar">
		<div class="controls-left">
			<!-- View Mode Toggle -->
			<div class="view-toggle">
				<button
					class="toggle-btn"
					class:active={viewMode === 'chart'}
					onclick={() => (viewMode = 'chart')}
				>
					<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
						<rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
						<line x1="3" y1="9" x2="21" y2="9"></line>
						<line x1="9" y1="21" x2="9" y2="9"></line>
					</svg>
					Chart
				</button>
				<button
					class="toggle-btn"
					class:active={viewMode === 'list'}
					onclick={() => (viewMode = 'list')}
				>
					<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
						<line x1="8" y1="6" x2="21" y2="6"></line>
						<line x1="8" y1="12" x2="21" y2="12"></line>
						<line x1="8" y1="18" x2="21" y2="18"></line>
						<line x1="3" y1="6" x2="3.01" y2="6"></line>
						<line x1="3" y1="12" x2="3.01" y2="12"></line>
						<line x1="3" y1="18" x2="3.01" y2="18"></line>
					</svg>
					List
				</button>
			</div>

			<!-- Anomalies Filter -->
			<label class="filter-checkbox">
				<input type="checkbox" bind:checked={showAnomaliesOnly} />
				<span class="checkbox-label">Show anomalies only</span>
			</label>
		</div>

		<div class="controls-right">
			<span class="showing-count">
				Showing {filteredTimeline.length} of {timeline.length} events
			</span>
		</div>
	</div>

	<!-- Main Content -->
	<div class="main-content">
		{#if loading}
			<div class="loading-state">
				<div class="loading-spinner"></div>
				<p>Loading timeline...</p>
			</div>
		{:else if error}
			<div class="error-state">
				<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
					<circle cx="12" cy="12" r="10"></circle>
					<line x1="12" y1="8" x2="12" y2="12"></line>
					<line x1="12" y1="16" x2="12.01" y2="16"></line>
				</svg>
				<p>{error}</p>
				<button class="retry-btn" onclick={() => location.reload()}> Retry </button>
			</div>
		{:else if filteredTimeline.length === 0}
			<div class="empty-state">
				<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
					<rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>
					<line x1="16" y1="2" x2="16" y2="6"></line>
					<line x1="8" y1="2" x2="8" y2="6"></line>
					<line x1="3" y1="10" x2="21" y2="10"></line>
				</svg>
				<h2>No Events Found</h2>
				<p>
					{showAnomaliesOnly ? 'No anomalies detected in this analysis.' : 'No timeline data available.'}
				</p>
			</div>
		{:else if viewMode === 'chart'}
			<div class="chart-layout">
				<div class="chart-section">
					<TimelineChart entries={filteredTimeline} onEntrySelect={handleEntrySelect} />
				</div>
				<aside class="entry-details-section">
					<TimelineEntryCard entry={selectedEntry} onClose={handleCardClose} />
				</aside>
			</div>
		{:else}
			<!-- List View -->
			<div class="list-layout">
				<div class="timeline-list">
					<div class="timeline-line"></div>
					{#each filteredTimeline as entry, i}
						<button
							class="timeline-item"
							class:selected={selectedEntry === entry}
							onclick={() => handleEntrySelect(entry)}
						>
							<div
								class="timeline-dot"
								style="background-color: {getRiskDotColor(entry.risk_score)};"
							></div>
							<div class="item-content">
								<div class="item-header">
									<span class="item-process">{entry.process_name}</span>
									<span class="item-pid">PID: {entry.pid}</span>
									{#if entry.is_anomaly}
										<span class="item-anomaly">Anomaly</span>
									{/if}
								</div>
								<p class="item-description">{entry.description}</p>
							</div>
							<div class="item-meta">
								<span
									class="item-risk"
									style="color: {getRiskDotColor(entry.risk_score)}; background-color: {entry.risk_score >= 50
										? 'rgba(239, 68, 68, 0.15)'
										: entry.risk_score >= 20
											? 'rgba(249, 115, 22, 0.15)'
											: entry.risk_score > 0
												? 'rgba(234, 179, 8, 0.15)'
												: 'rgba(107, 114, 128, 0.15)'};"
								>
									{entry.risk_score}
								</span>
								{#if entry.timestamp}
									<span class="item-time">{entry.timestamp}</span>
								{/if}
							</div>
						</button>
					{/each}
				</div>

				<aside class="entry-details-section">
					<TimelineEntryCard entry={selectedEntry} onClose={handleCardClose} />
				</aside>
			</div>
		{/if}
	</div>
</div>

<!-- ========================================================================== -->
<!-- STYLES -->
<!-- ========================================================================== -->

<style>
	.timeline-page {
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
		background: linear-gradient(135deg, rgba(139, 92, 246, 0.2), rgba(236, 72, 153, 0.2));
		border-radius: 12px;
		border: 1px solid rgba(139, 92, 246, 0.3);
	}

	.header-icon svg {
		width: 24px;
		height: 24px;
		color: #8b5cf6;
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

	.header-stats {
		display: flex;
		gap: 16px;
	}

	.stat-item {
		display: flex;
		flex-direction: column;
		align-items: center;
		padding: 8px 16px;
		background: rgba(255, 255, 255, 0.05);
		border-radius: 8px;
		border: 1px solid rgba(255, 255, 255, 0.1);
	}

	.stat-item.warning {
		border-color: rgba(249, 115, 22, 0.3);
		background: rgba(249, 115, 22, 0.1);
	}

	.stat-item.danger {
		border-color: rgba(239, 68, 68, 0.3);
		background: rgba(239, 68, 68, 0.1);
	}

	.stat-value {
		font-size: 18px;
		font-weight: 700;
		color: white;
	}

	.stat-item.warning .stat-value {
		color: #f97316;
	}

	.stat-item.danger .stat-value {
		color: #ef4444;
	}

	.stat-label {
		font-size: 10px;
		color: rgba(255, 255, 255, 0.5);
		text-transform: uppercase;
		letter-spacing: 0.5px;
	}

	/* Controls Bar */
	.controls-bar {
		display: flex;
		justify-content: space-between;
		align-items: center;
		padding: 12px 16px;
		background: var(--glass-bg, rgba(255, 255, 255, 0.03));
		border-radius: 12px;
		border: 1px solid var(--glass-border, rgba(255, 255, 255, 0.08));
		flex-wrap: wrap;
		gap: 12px;
	}

	.controls-left,
	.controls-right {
		display: flex;
		align-items: center;
		gap: 16px;
	}

	.view-toggle {
		display: flex;
		background: rgba(0, 0, 0, 0.2);
		border-radius: 8px;
		padding: 4px;
	}

	.toggle-btn {
		display: flex;
		align-items: center;
		gap: 6px;
		padding: 6px 14px;
		background: transparent;
		border: none;
		border-radius: 6px;
		color: rgba(255, 255, 255, 0.6);
		font-size: 13px;
		font-weight: 500;
		cursor: pointer;
		transition: all 0.2s ease;
	}

	.toggle-btn svg {
		width: 14px;
		height: 14px;
	}

	.toggle-btn:hover {
		color: white;
	}

	.toggle-btn.active {
		background: rgba(255, 255, 255, 0.1);
		color: white;
	}

	.filter-checkbox {
		display: flex;
		align-items: center;
		gap: 8px;
		cursor: pointer;
	}

	.filter-checkbox input {
		width: 16px;
		height: 16px;
		accent-color: #3b82f6;
	}

	.checkbox-label {
		font-size: 13px;
		color: rgba(255, 255, 255, 0.7);
	}

	.showing-count {
		font-size: 13px;
		color: rgba(255, 255, 255, 0.5);
	}

	/* Main Content */
	.main-content {
		flex: 1;
		display: flex;
		flex-direction: column;
		min-height: 0;
	}

	/* Chart Layout */
	.chart-layout {
		flex: 1;
		display: grid;
		grid-template-columns: 1fr 320px;
		gap: 20px;
		min-height: 400px;
	}

	.chart-section {
		min-height: 400px;
	}

	.entry-details-section {
		min-height: 300px;
	}

	/* List Layout */
	.list-layout {
		flex: 1;
		display: grid;
		grid-template-columns: 1fr 320px;
		gap: 20px;
	}

	.timeline-list {
		position: relative;
		display: flex;
		flex-direction: column;
		gap: 12px;
		padding: 16px;
		background: var(--glass-bg, rgba(255, 255, 255, 0.03));
		border-radius: 12px;
		border: 1px solid var(--glass-border, rgba(255, 255, 255, 0.08));
		max-height: 600px;
		overflow-y: auto;
	}

	.timeline-line {
		position: absolute;
		left: 32px;
		top: 16px;
		bottom: 16px;
		width: 2px;
		background: rgba(255, 255, 255, 0.1);
	}

	.timeline-item {
		position: relative;
		display: flex;
		align-items: flex-start;
		gap: 16px;
		padding: 12px 16px 12px 40px;
		background: rgba(255, 255, 255, 0.02);
		border: 1px solid rgba(255, 255, 255, 0.05);
		border-radius: 8px;
		cursor: pointer;
		transition: all 0.2s ease;
		text-align: left;
		width: 100%;
	}

	.timeline-item:hover {
		background: rgba(255, 255, 255, 0.05);
		border-color: rgba(255, 255, 255, 0.1);
	}

	.timeline-item.selected {
		background: rgba(59, 130, 246, 0.1);
		border-color: rgba(59, 130, 246, 0.3);
	}

	.timeline-dot {
		position: absolute;
		left: 10px;
		top: 16px;
		width: 10px;
		height: 10px;
		border-radius: 50%;
		border: 2px solid rgba(10, 10, 15, 1);
	}

	.item-content {
		flex: 1;
		min-width: 0;
	}

	.item-header {
		display: flex;
		align-items: center;
		gap: 8px;
		flex-wrap: wrap;
		margin-bottom: 4px;
	}

	.item-process {
		font-weight: 500;
		color: white;
		font-size: 14px;
	}

	.item-pid {
		font-size: 11px;
		color: rgba(255, 255, 255, 0.5);
		font-family: monospace;
	}

	.item-anomaly {
		padding: 2px 6px;
		background: rgba(239, 68, 68, 0.15);
		border-radius: 3px;
		font-size: 10px;
		font-weight: 600;
		color: #ef4444;
	}

	.item-description {
		margin: 0;
		font-size: 12px;
		color: rgba(255, 255, 255, 0.6);
		overflow: hidden;
		text-overflow: ellipsis;
		white-space: nowrap;
	}

	.item-meta {
		display: flex;
		flex-direction: column;
		align-items: flex-end;
		gap: 4px;
		flex-shrink: 0;
	}

	.item-risk {
		padding: 4px 8px;
		border-radius: 4px;
		font-size: 12px;
		font-weight: 600;
	}

	.item-time {
		font-size: 10px;
		color: rgba(255, 255, 255, 0.4);
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
		border-top-color: #8b5cf6;
		border-radius: 50%;
		animation: spin 1s linear infinite;
	}

	@keyframes spin {
		to {
			transform: rotate(360deg);
		}
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
		background: #8b5cf6;
		border: none;
		border-radius: 8px;
		color: white;
		font-size: 14px;
		font-weight: 500;
		cursor: pointer;
		transition: background 0.2s ease;
	}

	.retry-btn:hover {
		background: #7c3aed;
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
		.chart-layout,
		.list-layout {
			grid-template-columns: 1fr;
		}

		.entry-details-section {
			order: -1;
		}
	}

	@media (max-width: 640px) {
		.timeline-page {
			padding: 16px;
		}

		.page-header {
			flex-direction: column;
			align-items: flex-start;
		}

		.header-stats {
			width: 100%;
			justify-content: space-between;
		}
	}
</style>
