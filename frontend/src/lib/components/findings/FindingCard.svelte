<script lang="ts">
  import type { ProcessSummary } from '$lib/api/types';
  import { getRiskLevel } from '$lib/api/types';
  import { uiStore } from '$lib/stores/ui';
  import { colors, spacing, borders, animation, getRiskColors, getLegitimacyColors } from '$lib/styles/design-tokens';

  interface Props {
    process: ProcessSummary;
    compact?: boolean;
  }

  let { process, compact = false }: Props = $props();

  const riskLevel = $derived(getRiskLevel(process.risk_score));
  const riskColors = $derived(getRiskColors(process.risk_score));
  const legitimacyStyles = $derived(getLegitimacyColors(process.legitimacy));

  function handleClick() {
    uiStore.selectProcess(process.pid);
  }
</script>

<button
  style="
    width: 100%; 
    text-align: left; 
    border-left: 4px solid {riskColors.color}; 
    border-radius: {borders.radius.lg}; 
    padding: {compact ? spacing.md : spacing.lg}; 
    background: {colors.glass.background};
    backdrop-filter: blur(8px);
    -webkit-backdrop-filter: blur(8px);
    cursor: pointer; 
    border-top: 1px solid {colors.glass.border}; 
    border-right: 1px solid {colors.glass.border}; 
    border-bottom: 1px solid {colors.glass.border};
    transition: all {animation.duration.normal} {animation.easing.easeInOut};
  "
  onclick={handleClick}
  onmouseenter={(e) => {
    const el = e.currentTarget as HTMLElement;
    el.style.background = colors.glass.backgroundHover;
    el.style.borderColor = riskColors.color;
    el.style.transform = 'translateX(4px)';
    el.style.boxShadow = `0 0 20px ${riskColors.color}22`;
  }}
  onmouseleave={(e) => {
    const el = e.currentTarget as HTMLElement;
    el.style.background = colors.glass.background;
    el.style.borderColor = colors.glass.border;
    el.style.borderLeftColor = riskColors.color;
    el.style.transform = 'translateX(0)';
    el.style.boxShadow = 'none';
  }}
>
  <div style="display: flex; align-items: flex-start; justify-content: space-between;">
    <div style="flex: 1; min-width: 0;">
      <div style="display: flex; align-items: center; gap: {spacing.sm};">
        <h4 style="font-weight: 600; color: {colors.text.primary}; margin: 0; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">
          {process.process_name}
        </h4>
        <span style="font-size: 0.7rem; color: {colors.text.muted}; font-family: monospace; background: {colors.glass.backgroundHover}; padding: 2px 6px; border-radius: {borders.radius.sm};">
          PID: {process.pid}
        </span>
      </div>

      {#if !compact && process.image_path}
        <p
          style="font-size: 0.8rem; color: {colors.text.tertiary}; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; margin: {spacing.xs} 0 0 0; font-family: monospace;"
          title={process.image_path}
        >
          {process.image_path}
        </p>
      {/if}

      {#if process.matched_rules.length > 0}
        <div style="display: flex; flex-wrap: wrap; gap: {spacing.xs}; margin-top: {spacing.sm};">
          {#each process.matched_rules.slice(0, compact ? 2 : 5) as rule}
            <span style="
              display: inline-flex; 
              align-items: center; 
              padding: 2px {spacing.sm}; 
              border-radius: {borders.radius.sm}; 
              font-size: 0.7rem; 
              font-weight: 500; 
              background: {colors.glass.backgroundHover}; 
              color: {colors.text.secondary};
              border: 1px solid {colors.glass.border};
            ">
              {rule}
            </span>
          {/each}
          {#if process.matched_rules.length > (compact ? 2 : 5)}
            <span style="font-size: 0.7rem; color: {colors.text.muted};">
              +{process.matched_rules.length - (compact ? 2 : 5)} more
            </span>
          {/if}
        </div>
      {/if}
    </div>

    <div style="display: flex; flex-direction: column; align-items: flex-end; margin-left: {spacing.md}; flex-shrink: 0; gap: {spacing.sm};">
      <!-- Risk Score Badge -->
      <span
        style="
          padding: {spacing.xs} {spacing.sm}; 
          border-radius: {borders.radius.md}; 
          font-size: 0.9rem; 
          font-weight: 700;
          color: {riskColors.color};
          background: {riskColors.bg};
          border: 1px solid {riskColors.border};
          min-width: 40px;
          text-align: center;
          text-shadow: 0 0 10px {riskColors.color}44;
        "
      >
        {process.risk_score}
      </span>

      <!-- Legitimacy Badge -->
      <span
        style="
          padding: 2px {spacing.sm}; 
          border-radius: {borders.radius.full}; 
          font-size: 0.65rem; 
          font-weight: 600; 
          text-transform: uppercase;
          letter-spacing: 0.05em;
          color: {legitimacyStyles.color}; 
          background: {legitimacyStyles.bg};
          border: 1px solid {legitimacyStyles.border};
        "
      >
        {process.legitimacy}
      </span>
    </div>
  </div>

  {#if !compact && process.behavior_tags.length > 0}
    <div style="display: flex; flex-wrap: wrap; gap: {spacing.xs}; margin-top: {spacing.md}; padding-top: {spacing.md}; border-top: 1px solid {colors.glass.border};">
      {#each process.behavior_tags as tag}
        <span style="
          display: inline-flex; 
          align-items: center; 
          padding: 2px {spacing.sm}; 
          border-radius: {borders.radius.sm}; 
          font-size: 0.7rem; 
          font-weight: 500; 
          background: rgba(139, 92, 246, 0.15); 
          color: {colors.accent.secondary};
          border: 1px solid rgba(139, 92, 246, 0.3);
        ">
          {tag}
        </span>
      {/each}
    </div>
  {/if}

  {#if !compact && process.ai_reasoning}
    <div style="margin-top: {spacing.md}; padding-top: {spacing.md}; border-top: 1px solid {colors.glass.border};">
      <p style="display: flex; align-items: center; gap: {spacing.xs}; font-weight: 600; color: {colors.accent.primary}; margin: 0 0 {spacing.xs} 0; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.05em;">
        <svg style="width: 14px; height: 14px;" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
        </svg>
        AI Analysis
      </p>
      <p style="font-style: italic; margin: 0; color: {colors.text.tertiary}; font-size: 0.85rem; line-height: 1.5;">{process.ai_reasoning}</p>
    </div>
  {/if}
</button>
