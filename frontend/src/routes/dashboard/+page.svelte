<script lang="ts">
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { analysisResult, hasAnalysis, topThreats } from '$lib/stores/analysis';
	import { api } from '$lib/api/client';
	import RiskGauge from '$lib/components/visualization/RiskGauge.svelte';
	import FindingList from '$lib/components/findings/FindingList.svelte';
	import { GlassCard, Button } from '$lib/components/ui';
	import { colors, spacing, borders, animation, shadows } from '$lib/styles/design-tokens';

	let downloading = $state(false);

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
	const maxRiskScore = $derived(
		$topThreats.length > 0 
			? Math.max(...$topThreats.map(p => p.risk_score)) 
			: 0
	);

	// Stats configuration
	const stats = $derived([
		{ label: 'Total Events', value: $analysisResult?.total_events.toLocaleString() ?? '0', color: colors.accent.primary, icon: 'events' },
		{ label: 'Total Processes', value: $analysisResult?.total_processes.toString() ?? '0', color: colors.accent.secondary, icon: 'processes' },
		{ label: 'Flagged', value: $analysisResult?.flagged_processes.toString() ?? '0', color: colors.risk.medium, icon: 'flagged' },
		{ label: 'High Risk', value: $analysisResult?.high_risk_count.toString() ?? '0', color: colors.risk.high, icon: 'danger' },
		{ label: 'Analysis Time', value: `${$analysisResult?.analysis_duration_seconds.toFixed(2) ?? '0'}s`, color: colors.status.success, icon: 'time' },
	]);
</script>

