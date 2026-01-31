<script lang="ts">
	/**
	 * Badge Component
	 * 
	 * Status and tag badges with color-coded variants.
	 */

	import { colors, borders, spacing } from '$lib/styles/design-tokens';

	interface Props {
		variant?: 'risk-high' | 'risk-medium' | 'risk-low' | 'info' | 'success' | 'warning' | 'error' | 'neutral';
		size?: 'sm' | 'md';
		dot?: boolean;
		class?: string;
		children: import('svelte').Snippet;
	}

	let {
		variant = 'neutral',
		size = 'md',
		dot = false,
		class: className = '',
		children
	}: Props = $props();

	const variantStyles: Record<string, { bg: string; color: string; border: string }> = {
		'risk-high': {
			bg: colors.risk.highBg,
			color: colors.risk.high,
			border: colors.risk.highBorder,
		},
		'risk-medium': {
			bg: colors.risk.mediumBg,
			color: colors.risk.medium,
			border: colors.risk.mediumBorder,
		},
		'risk-low': {
			bg: colors.risk.lowBg,
			color: colors.risk.low,
			border: colors.risk.lowBorder,
		},
		info: {
			bg: colors.status.infoBg,
			color: colors.status.info,
			border: 'rgba(59, 130, 246, 0.3)',
		},
		success: {
			bg: colors.status.successBg,
			color: colors.status.success,
			border: 'rgba(34, 197, 94, 0.3)',
		},
		warning: {
			bg: colors.status.warningBg,
			color: colors.status.warning,
			border: 'rgba(245, 158, 11, 0.3)',
		},
		error: {
			bg: colors.status.errorBg,
			color: colors.status.error,
			border: 'rgba(239, 68, 68, 0.3)',
		},
		neutral: {
			bg: colors.glass.background,
			color: colors.text.secondary,
			border: colors.glass.border,
		},
	};

	const sizeStyles: Record<string, { padding: string; fontSize: string; dotSize: string }> = {
		sm: { padding: '0.125rem 0.375rem', fontSize: '0.625rem', dotSize: '6px' },
		md: { padding: `${spacing.xs} ${spacing.sm}`, fontSize: '0.75rem', dotSize: '8px' },
	};

	function getStyle(): string {
		const variantStyle = variantStyles[variant];
		const sizeStyle = sizeStyles[size];
		
		return `
			display: inline-flex;
			align-items: center;
			gap: ${spacing.xs};
			padding: ${sizeStyle.padding};
			font-size: ${sizeStyle.fontSize};
			font-weight: 500;
			border-radius: ${borders.radius.full};
			white-space: nowrap;
			background: ${variantStyle.bg};
			color: ${variantStyle.color};
			border: 1px solid ${variantStyle.border};
		`;
	}

	function getDotStyle(): string {
		const variantStyle = variantStyles[variant];
		const sizeStyle = sizeStyles[size];
		
		return `
			width: ${sizeStyle.dotSize};
			height: ${sizeStyle.dotSize};
			border-radius: 50%;
			background: ${variantStyle.color};
		`;
	}
</script>

<span class="badge {className}" style={getStyle()}>
	{#if dot}
		<span style={getDotStyle()}></span>
	{/if}
	{@render children()}
</span>
