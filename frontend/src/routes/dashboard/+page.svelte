<script lang="ts">
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { analysisStore, analysisResult, hasAnalysis, topThreats } from '$lib/stores/analysis';
	import { api } from '$lib/api/client';
	import RiskGauge from '$lib/components/visualization/RiskGauge.svelte';
	import FindingList from '$lib/components/findings/FindingList.svelte';

	let downloading = false;

	// Redirect if no analysis
	onMount(() => {
		if (!$hasAnalysis) {
			goto('/');
		}
	});

	// Download PDF report
	async function downloadReport() {
		if (!$analysisResult) return;

		downloading = true;
		try {
			const blob = await api.downloadReport($analysisResult.analysis_id);
			const url = URL.createObjectURL(blob);
			const a = document.createElement('a');
			a.href = url;
			a.download = `procbench_report_${$analysisResult.analysis_id}.pdf`;
			document.body.appendChild(a);
			a.click();
			document.body.removeChild(a);
			URL.revokeObjectURL(url);
		} catch (e) {
			console.error('Failed to download report:', e);
		} finally {
			downloading = false;
		}
	}

	// Calculate max risk score
	$: maxRiskScore = $topThreats.length > 0 
		? Math.max(...$topThreats.map(p => p.risk_score)) 
		: 0;
</script>

{#if $analysisResult}
	<div class="p-6">
		<!-- Header -->
		<div class="flex items-center justify-between mb-6">
			<div>
				<h1 class="text-2xl font-bold text-gray-900 dark:text-white">
					Analysis Dashboard
				</h1>
				<p class="text-gray-600 dark:text-gray-400">
					{$analysisResult.filename} • {$analysisResult.analysis_id}
				</p>
			</div>

			<button
				class="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg
					   hover:bg-blue-700 transition-colors disabled:opacity-50"
				on:click={downloadReport}
				disabled={downloading}
			>
				{#if downloading}
					<svg class="animate-spin w-5 h-5" fill="none" viewBox="0 0 24 24">
						<circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
						<path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
					</svg>
				{:else}
					<svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
						<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
					</svg>
				{/if}
				Download Report
			</button>
		</div>

		<!-- Stats Grid -->
		<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4 mb-6">
			<div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm p-6">
				<p class="text-sm text-gray-500 dark:text-gray-400">Total Events</p>
				<p class="text-2xl font-bold text-gray-900 dark:text-white">
					{$analysisResult.total_events.toLocaleString()}
				</p>
			</div>

			<div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm p-6">
				<p class="text-sm text-gray-500 dark:text-gray-400">Total Processes</p>
				<p class="text-2xl font-bold text-gray-900 dark:text-white">
					{$analysisResult.total_processes}
				</p>
			</div>

			<div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm p-6">
				<p class="text-sm text-gray-500 dark:text-gray-400">Flagged Processes</p>
				<p class="text-2xl font-bold text-orange-600">
					{$analysisResult.flagged_processes}
				</p>
			</div>

			<div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm p-6">
				<p class="text-sm text-gray-500 dark:text-gray-400">High Risk</p>
				<p class="text-2xl font-bold text-red-600">
					{$analysisResult.high_risk_count}
				</p>
			</div>

			<div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm p-6">
				<p class="text-sm text-gray-500 dark:text-gray-400">Analysis Time</p>
				<p class="text-2xl font-bold text-gray-900 dark:text-white">
					{$analysisResult.analysis_duration_seconds.toFixed(2)}s
				</p>
			</div>
		</div>

		<!-- Main Content -->
		<div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
			<!-- Risk Overview -->
			<div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm p-6">
				<h2 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">
					Risk Overview
				</h2>
				
				<div class="flex justify-center mb-6">
					<RiskGauge score={maxRiskScore} size="lg" />
				</div>

				<div class="space-y-3">
					<div class="flex items-center justify-between">
						<span class="flex items-center gap-2">
							<span class="w-3 h-3 rounded-full bg-red-500"></span>
							<span class="text-gray-700 dark:text-gray-300">High Risk</span>
						</span>
						<span class="font-semibold text-gray-900 dark:text-white">
							{$analysisResult.high_risk_count}
						</span>
					</div>

					<div class="flex items-center justify-between">
						<span class="flex items-center gap-2">
							<span class="w-3 h-3 rounded-full bg-orange-500"></span>
							<span class="text-gray-700 dark:text-gray-300">Medium Risk</span>
						</span>
						<span class="font-semibold text-gray-900 dark:text-white">
							{$analysisResult.medium_risk_count}
						</span>
					</div>

					<div class="flex items-center justify-between">
						<span class="flex items-center gap-2">
							<span class="w-3 h-3 rounded-full bg-green-500"></span>
							<span class="text-gray-700 dark:text-gray-300">Low Risk</span>
						</span>
						<span class="font-semibold text-gray-900 dark:text-white">
							{$analysisResult.low_risk_count}
						</span>
					</div>
				</div>
			</div>

			<!-- Top Threats -->
			<div class="lg:col-span-2 bg-white dark:bg-gray-800 rounded-xl shadow-sm p-6">
				<FindingList 
					processes={$topThreats} 
					title="Top Threats" 
					emptyMessage="No threats detected"
					maxItems={5}
					compact
				/>
			</div>
		</div>

		<!-- Quick Actions -->
		<div class="mt-6 flex gap-4">
			<a
				href="/investigate/tree"
				class="flex-1 flex items-center justify-center gap-2 p-4 bg-white dark:bg-gray-800 
					   rounded-xl shadow-sm hover:shadow-md transition-shadow text-gray-900 dark:text-white"
			>
				<svg class="w-6 h-6 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
					<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
				</svg>
				<span class="font-medium">View Process Tree</span>
			</a>

			<a
				href="/investigate/timeline"
				class="flex-1 flex items-center justify-center gap-2 p-4 bg-white dark:bg-gray-800 
					   rounded-xl shadow-sm hover:shadow-md transition-shadow text-gray-900 dark:text-white"
			>
				<svg class="w-6 h-6 text-purple-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
					<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
				</svg>
				<span class="font-medium">View Timeline</span>
			</a>
		</div>
	</div>
{:else}
	<div class="flex items-center justify-center min-h-screen">
		<p class="text-gray-500">Loading...</p>
	</div>
{/if}