{#if $analysisResult}
	<div style="padding: {spacing.lg}; animation: fadeInUp {animation.duration.normal} {animation.easing.easeOut};">
		<!-- Header -->
		<div style="
			display: flex;
			align-items: center;
			justify-content: space-between;
			margin-bottom: {spacing.xl};
		">
			<div>
				<h1 style="
					font-size: 1.75rem;
					font-weight: 700;
					color: {colors.text.primary};
					margin: 0;
					background: {colors.accent.gradient};
					-webkit-background-clip: text;
					-webkit-text-fill-color: transparent;
					background-clip: text;
				">
					Analysis Dashboard
				</h1>
				<p style="color: {colors.text.tertiary}; margin: {spacing.xs} 0 0 0; font-size: 0.875rem;">
					<span style="color: {colors.text.secondary};">{$analysisResult.filename}</span>
					<span style="margin: 0 {spacing.sm};">•</span>
					<span style="font-family: monospace; font-size: 0.8rem;">{$analysisResult.analysis_id}</span>
				</p>
			</div>

			<Button variant="primary" loading={downloading} onclick={downloadReport}>
				<svg style="width: 18px; height: 18px;" fill="none" viewBox="0 0 24 24" stroke="currentColor">
					<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
				</svg>
				Download Report
			</Button>
		</div>

		<!-- Stats Grid -->
		<div style="display: grid; grid-template-columns: repeat(5, 1fr); gap: {spacing.md}; margin-bottom: {spacing.xl};">
			{#each stats as stat, i}
				<div 
					role="article"
					style="
						background: {colors.glass.background};
						backdrop-filter: blur(12px);
						-webkit-backdrop-filter: blur(12px);
						border: 1px solid {colors.glass.border};
						border-radius: {borders.radius.xl};
						padding: {spacing.lg};
						transition: all {animation.duration.normal} {animation.easing.easeInOut};
						animation: fadeInUp {animation.duration.normal} {animation.easing.easeOut};
						animation-delay: {i * 50}ms;
						animation-fill-mode: backwards;
					"
					onmouseenter={(e) => {
						const el = e.currentTarget as HTMLElement;
						el.style.transform = 'translateY(-4px)';
						el.style.borderColor = stat.color;
						el.style.boxShadow = `0 0 20px ${stat.color}33`;
					}}
					onmouseleave={(e) => {
						const el = e.currentTarget as HTMLElement;
						el.style.transform = 'translateY(0)';
						el.style.borderColor = colors.glass.border;
						el.style.boxShadow = 'none';
					}}
				>
					<p style="font-size: 0.75rem; color: {colors.text.tertiary}; margin: 0; text-transform: uppercase; letter-spacing: 0.05em;">
						{stat.label}
					</p>
					<p style="font-size: 1.75rem; font-weight: 700; color: {stat.color}; margin: {spacing.xs} 0 0 0;">
						{stat.value}
					</p>
				</div>
			{/each}
		</div>

		<!-- Main Content -->
		<div style="display: grid; grid-template-columns: 1fr 2fr; gap: {spacing.lg};">
			<!-- Risk Overview -->
			<GlassCard variant="elevated">
				<h2 style="
					font-size: 1rem;
					font-weight: 600;
					color: {colors.text.primary};
					margin: 0 0 {spacing.lg} 0;
					display: flex;
					align-items: center;
					gap: {spacing.sm};
				">
					<svg style="width: 18px; height: 18px; color: {colors.accent.primary};" fill="none" viewBox="0 0 24 24" stroke="currentColor">
						<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
					</svg>
					Risk Overview
				</h2>
				
				<div style="display: flex; justify-content: center; margin-bottom: {spacing.xl};">
					<RiskGauge score={maxRiskScore} size="lg" />
				</div>

				<div style="display: flex; flex-direction: column; gap: {spacing.md};">
					<!-- High Risk -->
					<div style="
						display: flex;
						align-items: center;
						justify-content: space-between;
						padding: {spacing.sm} {spacing.md};
						background: {colors.risk.highBg};
						border-radius: {borders.radius.lg};
						border: 1px solid {colors.risk.highBorder};
					">
						<span style="display: flex; align-items: center; gap: {spacing.sm};">
							<span style="width: 10px; height: 10px; border-radius: 50%; background: {colors.risk.high}; box-shadow: 0 0 8px {colors.risk.high};"></span>
							<span style="color: {colors.text.secondary}; font-size: 0.875rem;">High Risk</span>
						</span>
						<span style="font-weight: 700; color: {colors.risk.high}; font-size: 1.125rem;">
							{$analysisResult.high_risk_count}
						</span>
					</div>

					<!-- Medium Risk -->
					<div style="
						display: flex;
						align-items: center;
						justify-content: space-between;
						padding: {spacing.sm} {spacing.md};
						background: {colors.risk.mediumBg};
						border-radius: {borders.radius.lg};
						border: 1px solid {colors.risk.mediumBorder};
					">
						<span style="display: flex; align-items: center; gap: {spacing.sm};">
							<span style="width: 10px; height: 10px; border-radius: 50%; background: {colors.risk.medium}; box-shadow: 0 0 8px {colors.risk.medium};"></span>
							<span style="color: {colors.text.secondary}; font-size: 0.875rem;">Medium Risk</span>
						</span>
						<span style="font-weight: 700; color: {colors.risk.medium}; font-size: 1.125rem;">
							{$analysisResult.medium_risk_count}
						</span>
					</div>

					<!-- Low Risk -->
					<div style="
						display: flex;
						align-items: center;
						justify-content: space-between;
						padding: {spacing.sm} {spacing.md};
						background: {colors.status.successBg};
						border-radius: {borders.radius.lg};
						border: 1px solid rgba(34, 197, 94, 0.3);
					">
						<span style="display: flex; align-items: center; gap: {spacing.sm};">
							<span style="width: 10px; height: 10px; border-radius: 50%; background: {colors.status.success}; box-shadow: 0 0 8px {colors.status.success};"></span>
							<span style="color: {colors.text.secondary}; font-size: 0.875rem;">Low Risk</span>
						</span>
						<span style="font-weight: 700; color: {colors.status.success}; font-size: 1.125rem;">
							{$analysisResult.low_risk_count}
						</span>
					</div>
				</div>
			</GlassCard>

			<!-- Top Threats -->
			<GlassCard variant="elevated">
				<FindingList 
					processes={$topThreats} 
					title="Top Threats" 
					emptyMessage="No threats detected"
					maxItems={5}
					compact
				/>
			</GlassCard>
		</div>

		<!-- Quick Actions -->
		<div style="margin-top: {spacing.xl}; display: grid; grid-template-columns: 1fr 1fr; gap: {spacing.md};">
			<a
				href="/investigate/tree"
				style="
					display: flex;
					align-items: center;
					justify-content: center;
					gap: {spacing.md};
					padding: {spacing.lg};
					background: {colors.glass.background};
					backdrop-filter: blur(12px);
					border: 1px solid {colors.glass.border};
					border-radius: {borders.radius.xl};
					color: {colors.text.primary};
					text-decoration: none;
					transition: all {animation.duration.normal} {animation.easing.easeInOut};
				"
				onmouseenter={(e) => {
					const el = e.currentTarget as HTMLElement;
					el.style.background = colors.glass.backgroundHover;
					el.style.borderColor = colors.accent.primary;
					el.style.boxShadow = shadows.glow.primary;
					el.style.transform = 'translateY(-2px)';
				}}
				onmouseleave={(e) => {
					const el = e.currentTarget as HTMLElement;
					el.style.background = colors.glass.background;
					el.style.borderColor = colors.glass.border;
					el.style.boxShadow = 'none';
					el.style.transform = 'translateY(0)';
				}}
			>
				<div style="
					width: 48px;
					height: 48px;
					display: flex;
					align-items: center;
					justify-content: center;
					background: {colors.status.infoBg};
					border-radius: {borders.radius.lg};
				">
					<svg style="width: 24px; height: 24px; color: {colors.accent.primary};" fill="none" viewBox="0 0 24 24" stroke="currentColor">
						<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
					</svg>
				</div>
				<div>
					<span style="font-weight: 600; font-size: 1rem;">View Process Tree</span>
					<p style="margin: {spacing.xs} 0 0 0; font-size: 0.8rem; color: {colors.text.tertiary};">Interactive process hierarchy</p>
				</div>
				<svg style="width: 20px; height: 20px; color: {colors.text.muted}; margin-left: auto;" fill="none" viewBox="0 0 24 24" stroke="currentColor">
					<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
				</svg>
			</a>

			<a
				href="/investigate/timeline"
				style="
					display: flex;
					align-items: center;
					justify-content: center;
					gap: {spacing.md};
					padding: {spacing.lg};
					background: {colors.glass.background};
					backdrop-filter: blur(12px);
					border: 1px solid {colors.glass.border};
					border-radius: {borders.radius.xl};
					color: {colors.text.primary};
					text-decoration: none;
					transition: all {animation.duration.normal} {animation.easing.easeInOut};
				"
				onmouseenter={(e) => {
					const el = e.currentTarget as HTMLElement;
					el.style.background = colors.glass.backgroundHover;
					el.style.borderColor = colors.accent.secondary;
					el.style.boxShadow = '0 0 20px rgba(139, 92, 246, 0.3)';
					el.style.transform = 'translateY(-2px)';
				}}
				onmouseleave={(e) => {
					const el = e.currentTarget as HTMLElement;
					el.style.background = colors.glass.background;
					el.style.borderColor = colors.glass.border;
					el.style.boxShadow = 'none';
					el.style.transform = 'translateY(0)';
				}}
			>
				<div style="
					width: 48px;
					height: 48px;
					display: flex;
					align-items: center;
					justify-content: center;
					background: rgba(139, 92, 246, 0.15);
					border-radius: {borders.radius.lg};
				">
					<svg style="width: 24px; height: 24px; color: {colors.accent.secondary};" fill="none" viewBox="0 0 24 24" stroke="currentColor">
						<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
					</svg>
				</div>
				<div>
					<span style="font-weight: 600; font-size: 1rem;">View Timeline</span>
					<p style="margin: {spacing.xs} 0 0 0; font-size: 0.8rem; color: {colors.text.tertiary};">Chronological event analysis</p>
				</div>
				<svg style="width: 20px; height: 20px; color: {colors.text.muted}; margin-left: auto;" fill="none" viewBox="0 0 24 24" stroke="currentColor">
					<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
				</svg>
			</a>
		</div>
	</div>
{:else}
	<div style="display: flex; align-items: center; justify-content: center; min-height: 100vh;">
		<div style="text-align: center;">
			<div style="
				width: 48px;
				height: 48px;
				margin: 0 auto {spacing.md};
				border: 3px solid {colors.glass.border};
				border-top-color: {colors.accent.primary};
				border-radius: 50%;
				animation: spin 1s linear infinite;
			"></div>
			<p style="color: {colors.text.tertiary};">Loading analysis...</p>
		</div>
	</div>
{/if}

<style>
	@keyframes spin {
		from { transform: rotate(0deg); }
		to { transform: rotate(360deg); }
	}
	
	@keyframes fadeInUp {
		from {
			opacity: 0;
			transform: translateY(10px);
		}
		to {
			opacity: 1;
			transform: translateY(0);
		}
	}
</style>
