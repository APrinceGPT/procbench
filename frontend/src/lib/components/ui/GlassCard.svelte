<script lang="ts">
	/**
	 * GlassCard Component
	 * 
	 * A reusable card component with glass morphism styling.
	 * Provides consistent visual hierarchy across the application.
	 */

	import { colors, borders, spacing, animation } from '$lib/styles/design-tokens';

	interface Props {
		variant?: 'default' | 'elevated' | 'interactive' | 'subtle';
		padding?: 'none' | 'sm' | 'md' | 'lg' | 'xl';
		rounded?: 'md' | 'lg' | 'xl' | '2xl';
		hover?: boolean;
		glow?: boolean;
		glowColor?: 'primary' | 'success' | 'danger' | 'warning';
		class?: string;
		children: import('svelte').Snippet;
	}

	let {
		variant = 'default',
		padding = 'lg',
		rounded = 'xl',
		hover = false,
		glow = false,
		glowColor = 'primary',
		class: className = '',
		children
	}: Props = $props();

	const paddingMap: Record<string, string> = {
		none: '0',
		sm: spacing.sm,
		md: spacing.md,
		lg: spacing.lg,
		xl: spacing.xl,
	};

	const roundedMap: Record<string, string> = {
		md: borders.radius.md,
		lg: borders.radius.lg,
		xl: borders.radius.xl,
		'2xl': borders.radius['2xl'],
	};

	const variantStyles: Record<string, string> = {
		default: `
			background: ${colors.glass.background};
			backdrop-filter: blur(12px);
			-webkit-backdrop-filter: blur(12px);
			border: 1px solid ${colors.glass.border};
		`,
		elevated: `
			background: rgba(255, 255, 255, 0.05);
			backdrop-filter: blur(16px);
			-webkit-backdrop-filter: blur(16px);
			border: 1px solid rgba(255, 255, 255, 0.1);
			box-shadow: 0 10px 15px rgba(0, 0, 0, 0.3);
		`,
		interactive: `
			background: ${colors.glass.background};
			backdrop-filter: blur(12px);
			-webkit-backdrop-filter: blur(12px);
			border: 1px solid ${colors.glass.border};
			cursor: pointer;
		`,
		subtle: `
			background: rgba(255, 255, 255, 0.02);
			backdrop-filter: blur(4px);
			-webkit-backdrop-filter: blur(4px);
			border: 1px solid rgba(255, 255, 255, 0.05);
		`,
	};

	const glowColors: Record<string, string> = {
		primary: '0 0 20px rgba(59, 130, 246, 0.3)',
		success: '0 0 20px rgba(34, 197, 94, 0.3)',
		danger: '0 0 20px rgba(239, 68, 68, 0.3)',
		warning: '0 0 20px rgba(249, 115, 22, 0.3)',
	};

	function getBaseStyle(): string {
		let style = `
			padding: ${paddingMap[padding]};
			border-radius: ${roundedMap[rounded]};
			${variantStyles[variant]}
			transition: all ${animation.duration.normal} ${animation.easing.easeInOut};
		`;
		return style;
	}

	function getHoverStyle(): string {
		if (!hover && variant !== 'interactive') return '';
		return `
			background: ${colors.glass.backgroundHover};
			border-color: ${colors.glass.borderHover};
			transform: translateY(-2px);
			box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
		`;
	}

	function getGlowStyle(): string {
		if (!glow) return '';
		return `box-shadow: ${glowColors[glowColor]};`;
	}
</script>

<div
	role="region"
	class="glass-card {className}"
	style="{getBaseStyle()} {getGlowStyle()}"
	onmouseenter={(e) => {
		if (hover || variant === 'interactive') {
			const target = e.currentTarget as HTMLElement;
			target.style.cssText += getHoverStyle();
		}
	}}
	onmouseleave={(e) => {
		if (hover || variant === 'interactive') {
			const target = e.currentTarget as HTMLElement;
			target.style.cssText = `${getBaseStyle()} ${getGlowStyle()}`;
		}
	}}
>
	{@render children()}
</div>
