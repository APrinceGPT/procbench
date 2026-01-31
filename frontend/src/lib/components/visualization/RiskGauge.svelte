<script lang="ts">
  import { getRiskLevel } from '$lib/api/types';
  import { colors, spacing, borders, animation } from '$lib/styles/design-tokens';

  interface Props {
    score: number;
    size?: 'sm' | 'md' | 'lg';
  }

  let { score, size = 'md' }: Props = $props();

  const riskLevel = $derived(getRiskLevel(score));

  const sizeStyles: Record<string, { width: string; height: string; fontSize: string }> = {
    sm: { width: '80px', height: '80px', fontSize: '1.125rem' },
    md: { width: '120px', height: '120px', fontSize: '1.5rem' },
    lg: { width: '160px', height: '160px', fontSize: '2rem' },
  };

  // Calculate rotation for gauge needle (0-100 maps to -90 to 90 degrees)
  const rotation = $derived(Math.min(100, Math.max(0, score)) * 1.8 - 90);

  // Get colors from design tokens based on risk level
  const gaugeColor = $derived(
    score >= 50
      ? colors.risk.high
      : score >= 20
        ? colors.risk.medium
        : score > 0
          ? colors.risk.low
          : colors.status.success
  );

  const labelBgColor = $derived(
    score >= 50
      ? colors.risk.highBg
      : score >= 20
        ? colors.risk.mediumBg
        : colors.status.successBg
  );

  const labelBorderColor = $derived(
    score >= 50
      ? colors.risk.highBorder
      : score >= 20
        ? colors.risk.mediumBorder
        : 'rgba(34, 197, 94, 0.3)'
  );
</script>

<div style="display: flex; flex-direction: column; align-items: center; animation: fadeIn {animation.duration.normal} {animation.easing.easeOut};">
  <div style="position: relative; width: {sizeStyles[size].width}; height: {sizeStyles[size].height};">
    <svg viewBox="0 0 100 70" style="width: 100%; height: 100%;">
      <!-- Glow filter -->
      <defs>
        <filter id="glow" x="-50%" y="-50%" width="200%" height="200%">
          <feGaussianBlur stdDeviation="2" result="coloredBlur"/>
          <feMerge>
            <feMergeNode in="coloredBlur"/>
            <feMergeNode in="SourceGraphic"/>
          </feMerge>
        </filter>
        <linearGradient id="gaugeGradient" x1="0%" y1="0%" x2="100%" y2="0%">
          <stop offset="0%" style="stop-color: {colors.status.success};" />
          <stop offset="50%" style="stop-color: {colors.risk.medium};" />
          <stop offset="100%" style="stop-color: {colors.risk.high};" />
        </linearGradient>
      </defs>
      
      <!-- Background arc (darker glass effect) -->
      <path
        d="M 10 55 A 40 40 0 0 1 90 55"
        fill="none"
        stroke="{colors.glass.border}"
        stroke-width="10"
        stroke-linecap="round"
      />

      <!-- Progress arc with gradient -->
      <path
        d="M 10 55 A 40 40 0 0 1 90 55"
        fill="none"
        stroke={gaugeColor}
        stroke-width="10"
        stroke-linecap="round"
        stroke-dasharray="126"
        stroke-dashoffset={126 - (score / 100) * 126}
        filter="url(#glow)"
        style="transition: all {animation.duration.slow} {animation.easing.easeInOut};"
      />

      <!-- Tick marks -->
      {#each [0, 25, 50, 75, 100] as tick}
        <line
          x1="50"
          y1="15"
          x2="50"
          y2="20"
          stroke="{colors.text.muted}"
          stroke-width="1"
          transform="rotate({tick * 1.8 - 90} 50 55)"
        />
      {/each}

      <!-- Needle -->
      <g transform="rotate({rotation} 50 55)" style="transition: transform {animation.duration.slow} {animation.easing.easeInOut};">
        <line
          x1="50"
          y1="55"
          x2="50"
          y2="22"
          stroke="{colors.text.primary}"
          stroke-width="2"
          stroke-linecap="round"
        />
        <circle cx="50" cy="22" r="3" fill="{gaugeColor}" filter="url(#glow)" />
      </g>

      <!-- Center circle -->
      <circle cx="50" cy="55" r="8" fill="{colors.glass.backgroundHover}" stroke="{colors.glass.border}" stroke-width="2" />
      <circle cx="50" cy="55" r="4" fill="{gaugeColor}" />
    </svg>

    <!-- Score display -->
    <div style="position: absolute; left: 0; right: 0; bottom: -8px; text-align: center;">
      <span style="
        font-weight: 700; 
        font-size: {sizeStyles[size].fontSize}; 
        color: {gaugeColor};
        text-shadow: 0 0 20px {gaugeColor};
      ">{score}</span>
    </div>
  </div>

  <p style="
    margin-top: {spacing.md}; 
    font-size: 0.8rem; 
    font-weight: 600; 
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: {gaugeColor}; 
    background: {labelBgColor}; 
    padding: {spacing.xs} {spacing.md}; 
    border-radius: {borders.radius.full};
    border: 1px solid {labelBorderColor};
  ">
    {riskLevel} Risk
  </p>
</div>

<style>
  @keyframes fadeIn {
    from { opacity: 0; transform: scale(0.95); }
    to { opacity: 1; transform: scale(1); }
  }
</style>
