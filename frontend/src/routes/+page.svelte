<script lang="ts">
	import FileUpload from '$lib/components/upload/FileUpload.svelte';
	import { colors, spacing, borders, animation, shadows } from '$lib/styles/design-tokens';
</script>

<div style="min-height: 100vh; display: flex; flex-direction: column;">
	<!-- Page Header -->
	<div style="
		background: {colors.glass.background};
		backdrop-filter: blur(16px);
		-webkit-backdrop-filter: blur(16px);
		border-bottom: 1px solid {colors.glass.border};
		padding: {spacing.xl} {spacing.lg};
	">
		<div style="max-width: 56rem; margin: 0 auto; text-align: center;">
			<h1 style="
				font-size: 2.5rem; 
				font-weight: 800; 
				margin: 0;
				background: {colors.accent.gradient};
				-webkit-background-clip: text;
				-webkit-text-fill-color: transparent;
				background-clip: text;
				text-shadow: none;
			">
				ProcBench
			</h1>
			<p style="margin-top: {spacing.sm}; color: {colors.text.tertiary}; font-size: 1rem;">
				AI-powered Process Monitor log analysis for SOC analysts
			</p>
		</div>
	</div>

	<!-- Main content -->
	<main style="flex: 1; display: flex; align-items: center; justify-content: center; padding: {spacing.xl};">
		<div style="max-width: 56rem; width: 100%; animation: fadeInUp {animation.duration.normal} {animation.easing.easeOut};">
			<div style="text-align: center; margin-bottom: {spacing.xl};">
				<h2 style="font-size: 1.5rem; font-weight: 600; color: {colors.text.primary}; margin: 0 0 {spacing.sm} 0;">
					Upload Process Monitor Log
				</h2>
				<p style="color: {colors.text.tertiary}; margin: 0; max-width: 32rem; margin: 0 auto;">
					Turn process noise into threat signal. Upload your PML, CSV, or XML log file to get started.
				</p>
			</div>

			<FileUpload />

			<!-- Features -->
			<div style="margin-top: {spacing['2xl']}; display: grid; grid-template-columns: repeat(3, 1fr); gap: {spacing.lg};">
				<div 
					role="article"
					style="
						text-align: center; 
						padding: {spacing.xl}; 
						background: {colors.glass.background};
						backdrop-filter: blur(12px);
						-webkit-backdrop-filter: blur(12px);
						border: 1px solid {colors.glass.border};
						border-radius: {borders.radius.xl};
						transition: all {animation.duration.normal} {animation.easing.easeInOut};
					"
					onmouseenter={(e) => {
						const el = e.currentTarget as HTMLElement;
						el.style.transform = 'translateY(-4px)';
						el.style.borderColor = colors.accent.primary;
						el.style.boxShadow = shadows.glow.primary;
					}}
					onmouseleave={(e) => {
						const el = e.currentTarget as HTMLElement;
						el.style.transform = 'translateY(0)';
						el.style.borderColor = colors.glass.border;
						el.style.boxShadow = 'none';
					}}
				>
					<div style="
						width: 56px; 
						height: 56px; 
						margin: 0 auto {spacing.md}; 
						background: {colors.status.infoBg}; 
						border-radius: {borders.radius.lg}; 
						display: flex; 
						align-items: center; 
						justify-content: center;
						border: 1px solid rgba(59, 130, 246, 0.3);
					">
						<svg style="width: 28px; height: 28px; color: {colors.accent.primary};" fill="none" viewBox="0 0 24 24" stroke="currentColor">
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
						</svg>
					</div>
					<h3 style="font-weight: 600; color: {colors.text.primary}; margin: 0 0 {spacing.sm} 0;">LOLBAS Detection</h3>
					<p style="font-size: 0.875rem; color: {colors.text.tertiary}; margin: 0; line-height: 1.5;">
						Identifies living-off-the-land binaries used by attackers
					</p>
				</div>

				<div 
					role="article"
					style="
						text-align: center; 
						padding: {spacing.xl}; 
						background: {colors.glass.background};
						backdrop-filter: blur(12px);
						-webkit-backdrop-filter: blur(12px);
						border: 1px solid {colors.glass.border};
						border-radius: {borders.radius.xl};
						transition: all {animation.duration.normal} {animation.easing.easeInOut};
					"
					onmouseenter={(e) => {
						const el = e.currentTarget as HTMLElement;
						el.style.transform = 'translateY(-4px)';
						el.style.borderColor = colors.accent.secondary;
						el.style.boxShadow = '0 0 20px rgba(139, 92, 246, 0.3)';
					}}
					onmouseleave={(e) => {
						const el = e.currentTarget as HTMLElement;
						el.style.transform = 'translateY(0)';
						el.style.borderColor = colors.glass.border;
						el.style.boxShadow = 'none';
					}}
				>
					<div style="
						width: 56px; 
						height: 56px; 
						margin: 0 auto {spacing.md}; 
						background: rgba(139, 92, 246, 0.15); 
						border-radius: {borders.radius.lg}; 
						display: flex; 
						align-items: center; 
						justify-content: center;
						border: 1px solid rgba(139, 92, 246, 0.3);
					">
						<svg style="width: 28px; height: 28px; color: {colors.accent.secondary};" fill="none" viewBox="0 0 24 24" stroke="currentColor">
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
						</svg>
					</div>
					<h3 style="font-weight: 600; color: {colors.text.primary}; margin: 0 0 {spacing.sm} 0;">AI Analysis</h3>
					<p style="font-size: 0.875rem; color: {colors.text.tertiary}; margin: 0; line-height: 1.5;">
						AI-powered reasoning for suspicious process behavior
					</p>
				</div>

				<div 
					role="article"
					style="
						text-align: center; 
						padding: {spacing.xl}; 
						background: {colors.glass.background};
						backdrop-filter: blur(12px);
						-webkit-backdrop-filter: blur(12px);
						border: 1px solid {colors.glass.border};
						border-radius: {borders.radius.xl};
						transition: all {animation.duration.normal} {animation.easing.easeInOut};
					"
					onmouseenter={(e) => {
						const el = e.currentTarget as HTMLElement;
						el.style.transform = 'translateY(-4px)';
						el.style.borderColor = colors.status.success;
						el.style.boxShadow = '0 0 20px rgba(34, 197, 94, 0.3)';
					}}
					onmouseleave={(e) => {
						const el = e.currentTarget as HTMLElement;
						el.style.transform = 'translateY(0)';
						el.style.borderColor = colors.glass.border;
						el.style.boxShadow = 'none';
					}}
				>
					<div style="
						width: 56px; 
						height: 56px; 
						margin: 0 auto {spacing.md}; 
						background: {colors.status.successBg}; 
						border-radius: {borders.radius.lg}; 
						display: flex; 
						align-items: center; 
						justify-content: center;
						border: 1px solid rgba(34, 197, 94, 0.3);
					">
						<svg style="width: 28px; height: 28px; color: {colors.status.success};" fill="none" viewBox="0 0 24 24" stroke="currentColor">
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
						</svg>
					</div>
					<h3 style="font-weight: 600; color: {colors.text.primary}; margin: 0 0 {spacing.sm} 0;">PDF Reports</h3>
					<p style="font-size: 0.875rem; color: {colors.text.tertiary}; margin: 0; line-height: 1.5;">
						Export professional reports for stakeholders
					</p>
				</div>
			</div>
		</div>
	</main>

	<!-- Footer -->
	<footer style="
		padding: {spacing.md}; 
		text-align: center;
		border-top: 1px solid {colors.glass.border};
		background: {colors.glass.background};
	">
		<p style="font-size: 0.8rem; color: {colors.text.muted}; margin: 0;">
			ProcBench v1.0 - Process Monitor Analysis Platform
		</p>
	</footer>
</div>

<style>
	@keyframes fadeInUp {
		from {
			opacity: 0;
			transform: translateY(16px);
		}
		to {
			opacity: 1;
			transform: translateY(0);
		}
	}
</style>
