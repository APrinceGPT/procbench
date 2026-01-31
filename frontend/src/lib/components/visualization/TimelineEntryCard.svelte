<script lang="ts">
  import type { TimelineEntry } from '$lib/api/types';
  import { getRiskLevel } from '$lib/api/types';
  import { colors } from '$lib/styles/design-tokens';

  // ==========================================================================
  // PROPS
  // ==========================================================================

  interface Props {
    entry: TimelineEntry | null;
    onClose?: () => void;
  }

  let { entry, onClose }: Props = $props();

  // ==========================================================================
  // DERIVED STATE
  // ==========================================================================

  const riskLevel = $derived(entry ? getRiskLevel(entry.risk_score) : 'none');

  const riskColor = $derived(
    entry
      ? entry.risk_score >= 50
        ? colors.risk.high
        : entry.risk_score >= 20
          ? colors.risk.medium
          : entry.risk_score > 0
            ? colors.risk.low
            : colors.status.success
      : colors.text.muted
  );

  const riskBgColor = $derived(
    entry
      ? entry.risk_score >= 50
        ? colors.risk.highBg
        : entry.risk_score >= 20
          ? colors.risk.mediumBg
          : entry.risk_score > 0
            ? 'rgba(234, 179, 8, 0.15)'
            : colors.status.successBg
      : 'rgba(107, 114, 128, 0.15)'
  );
</script>

<!-- ========================================================================== -->
<!-- TEMPLATE -->
<!-- ========================================================================== -->

{#if entry}
  <div class="entry-card">
    <!-- Header -->
    <div class="card-header">
      <div class="header-content">
        <div class="title-row">
          <h3 class="process-name">{entry.process_name}</h3>
          {#if entry.is_anomaly}
            <span class="anomaly-badge">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path>
                <line x1="12" y1="9" x2="12" y2="13"></line>
                <line x1="12" y1="17" x2="12.01" y2="17"></line>
              </svg>
              Anomaly
            </span>
          {/if}
        </div>
        <span class="pid-badge">PID: {entry.pid}</span>
      </div>
      <button class="close-btn" onclick={onClose} title="Close">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <line x1="18" y1="6" x2="6" y2="18"></line>
          <line x1="6" y1="6" x2="18" y2="18"></line>
        </svg>
      </button>
    </div>

    <!-- Risk Score -->
    <div class="risk-section">
      <div class="risk-display" style="--risk-color: {riskColor}; --risk-bg: {riskBgColor};">
        <div class="risk-score-value">{entry.risk_score}</div>
        <div class="risk-label">{riskLevel} Risk</div>
      </div>
      {#if entry.timestamp}
        <div class="timestamp">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="10"></circle>
            <polyline points="12 6 12 12 16 14"></polyline>
          </svg>
          {entry.timestamp}
        </div>
      {/if}
    </div>

    <!-- Description -->
    <div class="description-section">
      <h4 class="section-title">Description</h4>
      <p class="description">{entry.description}</p>
    </div>
  </div>
{:else}
  <div class="empty-card">
    <div class="empty-icon">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
        <rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>
        <line x1="16" y1="2" x2="16" y2="6"></line>
        <line x1="8" y1="2" x2="8" y2="6"></line>
        <line x1="3" y1="10" x2="21" y2="10"></line>
      </svg>
    </div>
    <p class="empty-text">Select an event from the chart to view details</p>
  </div>
{/if}

<!-- ========================================================================== -->
<!-- STYLES -->
<!-- ========================================================================== -->

<style>
  .entry-card {
    background: var(--glass-bg, rgba(255, 255, 255, 0.03));
    border-radius: 12px;
    border: 1px solid var(--glass-border, rgba(255, 255, 255, 0.08));
    overflow: hidden;
  }

  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    padding: 16px;
    background: rgba(0, 0, 0, 0.2);
    border-bottom: 1px solid rgba(255, 255, 255, 0.08);
  }

  .header-content {
    display: flex;
    flex-direction: column;
    gap: 8px;
    min-width: 0;
  }

  .title-row {
    display: flex;
    align-items: center;
    gap: 10px;
    flex-wrap: wrap;
  }

  .process-name {
    margin: 0;
    font-size: 16px;
    font-weight: 600;
    color: white;
  }

  .anomaly-badge {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    padding: 3px 8px;
    background: rgba(239, 68, 68, 0.15);
    border: 1px solid rgba(239, 68, 68, 0.3);
    border-radius: 4px;
    font-size: 11px;
    font-weight: 600;
    color: #ef4444;
  }

  .anomaly-badge svg {
    width: 12px;
    height: 12px;
  }

  .pid-badge {
    display: inline-flex;
    padding: 2px 8px;
    background: rgba(255, 255, 255, 0.1);
    border-radius: 4px;
    font-size: 12px;
    font-family: monospace;
    color: rgba(255, 255, 255, 0.7);
    width: fit-content;
  }

  .close-btn {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 28px;
    height: 28px;
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 6px;
    color: rgba(255, 255, 255, 0.6);
    cursor: pointer;
    flex-shrink: 0;
    transition: all 0.2s ease;
  }

  .close-btn:hover {
    background: rgba(239, 68, 68, 0.2);
    border-color: rgba(239, 68, 68, 0.3);
    color: #ef4444;
  }

  .close-btn svg {
    width: 14px;
    height: 14px;
  }

  .risk-section {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
    padding: 16px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.05);
  }

  .risk-display {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 12px 20px;
    background: var(--risk-bg);
    border-radius: 8px;
    border: 1px solid var(--risk-color);
    min-width: 80px;
  }

  .risk-score-value {
    font-size: 24px;
    font-weight: 700;
    color: var(--risk-color);
    line-height: 1;
  }

  .risk-label {
    font-size: 11px;
    color: var(--risk-color);
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-top: 4px;
  }

  .timestamp {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 8px 12px;
    background: rgba(255, 255, 255, 0.05);
    border-radius: 6px;
    font-size: 13px;
    color: rgba(255, 255, 255, 0.7);
  }

  .timestamp svg {
    width: 16px;
    height: 16px;
    color: rgba(255, 255, 255, 0.5);
  }

  .description-section {
    padding: 16px;
  }

  .section-title {
    margin: 0 0 8px 0;
    font-size: 12px;
    font-weight: 600;
    color: rgba(255, 255, 255, 0.5);
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }

  .description {
    margin: 0;
    font-size: 14px;
    color: rgba(255, 255, 255, 0.8);
    line-height: 1.5;
  }

  /* Empty State */
  .empty-card {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 32px 24px;
    background: var(--glass-bg, rgba(255, 255, 255, 0.03));
    border-radius: 12px;
    border: 1px solid var(--glass-border, rgba(255, 255, 255, 0.08));
  }

  .empty-icon {
    width: 40px;
    height: 40px;
    color: rgba(255, 255, 255, 0.2);
    margin-bottom: 12px;
  }

  .empty-icon svg {
    width: 100%;
    height: 100%;
  }

  .empty-text {
    margin: 0;
    text-align: center;
    font-size: 13px;
    color: rgba(255, 255, 255, 0.4);
  }
</style>
