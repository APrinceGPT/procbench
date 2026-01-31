<script lang="ts">
  import { onMount, onDestroy } from 'svelte';
  import { Chart, registerables } from 'chart.js';
  import type { ProcessSummary } from '$lib/api/types';
  import { colors } from '$lib/styles/design-tokens';

  // Register Chart.js components
  Chart.register(...registerables);

  // ==========================================================================
  // PROPS
  // ==========================================================================

  interface Props {
    processes: ProcessSummary[];
  }

  let { processes }: Props = $props();

  // ==========================================================================
  // STATE
  // ==========================================================================

  let canvasRef: HTMLCanvasElement | null = $state(null);
  let chart: Chart | null = $state(null);

  // ==========================================================================
  // COMPUTED DATA
  // ==========================================================================

  interface OperationStats {
    file: number;
    registry: number;
    network: number;
    process: number;
    total: number;
  }

  const operationStats = $derived.by(() => {
    let file = 0;
    let registry = 0;
    let network = 0;
    let process = 0;

    for (const p of processes) {
      file += p.file_operations;
      registry += p.registry_operations;
      network += p.network_operations;
      // Estimate process operations as event_count minus file/registry/network
      const processOps = Math.max(0, p.event_count - p.file_operations - p.registry_operations - p.network_operations);
      process += processOps;
    }

    return {
      file,
      registry,
      network,
      process,
      total: file + registry + network + process,
    };
  });

  const chartData = $derived([
    { label: 'File Operations', value: operationStats.file, color: '#3b82f6' },
    { label: 'Registry Operations', value: operationStats.registry, color: '#8b5cf6' },
    { label: 'Network Operations', value: operationStats.network, color: '#06b6d4' },
    { label: 'Process Operations', value: operationStats.process, color: '#f97316' },
  ]);

  // ==========================================================================
  // CHART INITIALIZATION
  // ==========================================================================

  function initChart(): void {
    if (!canvasRef) return;
    if (chart) chart.destroy();

    const ctx = canvasRef.getContext('2d');
    if (!ctx) return;

    chart = new Chart(ctx, {
      type: 'doughnut',
      data: {
        labels: chartData.map((d) => d.label),
        datasets: [
          {
            data: chartData.map((d) => d.value),
            backgroundColor: chartData.map((d) => d.color + 'cc'),
            borderColor: chartData.map((d) => d.color),
            borderWidth: 2,
            hoverOffset: 8,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        cutout: '65%',
        plugins: {
          legend: {
            display: false,
          },
          tooltip: {
            enabled: true,
            backgroundColor: 'rgba(10, 10, 15, 0.95)',
            titleColor: '#ffffff',
            bodyColor: 'rgba(255, 255, 255, 0.8)',
            borderColor: 'rgba(255, 255, 255, 0.1)',
            borderWidth: 1,
            padding: 12,
            cornerRadius: 8,
            callbacks: {
              label: (context) => {
                const value = context.parsed;
                const total = operationStats.total;
                const percent = total > 0 ? ((value / total) * 100).toFixed(1) : '0';
                return `${value.toLocaleString()} (${percent}%)`;
              },
            },
          },
        },
        animation: {
          animateRotate: true,
          animateScale: true,
          duration: 800,
          easing: 'easeOutQuart',
        },
      },
    });
  }

  // ==========================================================================
  // EFFECTS
  // ==========================================================================

  $effect(() => {
    if (processes && canvasRef) {
      initChart();
    }
  });

  onMount(() => {
    if (canvasRef && processes.length > 0) {
      initChart();
    }
  });

  onDestroy(() => {
    if (chart) {
      chart.destroy();
      chart = null;
    }
  });
</script>

<!-- ========================================================================== -->
<!-- TEMPLATE -->
<!-- ========================================================================== -->

<div class="activity-chart-container">
  <div class="chart-header">
    <h3 class="chart-title">Activity Distribution</h3>
    <span class="total-badge">{operationStats.total.toLocaleString()} total</span>
  </div>

  <div class="chart-content">
    <div class="chart-wrapper">
      <canvas bind:this={canvasRef}></canvas>
      <div class="chart-center">
        <span class="center-value">{processes.length}</span>
        <span class="center-label">Processes</span>
      </div>
    </div>

    <div class="legend">
      {#each chartData as item}
        <div class="legend-item">
          <div class="legend-color" style="background-color: {item.color};"></div>
          <div class="legend-content">
            <span class="legend-label">{item.label}</span>
            <span class="legend-value">{item.value.toLocaleString()}</span>
          </div>
        </div>
      {/each}
    </div>
  </div>
</div>

<!-- ========================================================================== -->
<!-- STYLES -->
<!-- ========================================================================== -->

<style>
  .activity-chart-container {
    display: flex;
    flex-direction: column;
    height: 100%;
    background: var(--glass-bg, rgba(255, 255, 255, 0.03));
    border-radius: 12px;
    border: 1px solid var(--glass-border, rgba(255, 255, 255, 0.08));
    overflow: hidden;
  }

  .chart-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 16px 20px;
    background: rgba(0, 0, 0, 0.2);
    border-bottom: 1px solid rgba(255, 255, 255, 0.08);
  }

  .chart-title {
    margin: 0;
    font-size: 14px;
    font-weight: 600;
    color: white;
  }

  .total-badge {
    padding: 4px 10px;
    background: rgba(255, 255, 255, 0.1);
    border-radius: 12px;
    font-size: 12px;
    color: rgba(255, 255, 255, 0.7);
  }

  .chart-content {
    flex: 1;
    display: flex;
    padding: 20px;
    gap: 24px;
  }

  .chart-wrapper {
    position: relative;
    flex: 1;
    min-width: 160px;
    max-width: 200px;
  }

  .chart-center {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
  }

  .center-value {
    font-size: 24px;
    font-weight: 700;
    color: white;
    line-height: 1;
  }

  .center-label {
    font-size: 11px;
    color: rgba(255, 255, 255, 0.5);
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-top: 4px;
  }

  .legend {
    display: flex;
    flex-direction: column;
    gap: 12px;
    justify-content: center;
  }

  .legend-item {
    display: flex;
    align-items: center;
    gap: 12px;
  }

  .legend-color {
    width: 12px;
    height: 12px;
    border-radius: 3px;
    flex-shrink: 0;
  }

  .legend-content {
    display: flex;
    flex-direction: column;
  }

  .legend-label {
    font-size: 12px;
    color: rgba(255, 255, 255, 0.7);
  }

  .legend-value {
    font-size: 14px;
    font-weight: 600;
    color: white;
  }
</style>
