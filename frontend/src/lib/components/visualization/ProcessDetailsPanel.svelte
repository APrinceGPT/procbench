<script lang="ts">
  import { colors } from '$lib/styles/design-tokens';
  import { getRiskLevel } from '$lib/api/types';
  import type { VisNode } from './graph-utils';

  // ==========================================================================
  // PROPS
  // ==========================================================================

  interface Props {
    node: VisNode | null;
    onClose?: () => void;
  }

  let { node, onClose }: Props = $props();

  // ==========================================================================
  // DERIVED STATE
  // ==========================================================================

  const riskLevel = $derived(node ? getRiskLevel(node.riskScore) : 'none');

  const riskColor = $derived(
    node
      ? node.riskScore >= 50
        ? colors.risk.high
        : node.riskScore >= 20
          ? colors.risk.medium
          : node.riskScore > 0
            ? colors.risk.low
            : colors.status.success
      : colors.text.muted
  );

  const riskBgColor = $derived(
    node
      ? node.riskScore >= 50
        ? colors.risk.highBg
        : node.riskScore >= 20
          ? colors.risk.mediumBg
          : node.riskScore > 0
            ? 'rgba(234, 179, 8, 0.15)'
            : colors.status.successBg
      : 'rgba(107, 114, 128, 0.15)'
  );

  const legitimacyColor = $derived(
    node
      ? node.legitimacy === 'malicious'
        ? colors.risk.high
        : node.legitimacy === 'suspicious'
          ? colors.risk.medium
          : node.legitimacy === 'legitimate'
            ? colors.status.success
            : colors.text.muted
      : colors.text.muted
  );
</script>

<!-- ========================================================================== -->
<!-- TEMPLATE -->
<!-- ========================================================================== -->

