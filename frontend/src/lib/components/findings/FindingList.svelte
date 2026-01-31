<script lang="ts">
  import type { ProcessSummary } from '$lib/api/types';
  import FindingCard from './FindingCard.svelte';
  import { colors, spacing, animation } from '$lib/styles/design-tokens';

  interface Props {
    processes: ProcessSummary[];
    title?: string;
    emptyMessage?: string;
    compact?: boolean;
    maxItems?: number | null;
  }

  let { 
    processes, 
    title = 'Findings', 
    emptyMessage = 'No findings to display', 
    compact = false, 
    maxItems = null 
  }: Props = $props();

  let showAll = $state(false);

  const displayProcesses = $derived(
    showAll || maxItems === null ? processes : processes.slice(0, maxItems)
  );
  const hasMore = $derived(maxItems !== null && !showAll && processes.length > maxItems);
</script>

<div style="width: 100%;">
  <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: {spacing.md};">
    <h3 style="display: flex; align-items: center; gap: {spacing.sm}; font-size: 1rem; font-weight: 600; color: {colors.text.primary}; margin: 0;">
      <svg style="width: 18px; height: 18px; color: {colors.risk.high};" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
      </svg>
      {title}
    </h3>
    <span style="
      font-size: 0.75rem; 
      color: {colors.text.tertiary};
      background: {colors.glass.backgroundHover};
      padding: {spacing.xs} {spacing.sm};
      border-radius: 9999px;
    ">
      {processes.length} {processes.length === 1 ? 'process' : 'processes'}
    </span>
  </div>

  {#if displayProcesses.length === 0}
    <div style="
      text-align: center; 
      padding: {spacing['2xl']} {spacing.lg}; 
      color: {colors.text.tertiary};
      background: {colors.glass.background};
      border-radius: 12px;
      border: 1px solid {colors.glass.border};
    ">
      <svg
        style="margin: 0 auto; width: 48px; height: 48px; color: {colors.status.success};"
        fill="none"
        stroke="currentColor"
        viewBox="0 0 24 24"
      >
        <path
          stroke-linecap="round"
          stroke-linejoin="round"
          stroke-width="2"
          d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
        />
      </svg>
      <p style="margin-top: {spacing.md}; font-weight: 500;">{emptyMessage}</p>
    </div>
  {:else}
    <div style="display: flex; flex-direction: column; gap: {spacing.sm};">
      {#each displayProcesses as process, i (process.pid)}
        <div style="animation: fadeInUp {animation.duration.normal} {animation.easing.easeOut}; animation-delay: {i * 50}ms; animation-fill-mode: backwards;">
          <FindingCard {process} {compact} />
        </div>
      {/each}
    </div>

    {#if hasMore}
      <div style="margin-top: {spacing.md}; text-align: center;">
        <button
          style="
            color: {colors.accent.primary}; 
            background: {colors.glass.background}; 
            border: 1px solid {colors.glass.border}; 
            cursor: pointer; 
            font-size: 0.875rem; 
            font-weight: 500;
            padding: {spacing.sm} {spacing.lg};
            border-radius: 9999px;
            transition: all {animation.duration.fast} {animation.easing.easeInOut};
          "
          onclick={() => showAll = true}
          onmouseenter={(e) => {
            const el = e.currentTarget as HTMLElement;
            el.style.background = colors.glass.backgroundHover;
            el.style.borderColor = colors.accent.primary;
          }}
          onmouseleave={(e) => {
            const el = e.currentTarget as HTMLElement;
            el.style.background = colors.glass.background;
            el.style.borderColor = colors.glass.border;
          }}
        >
          Show all {processes.length} processes →
        </button>
      </div>
    {/if}
  {/if}
</div>

<style>
  @keyframes fadeInUp {
    from {
      opacity: 0;
      transform: translateY(8px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }
</style>
