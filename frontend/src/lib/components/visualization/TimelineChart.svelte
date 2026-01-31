<script lang="ts">
  import { onMount, onDestroy } from 'svelte';
  import { Chart, registerables } from 'chart.js';
  import type { TimelineEntry } from '$lib/api/types';
  import { colors } from '$lib/styles/design-tokens';

  // Register Chart.js components
  Chart.register(...registerables);

  // ==========================================================================
  // PROPS
  // ==========================================================================

  interface Props {
    entries: TimelineEntry[];
    onEntrySelect?: (entry: TimelineEntry | null) => void;
  }

  let { entries, onEntrySelect }: Props = $props();

  // ==========================================================================
  // STATE
  // ==========================================================================

  let canvasRef: HTMLCanvasElement | null = $state(null);
  let chart: Chart | null = $state(null);
  let selectedIndex: number | null = $state(null);

  // ==========================================================================
  // COMPUTED DATA
  // ==========================================================================

  interface ChartData {
    labels: string[];
    riskScores: number[];
    backgroundColors: string[];
    borderColors: string[];
    processNames: string[];
    pids: number[];
    isAnomalies: boolean[];
    descriptions: string[];
  }

  function prepareChartData(data: TimelineEntry[]): ChartData {
    const labels: string[] = [];
    const riskScores: number[] = [];
    const backgroundColors: string[] = [];
    const borderColors: string[] = [];
    const processNames: string[] = [];
    const pids: number[] = [];
    const isAnomalies: boolean[] = [];
    const descriptions: string[] = [];

    data.forEach((entry, index) => {
      labels.push(entry.timestamp ?? `Event ${index + 1}`);
      riskScores.push(entry.risk_score);
      processNames.push(entry.process_name);
      pids.push(entry.pid);
      isAnomalies.push(entry.is_anomaly);
      descriptions.push(entry.description);

      const { bg, border } = getRiskColors(entry.risk_score, entry.is_anomaly);
      backgroundColors.push(bg);
      borderColors.push(border);
    });

    return {
      labels,
      riskScores,
      backgroundColors,
      borderColors,
      processNames,
      pids,
      isAnomalies,
      descriptions,
    };
  }

  function getRiskColors(score: number, isAnomaly: boolean): { bg: string; border: string } {
    if (isAnomaly || score >= 50) {
      return {
        bg: 'rgba(239, 68, 68, 0.6)',
        border: colors.risk.high,
      };
    }
    if (score >= 20) {
      return {
        bg: 'rgba(249, 115, 22, 0.6)',
        border: colors.risk.medium,
      };
    }
    if (score > 0) {
      return {
        bg: 'rgba(234, 179, 8, 0.6)',
        border: colors.risk.low,
      };
    }
    return {
      bg: 'rgba(107, 114, 128, 0.6)',
      border: colors.text.muted,
    };
  }

  // ==========================================================================
  // CHART INITIALIZATION
  // ==========================================================================

  function initChart(): void {
    if (!canvasRef) return;
    if (chart) chart.destroy();

    const ctx = canvasRef.getContext('2d');
    if (!ctx) return;

    const chartData = prepareChartData(entries);

    chart = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: chartData.labels,
        datasets: [
          {
            label: 'Risk Score',
            data: chartData.riskScores,
            backgroundColor: chartData.backgroundColors,
            borderColor: chartData.borderColors,
            borderWidth: 2,
            borderRadius: 4,
            barThickness: 'flex',
            maxBarThickness: 40,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        interaction: {
          mode: 'index',
          intersect: false,
        },
        onClick: (_event, elements) => {
          if (elements.length > 0) {
            const index = elements[0].index;
            selectedIndex = index;
            onEntrySelect?.(entries[index] ?? null);
          } else {
            selectedIndex = null;
            onEntrySelect?.(null);
          }
        },
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
            titleFont: {
              size: 14,
              weight: 'bold',
            },
            bodyFont: {
              size: 12,
            },
            callbacks: {
              title: (items) => {
                const index = items[0].dataIndex;
                return chartData.processNames[index];
              },
              label: (context) => {
                const index = context.dataIndex;
                return [
                  `PID: ${chartData.pids[index]}`,
                  `Risk Score: ${context.parsed.y}`,
                  chartData.isAnomalies[index] ? '⚠️ Anomaly Detected' : '',
                ].filter(Boolean);
              },
              afterLabel: (context) => {
                const index = context.dataIndex;
                const desc = chartData.descriptions[index];
                return desc.length > 50 ? desc.slice(0, 50) + '...' : desc;
              },
            },
          },
        },
        scales: {
          x: {
            display: true,
            grid: {
              color: 'rgba(255, 255, 255, 0.05)',
              drawOnChartArea: true,
            },
            ticks: {
              color: 'rgba(255, 255, 255, 0.5)',
              font: {
                size: 10,
              },
              maxRotation: 45,
              minRotation: 45,
              maxTicksLimit: 20,
            },
            border: {
              color: 'rgba(255, 255, 255, 0.1)',
            },
          },
          y: {
            display: true,
            beginAtZero: true,
            max: 100,
            grid: {
              color: 'rgba(255, 255, 255, 0.05)',
            },
            ticks: {
              color: 'rgba(255, 255, 255, 0.5)',
              font: {
                size: 11,
              },
              stepSize: 25,
              callback: (value) => `${value}`,
            },
            border: {
              color: 'rgba(255, 255, 255, 0.1)',
            },
            title: {
              display: true,
              text: 'Risk Score',
              color: 'rgba(255, 255, 255, 0.6)',
              font: {
                size: 12,
                weight: 'normal',
              },
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

  $effect(() => {
    if (entries && canvasRef) {
      initChart();
    }
  });

  onMount(() => {
    if (canvasRef && entries.length > 0) {
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

<div class="timeline-chart-container">
  <div class="chart-header">
    <h3 class="chart-title">Risk Score Timeline</h3>
    <p class="chart-subtitle">Click on bars to view event details</p>
  </div>

  <div class="chart-wrapper">
    <canvas bind:this={canvasRef}></canvas>
  </div>

  <div class="chart-legend">
    <div class="legend-item">
      <span class="legend-bar high"></span>
      <span>High Risk / Anomaly</span>
    </div>
    <div class="legend-item">
      <span class="legend-bar medium"></span>
      <span>Medium Risk</span>
    </div>
    <div class="legend-item">
      <span class="legend-bar low"></span>
      <span>Low Risk</span>
    </div>
    <div class="legend-item">
      <span class="legend-bar none"></span>
      <span>No Risk</span>
    </div>
  </div>
</div>

<!-- ========================================================================== -->
<!-- STYLES -->
<!-- ========================================================================== -->

<style>
  .timeline-chart-container {
    display: flex;
    flex-direction: column;
    height: 100%;
    background: var(--glass-bg, rgba(255, 255, 255, 0.03));
    border-radius: 12px;
    border: 1px solid var(--glass-border, rgba(255, 255, 255, 0.08));
    overflow: hidden;
  }

  .chart-header {
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

  .chart-subtitle {
    margin: 4px 0 0 0;
    font-size: 12px;
    color: rgba(255, 255, 255, 0.5);
  }

  .chart-wrapper {
    flex: 1;
    padding: 16px;
    min-height: 300px;
  }

  .chart-legend {
    display: flex;
    justify-content: center;
    gap: 24px;
    padding: 12px 16px;
    background: rgba(0, 0, 0, 0.2);
    border-top: 1px solid rgba(255, 255, 255, 0.08);
    flex-wrap: wrap;
  }

  .legend-item {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 12px;
    color: rgba(255, 255, 255, 0.6);
  }

  .legend-bar {
    width: 16px;
    height: 12px;
    border-radius: 2px;
    border-width: 2px;
    border-style: solid;
  }

  .legend-bar.high {
    background: rgba(239, 68, 68, 0.6);
    border-color: #ef4444;
  }

  .legend-bar.medium {
    background: rgba(249, 115, 22, 0.6);
    border-color: #f97316;
  }

  .legend-bar.low {
    background: rgba(234, 179, 8, 0.6);
    border-color: #eab308;
  }

  .legend-bar.none {
    background: rgba(107, 114, 128, 0.6);
    border-color: #6b7280;
  }
</style>