{#if node}
  <div class="details-panel">
    <!-- Header -->
    <div class="panel-header">
      <div class="header-content">
        <h3 class="process-name">{node.processName}</h3>
        <span class="pid-badge">PID: {node.id}</span>
      </div>
      <button class="close-btn" onclick={onClose} title="Close Panel">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <line x1="18" y1="6" x2="6" y2="18"></line>
          <line x1="6" y1="6" x2="18" y2="18"></line>
        </svg>
      </button>
    </div>

    <!-- Risk Score -->
    <div class="risk-section">
      <div class="risk-display" style="--risk-color: {riskColor}; --risk-bg: {riskBgColor};">
        <div class="risk-score-value">{node.riskScore}</div>
        <div class="risk-label">{riskLevel} Risk</div>
      </div>
      <div class="legitimacy-badge" style="--legitimacy-color: {legitimacyColor};">
        {node.legitimacy}
      </div>
    </div>

    <!-- Details Section -->
    <div class="details-section">
      <h4 class="section-title">Process Information</h4>

      <div class="detail-row">
        <span class="detail-label">Image Path</span>
        <span class="detail-value path">{node.imagePath ?? 'N/A'}</span>
      </div>

      <div class="detail-row">
        <span class="detail-label">Event Count</span>
        <span class="detail-value">{node.eventCount.toLocaleString()}</span>
      </div>
    </div>

    <!-- Behavior Tags -->
    {#if node.behaviorTags.length > 0}
      <div class="details-section">
        <h4 class="section-title">Behavior Tags</h4>
        <div class="tags-container">
          {#each node.behaviorTags as tag}
            <span class="behavior-tag">{tag}</span>
          {/each}
        </div>
      </div>
    {/if}

    <!-- Actions -->
    <div class="actions-section">
      <button class="action-btn primary" title="View full process details">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
          <circle cx="12" cy="12" r="3"></circle>
        </svg>
        View Details
      </button>
      <button class="action-btn secondary" title="Copy process info">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>
          <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>
        </svg>
        Copy Info
      </button>
    </div>
  </div>
{:else}
  <div class="empty-panel">
    <div class="empty-icon">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
        <circle cx="12" cy="12" r="10"></circle>
        <path d="M12 16v-4"></path>
        <path d="M12 8h.01"></path>
      </svg>
    </div>
    <p class="empty-text">Select a node in the graph to view process details</p>
  </div>
{/if}

<!-- ========================================================================== -->
<!-- STYLES -->
<!-- ========================================================================== -->

<style>
  .details-panel {
    height: 100%;
    display: flex;
    flex-direction: column;
    background: var(--glass-bg, rgba(255, 255, 255, 0.03));
    border-radius: 12px;
    border: 1px solid var(--glass-border, rgba(255, 255, 255, 0.08));
    overflow: hidden;
  }

  .panel-header {
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
    gap: 4px;
    min-width: 0;
  }

  .process-name {
    margin: 0;
    font-size: 16px;
    font-weight: 600;
    color: white;
    word-break: break-word;
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

  .legitimacy-badge {
    padding: 6px 12px;
    background: rgba(255, 255, 255, 0.05);
    border-radius: 6px;
    border: 1px solid rgba(255, 255, 255, 0.1);
    color: var(--legitimacy-color);
    font-size: 13px;
    font-weight: 500;
    text-transform: capitalize;
  }

  .details-section {
    padding: 16px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.05);
  }

  .section-title {
    margin: 0 0 12px 0;
    font-size: 12px;
    font-weight: 600;
    color: rgba(255, 255, 255, 0.5);
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }

  .detail-row {
    display: flex;
    flex-direction: column;
    gap: 4px;
    margin-bottom: 12px;
  }

  .detail-row:last-child {
    margin-bottom: 0;
  }

  .detail-label {
    font-size: 12px;
    color: rgba(255, 255, 255, 0.5);
  }

  .detail-value {
    font-size: 14px;
    color: white;
  }

  .detail-value.path {
    font-size: 12px;
    font-family: monospace;
    word-break: break-all;
    color: rgba(255, 255, 255, 0.8);
    background: rgba(255, 255, 255, 0.03);
    padding: 6px 8px;
    border-radius: 4px;
    border: 1px solid rgba(255, 255, 255, 0.05);
  }

  .tags-container {
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
  }

  .behavior-tag {
    display: inline-block;
    padding: 4px 10px;
    background: rgba(99, 102, 241, 0.15);
    border: 1px solid rgba(99, 102, 241, 0.3);
    border-radius: 4px;
    font-size: 12px;
    color: #a5b4fc;
  }

  .actions-section {
    padding: 16px;
    margin-top: auto;
    display: flex;
    flex-direction: column;
    gap: 8px;
  }

  .action-btn {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    padding: 10px 16px;
    border-radius: 8px;
    font-size: 13px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s ease;
  }

  .action-btn svg {
    width: 16px;
    height: 16px;
  }

  .action-btn.primary {
    background: var(--accent-primary, #3b82f6);
    border: none;
    color: white;
  }

  .action-btn.primary:hover {
    background: var(--accent-hover, #2563eb);
  }

  .action-btn.secondary {
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    color: rgba(255, 255, 255, 0.8);
  }

  .action-btn.secondary:hover {
    background: rgba(255, 255, 255, 0.1);
    color: white;
  }

  /* Empty State */
  .empty-panel {
    height: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 24px;
    background: var(--glass-bg, rgba(255, 255, 255, 0.03));
    border-radius: 12px;
    border: 1px solid var(--glass-border, rgba(255, 255, 255, 0.08));
  }

  .empty-icon {
    width: 48px;
    height: 48px;
    color: rgba(255, 255, 255, 0.2);
    margin-bottom: 16px;
  }

  .empty-icon svg {
    width: 100%;
    height: 100%;
  }

  .empty-text {
    margin: 0;
    text-align: center;
    font-size: 14px;
    color: rgba(255, 255, 255, 0.4);
    max-width: 200px;
  }
</style>
