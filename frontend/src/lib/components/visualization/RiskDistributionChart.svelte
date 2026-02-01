<script lang="ts">
  import { onMount, onDestroy } from 'svelte';
  import { Chart, registerables } from 'chart.js';
  import type { AnalysisResult } from '$lib/api/types';
  import { colors } from '$lib/styles/design-tokens';

  // Register Chart.js components
  Chart.register(...registerables);

  // ==========================================================================
  // PROPS
  // ==========================================================================

  interface Props {
    result: AnalysisResult;
  }

  let { result }: Props = $props();

  // ==========================================================================
  // STATE
  // ==========================================================================

  let canvasRef: HTMLCanvasElement | null = $state(null);
  let chart: Chart | null = null; // Not reactive - managed manually

  // ==========================================================================
  // COMPUTED DATA
  // ==========================================================================

  const safeCount = $derived(
    result.total_processes - result.high_risk_count - result.medium_risk_count - result.low_risk_count
  );

  const chartData = $derived([
    { label: 'High Risk', value: result.high_risk_count, color: colors.risk.high },
    { label: 'Medium Risk', value: result.medium_risk_count, color: colors.risk.medium },
    { label: 'Low Risk', value: result.low_risk_count, color: colors.risk.low },
    { label: 'Safe', value: Math.max(0, safeCount), color: colors.status.success },
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
      type: 'bar',
      data: {
        labels: chartData.map((d) => d.label),
        datasets: [
          {
            data: chartData.map((d) => d.value),
            backgroundColor: chartData.map((d) => d.color + 'cc'),
            borderColor: chartData.map((d) => d.color),
            borderWidth: 2,
            borderRadius: 6,
            barThickness: 32,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        indexAxis: 'y',
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
                const value = context.parsed.x ?? 0;
                const percent =
                  result.total_processes > 0
                    ? ((value / result.total_processes) * 100).toFixed(1)
                    : '0';
                return `${value} processes (${percent}%)`;
              },
            },
          },
        },
        scales: {
          x: {
            beginAtZero: true,
            grid: {
              color: 'rgba(255, 255, 255, 0.05)',
            },
            ticks: {
              color: 'rgba(255, 255, 255, 0.5)',
              font: { size: 11 },
              stepSize: 1,
            },
            border: {
              color: 'rgba(255, 255, 255, 0.1)',
            },
          },
          y: {
            grid: {
              display: false,
            },
            ticks: {
              color: 'rgba(255, 255, 255, 0.7)',
              font: { size: 12 },
            },
            border: {
              display: false,
            },
          },
        },
        animation: {
          duration: 600,
          easing: 'easeOutQuart',
        },
      },
    });
  }

  // ==========================================================================
  // EFFECTS
  // ==========================================================================

  // Track data changes and re-render chart
  $effect(() => {
    // Read reactive dependencies
    const data = chartData;
    const canvas = canvasRef;
    
    if (canvas && data.length > 0) {
      // Use setTimeout to break out of the reactive context
      setTimeout(() => initChart(), 0);
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

<div class="risk-chart-container">
  <div class="chart-header">
    <h3 class="chart-title">Risk Distribution</h3>
    <span class="total-badge">{result.total_processes} processes</span>
  </div>

  <div class="chart-wrapper">
    <canvas bind:this={canvasRef}></canvas>
  </div>

  <div class="chart-footer">
    {#each chartData as item}
      <div class="stat-item" style="--stat-color: {item.color};">
        <span class="stat-value">{item.value}</span>
        <span class="stat-label">{item.label}</span>
      </div>
    {/each}
  </div>
</div>

<!-- ========================================================================== -->
<!-- STYLES -->
<!-- ========================================================================== -->

<style>
  .risk-chart-container {
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

  .chart-wrapper {
    flex: 1;
    padding: 16px 20px;
    min-height: 160px;
  }

  .chart-footer {
    display: flex;
    justify-content: space-between;
    padding: 12px 20px;
    background: rgba(0, 0, 0, 0.2);
    border-top: 1px solid rgba(255, 255, 255, 0.08);
  }

  .stat-item {
    display: flex;
    flex-direction: column;
    align-items: center;
  }

  .stat-value {
    font-size: 18px;
    font-weight: 700;
    color: var(--stat-color);
  }

  .stat-label {
    font-size: 10px;
    color: rgba(255, 255, 255, 0.5);
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }
</style>
