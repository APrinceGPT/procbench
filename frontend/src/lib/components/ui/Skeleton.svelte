<script lang="ts">
	/**
	 * Skeleton Component
	 * 
	 * Loading placeholder with shimmer animation.
	 */

	import { borders } from '$lib/styles/design-tokens';

	interface Props {
		variant?: 'text' | 'circle' | 'card' | 'custom';
		width?: string;
		height?: string;
		rounded?: 'sm' | 'md' | 'lg' | 'xl' | 'full';
		class?: string;
	}

	let {
		variant = 'text',
		width,
		height,
		rounded = 'md',
		class: className = ''
	}: Props = $props();

	const roundedMap: Record<string, string> = {
		sm: borders.radius.sm,
		md: borders.radius.md,
		lg: borders.radius.lg,
		xl: borders.radius.xl,
		full: borders.radius.full,
	};

	// Use $derived to properly react to prop changes
	const computedStyle = $derived(() => {
		const variantDefaults: Record<string, { width: string; height: string; rounded: string }> = {
			text: { width: '100%', height: '1rem', rounded: borders.radius.md },
			circle: { width: '40px', height: '40px', rounded: borders.radius.full },
			card: { width: '100%', height: '120px', rounded: borders.radius.xl },
			custom: { width: width || '100%', height: height || '1rem', rounded: roundedMap[rounded] },
		};
		
		const defaults = variantDefaults[variant];
		
		return `
			width: ${width || defaults.width};
			height: ${height || defaults.height};
			border-radius: ${variant === 'custom' ? roundedMap[rounded] : defaults.rounded};
			background: linear-gradient(
				90deg,
				rgba(255, 255, 255, 0.03) 0%,
				rgba(255, 255, 255, 0.08) 50%,
				rgba(255, 255, 255, 0.03) 100%
			);
			background-size: 200% 100%;
			animation: shimmer 1.5s infinite;
		`;
	});
</script>

<div class="skeleton {className}" style={computedStyle()}></div>

<style>
	@keyframes shimmer {
		0% {
			background-position: -200% 0;
		}
		100% {
			background-position: 200% 0;
		}
	}
</style>
