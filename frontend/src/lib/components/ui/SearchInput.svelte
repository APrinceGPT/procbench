<script lang="ts">
	/**
	 * SearchInput Component
	 * 
	 * Search input with icon, clear button, and loading state.
	 */

	import { colors, borders, spacing, animation } from '$lib/styles/design-tokens';

	interface Props {
		value?: string;
		placeholder?: string;
		loading?: boolean;
		disabled?: boolean;
		size?: 'sm' | 'md' | 'lg';
		class?: string;
		oninput?: (event: Event & { currentTarget: HTMLInputElement }) => void;
		onkeydown?: (event: KeyboardEvent) => void;
		onclear?: () => void;
	}

	let {
		value = $bindable(''),
		placeholder = 'Search...',
		loading = false,
		disabled = false,
		size = 'md',
		class: className = '',
		oninput,
		onkeydown,
		onclear
	}: Props = $props();

	const sizeStyles: Record<string, { height: string; fontSize: string; iconSize: string }> = {
		sm: { height: '2rem', fontSize: '0.75rem', iconSize: '14px' },
		md: { height: '2.5rem', fontSize: '0.875rem', iconSize: '16px' },
		lg: { height: '3rem', fontSize: '1rem', iconSize: '18px' },
	};

	let isFocused = $state(false);

	function getContainerStyle(): string {
		const sizeStyle = sizeStyles[size];
		
		return `
			position: relative;
			display: flex;
			align-items: center;
			height: ${sizeStyle.height};
			background: ${colors.glass.background};
			border: 1px solid ${isFocused ? colors.accent.primary : colors.glass.border};
			border-radius: ${borders.radius.md};
			transition: all ${animation.duration.fast} ${animation.easing.easeInOut};
			opacity: ${disabled ? '0.5' : '1'};
			${isFocused ? `box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);` : ''}
		`;
	}

	function getInputStyle(): string {
		const sizeStyle = sizeStyles[size];
		
		return `
			flex: 1;
			height: 100%;
			padding: 0 ${spacing.sm};
			padding-left: calc(${spacing.sm} + ${sizeStyle.iconSize} + ${spacing.sm});
			padding-right: ${value ? `calc(${spacing.sm} + ${sizeStyle.iconSize} + ${spacing.sm})` : spacing.sm};
			background: transparent;
			border: none;
			color: ${colors.text.primary};
			font-size: ${sizeStyle.fontSize};
			outline: none;
		`;
	}

	function getIconStyle(): string {
		const sizeStyle = sizeStyles[size];
		
		return `
			position: absolute;
			left: ${spacing.sm};
			width: ${sizeStyle.iconSize};
			height: ${sizeStyle.iconSize};
			color: ${colors.text.tertiary};
			pointer-events: none;
		`;
	}

	function getClearButtonStyle(): string {
		const sizeStyle = sizeStyles[size];
		
		return `
			position: absolute;
			right: ${spacing.xs};
			display: flex;
			align-items: center;
			justify-content: center;
			width: calc(${sizeStyle.iconSize} + 8px);
			height: calc(${sizeStyle.iconSize} + 8px);
			background: transparent;
			border: none;
			border-radius: ${borders.radius.sm};
			color: ${colors.text.tertiary};
			cursor: pointer;
			transition: all ${animation.duration.fast} ${animation.easing.easeInOut};
		`;
	}

	function handleClear() {
		value = '';
		onclear?.();
	}
</script>

<div class="search-input {className}" style={getContainerStyle()}>
	<!-- Search Icon -->
	{#if loading}
		<svg style="{getIconStyle()} animation: spin 1s linear infinite;" fill="none" viewBox="0 0 24 24">
			<circle style="opacity: 0.25;" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
			<path style="opacity: 0.75;" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
		</svg>
	{:else}
		<svg style={getIconStyle()} fill="none" viewBox="0 0 24 24" stroke="currentColor">
			<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
		</svg>
	{/if}

	<!-- Input -->
	<input
		type="text"
		bind:value
		{placeholder}
		{disabled}
		style={getInputStyle()}
		onfocus={() => isFocused = true}
		onblur={() => isFocused = false}
		{oninput}
		{onkeydown}
	/>

	<!-- Clear Button -->
	{#if value && !disabled}
		<button
			type="button"
			style={getClearButtonStyle()}
			onclick={handleClear}
			aria-label="Clear search"
		>
			<svg style="width: 14px; height: 14px;" fill="none" viewBox="0 0 24 24" stroke="currentColor">
				<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
			</svg>
		</button>
	{/if}
</div>

<style>
	@keyframes spin {
		from { transform: rotate(0deg); }
		to { transform: rotate(360deg); }
	}

	input::placeholder {
		color: rgba(255, 255, 255, 0.4);
	}
</style>
