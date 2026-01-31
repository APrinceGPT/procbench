<script lang="ts">
	/**
	 * Button Component
	 * 
	 * Modern button with multiple variants, sizes, and loading states.
	 */

	import { colors, borders, spacing, animation, shadows } from '$lib/styles/design-tokens';

	interface Props {
		variant?: 'primary' | 'secondary' | 'ghost' | 'danger';
		size?: 'sm' | 'md' | 'lg';
		loading?: boolean;
		disabled?: boolean;
		fullWidth?: boolean;
		type?: 'button' | 'submit' | 'reset';
		class?: string;
		onclick?: (event: MouseEvent) => void;
		children: import('svelte').Snippet;
	}

	let {
		variant = 'primary',
		size = 'md',
		loading = false,
		disabled = false,
		fullWidth = false,
		type = 'button',
		class: className = '',
		onclick,
		children
	}: Props = $props();

	const sizeStyles: Record<string, { height: string; padding: string; fontSize: string }> = {
		sm: { height: '2rem', padding: `0 ${spacing.sm}`, fontSize: '0.75rem' },
		md: { height: '2.5rem', padding: `0 ${spacing.md}`, fontSize: '0.875rem' },
		lg: { height: '3rem', padding: `0 ${spacing.lg}`, fontSize: '1rem' },
	};

	const variantStyles: Record<string, { base: string; hover: string }> = {
		primary: {
			base: `
				background: ${colors.accent.gradient};
				color: white;
				border: none;
				box-shadow: ${shadows.sm};
			`,
			hover: `
				box-shadow: ${shadows.glow.primary};
				transform: translateY(-1px);
			`,
		},
		secondary: {
			base: `
				background: ${colors.glass.background};
				color: ${colors.text.primary};
				border: 1px solid ${colors.glass.border};
			`,
			hover: `
				background: ${colors.glass.backgroundHover};
				border-color: ${colors.glass.borderHover};
			`,
		},
		ghost: {
			base: `
				background: transparent;
				color: ${colors.text.secondary};
				border: none;
			`,
			hover: `
				background: ${colors.glass.background};
				color: ${colors.text.primary};
			`,
		},
		danger: {
			base: `
				background: ${colors.status.error};
				color: white;
				border: none;
			`,
			hover: `
				background: #dc2626;
				box-shadow: ${shadows.glow.danger};
			`,
		},
	};

	function getBaseStyle(): string {
		const sizeStyle = sizeStyles[size];
		const variantStyle = variantStyles[variant];
		
		return `
			display: inline-flex;
			align-items: center;
			justify-content: center;
			gap: ${spacing.sm};
			height: ${sizeStyle.height};
			padding: ${sizeStyle.padding};
			font-size: ${sizeStyle.fontSize};
			font-weight: 500;
			line-height: 1.5;
			border-radius: ${borders.radius.md};
			cursor: ${disabled || loading ? 'not-allowed' : 'pointer'};
			opacity: ${disabled || loading ? '0.5' : '1'};
			transition: all ${animation.duration.fast} ${animation.easing.easeInOut};
			white-space: nowrap;
			width: ${fullWidth ? '100%' : 'auto'};
			${variantStyle.base}
		`;
	}

	let isHovered = $state(false);

	function getHoverStyle(): string {
		if (disabled || loading || !isHovered) return '';
		return variantStyles[variant].hover;
	}
</script>

<button
	{type}
	disabled={disabled || loading}
	class="btn {className}"
	style="{getBaseStyle()} {getHoverStyle()}"
	onmouseenter={() => isHovered = true}
	onmouseleave={() => isHovered = false}
	{onclick}
>
	{#if loading}
		<svg 
			style="width: 16px; height: 16px; animation: spin 1s linear infinite;"
			fill="none" 
			viewBox="0 0 24 24"
		>
			<circle 
				style="opacity: 0.25;" 
				cx="12" 
				cy="12" 
				r="10" 
				stroke="currentColor" 
				stroke-width="4"
			></circle>
			<path 
				style="opacity: 0.75;" 
				fill="currentColor" 
				d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
			></path>
		</svg>
	{/if}
	{@render children()}
</button>

<style>
	@keyframes spin {
		from { transform: rotate(0deg); }
		to { transform: rotate(360deg); }
	}
</style>
