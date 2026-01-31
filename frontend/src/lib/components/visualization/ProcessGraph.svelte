<script lang="ts">
  import { onMount } from 'svelte';
  import type { ProcessTreeNode } from '$lib/api/types';
  import { colors, animation } from '$lib/styles/design-tokens';
  import {
    transformTreeToGraph,
    getGraphOptions,
    filterNodes,
    filterEdges,
    searchNodes,
    type VisNode,
    type VisEdge,
    type FilterMode,
  } from './graph-utils';

  // ==========================================================================
  // PROPS
  // ==========================================================================

  interface Props {
    tree: ProcessTreeNode[];
    onNodeSelect?: (node: VisNode | null) => void;
  }

  let { tree, onNodeSelect }: Props = $props();

  // ==========================================================================
  // STATE
  // ==========================================================================

  let containerRef: HTMLDivElement | null = $state(null);
  let network: any = $state(null);
  let allNodes: VisNode[] = $state([]);
  let allEdges: VisEdge[] = $state([]);
  let filterMode: FilterMode = $state('all');
  let searchQuery = $state('');
  let isLoading = $state(true);
  let selectedNodeId: number | null = $state(null);
  let nodeCount = $state(0);
  let edgeCount = $state(0);

  // ==========================================================================
  // DERIVED STATE
  // ==========================================================================

  const filteredData = $derived.by(() => {
    let nodes = filterNodes(allNodes, filterMode);
    if (searchQuery.trim()) {
      nodes = searchNodes(nodes, searchQuery);
    }
    const visibleIds = new Set(nodes.map((n) => n.id));
    const edges = filterEdges(allEdges, visibleIds);
    return { nodes, edges };
  });

  // ==========================================================================
  // VIS-NETWORK INITIALIZATION
  // ==========================================================================

  async function initializeNetwork(): Promise<void> {
    if (!containerRef) return;

    // Wait for vis-network to load
    const vis = (window as any).vis;
    if (!vis) {
      console.error('vis-network library not loaded');
      isLoading = false;
      return;
    }

    // Transform data
    const graphData = transformTreeToGraph(tree);
    allNodes = graphData.nodes;
    allEdges = graphData.edges;
    nodeCount = allNodes.length;
    edgeCount = allEdges.length;

    // Create network
    const container = containerRef;
    const data = {
      nodes: new vis.DataSet(allNodes),
      edges: new vis.DataSet(allEdges),
    };
    const options = getGraphOptions();

    network = new vis.Network(container, data, options);

    // Event handlers
    network.on('click', handleNodeClick);
    network.on('stabilizationIterationsDone', handleStabilizationDone);
    network.on('hoverNode', () => {
      if (container) container.style.cursor = 'pointer';
    });
    network.on('blurNode', () => {
      if (container) container.style.cursor = 'default';
    });
  }

  function handleNodeClick(params: { nodes: number[] }): void {
    if (params.nodes.length > 0) {
      const nodeId = params.nodes[0];
      selectedNodeId = nodeId;
      const node = allNodes.find((n) => n.id === nodeId);
      onNodeSelect?.(node ?? null);
    } else {
      selectedNodeId = null;
      onNodeSelect?.(null);
    }
  }

  function handleStabilizationDone(): void {
    isLoading = false;
    network?.setOptions({ physics: { enabled: false } });
  }

  // ==========================================================================
  // GRAPH CONTROLS
  // ==========================================================================

  function updateNetworkData(): void {
    if (!network) return;

    const vis = (window as any).vis;
    if (!vis) return;

    const data = filteredData;
    network.setData({
      nodes: new vis.DataSet(data.nodes),
      edges: new vis.DataSet(data.edges),
    });

    nodeCount = data.nodes.length;
    edgeCount = data.edges.length;
  }

  function zoomIn(): void {
    if (!network) return;
    const scale = network.getScale();
    network.moveTo({ scale: scale * 1.3, animation: true });
  }

  function zoomOut(): void {
    if (!network) return;
    const scale = network.getScale();
    network.moveTo({ scale: scale / 1.3, animation: true });
  }

  function fitToScreen(): void {
    if (!network) return;
    network.fit({ animation: true });
  }

  function togglePhysics(): void {
    if (!network) return;
    const options = network.getOptionsFromConfigurator();
    const currentPhysics = options?.physics?.enabled ?? false;
    network.setOptions({ physics: { enabled: !currentPhysics } });
  }

  function focusOnNode(nodeId: number): void {
    if (!network) return;
    network.focus(nodeId, {
      scale: 1.5,
      animation: {
        duration: 500,
        easingFunction: 'easeInOutQuad',
      },
    });
    network.selectNodes([nodeId]);
    selectedNodeId = nodeId;
    const node = allNodes.find((n) => n.id === nodeId);
    onNodeSelect?.(node ?? null);
  }

  // ==========================================================================
  // EFFECTS
  // ==========================================================================

  $effect(() => {
    if (filterMode || searchQuery) {
      updateNetworkData();
    }
  });

  onMount(() => {
    // Load vis-network script
    const script = document.createElement('script');
    script.src = '/vis-network.min.js';
    script.onload = () => {
      // Load CSS
      const link = document.createElement('link');
      link.rel = 'stylesheet';
      link.href = '/vis-network.css';
      document.head.appendChild(link);

      // Initialize network after short delay
      setTimeout(initializeNetwork, 100);
    };
    script.onerror = () => {
      console.error('Failed to load vis-network library');
      isLoading = false;
    };
    document.head.appendChild(script);

    return () => {
      if (network) {
        network.destroy();
        network = null;
      }
    };
  });
</script>

<!-- ========================================================================== -->
<!-- TEMPLATE -->
<!-- ========================================================================== -->

<div class="graph-container">
  <!-- Controls Bar -->
  <div class="controls-bar">
    <div class="controls-left">
      <!-- Search -->
      <div class="search-container">
        <svg class="search-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <circle cx="11" cy="11" r="8"></circle>
          <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
        </svg>
        <input
          type="text"
          placeholder="Search processes..."
          bind:value={searchQuery}
          class="search-input"
        />
      </div>

      <!-- Filter Buttons -->
      <div class="filter-buttons">
        <button
          class="filter-btn"
          class:active={filterMode === 'all'}
          onclick={() => (filterMode = 'all')}
        >
          All
        </button>
        <button
          class="filter-btn"
          class:active={filterMode === 'flagged'}
          onclick={() => (filterMode = 'flagged')}
        >
          Flagged
        </button>
        <button
          class="filter-btn high-risk"
          class:active={filterMode === 'high-risk'}
          onclick={() => (filterMode = 'high-risk')}
        >
          High Risk
        </button>
      </div>
    </div>

    <div class="controls-right">
      <!-- Stats -->
      <div class="stats">
        <span class="stat">
          <span class="stat-value">{nodeCount}</span>
          <span class="stat-label">Nodes</span>
        </span>
        <span class="stat">
          <span class="stat-value">{edgeCount}</span>
          <span class="stat-label">Edges</span>
        </span>
      </div>

      <!-- Zoom Controls -->
      <div class="zoom-controls">
        <button class="icon-btn" onclick={zoomIn} title="Zoom In">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="11" cy="11" r="8"></circle>
            <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
            <line x1="11" y1="8" x2="11" y2="14"></line>
            <line x1="8" y1="11" x2="14" y2="11"></line>
          </svg>
        </button>
        <button class="icon-btn" onclick={zoomOut} title="Zoom Out">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="11" cy="11" r="8"></circle>
            <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
            <line x1="8" y1="11" x2="14" y2="11"></line>
          </svg>
        </button>
        <button class="icon-btn" onclick={fitToScreen} title="Fit to Screen">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M8 3H5a2 2 0 0 0-2 2v3"></path>
            <path d="M21 8V5a2 2 0 0 0-2-2h-3"></path>
            <path d="M3 16v3a2 2 0 0 0 2 2h3"></path>
            <path d="M16 21h3a2 2 0 0 0 2-2v-3"></path>
          </svg>
        </button>
        <button class="icon-btn" onclick={togglePhysics} title="Toggle Physics">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="3"></circle>
            <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"></path>
          </svg>
        </button>
      </div>
    </div>
  </div>

  <!-- Graph Area -->
  <div class="graph-area">
    {#if isLoading}
      <div class="loading-overlay">
        <div class="loading-spinner"></div>
        <p>Building process graph...</p>
      </div>
    {/if}
    <div bind:this={containerRef} class="network-container"></div>
  </div>

  <!-- Legend -->
  <div class="legend">
    <div class="legend-item">
      <span class="legend-dot high"></span>
      <span>High Risk (≥50)</span>
    </div>
    <div class="legend-item">
      <span class="legend-dot medium"></span>
      <span>Medium Risk (20-49)</span>
    </div>
    <div class="legend-item">
      <span class="legend-dot low"></span>
      <span>Low Risk (1-19)</span>
    </div>
    <div class="legend-item">
      <span class="legend-dot none"></span>
      <span>No Risk (0)</span>
    </div>
  </div>
</div>

<!-- ========================================================================== -->
<!-- STYLES -->
<!-- ========================================================================== -->

<style>
  .graph-container {
    display: flex;
    flex-direction: column;
    height: 100%;
    background: var(--glass-bg, rgba(255, 255, 255, 0.03));
    border-radius: 12px;
    border: 1px solid var(--glass-border, rgba(255, 255, 255, 0.08));
    overflow: hidden;
  }

  .controls-bar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 12px 16px;
    background: rgba(0, 0, 0, 0.2);
    border-bottom: 1px solid rgba(255, 255, 255, 0.08);
    flex-wrap: wrap;
    gap: 12px;
  }

  .controls-left,
  .controls-right {
    display: flex;
    align-items: center;
    gap: 16px;
  }

  .search-container {
    position: relative;
    display: flex;
    align-items: center;
  }

  .search-icon {
    position: absolute;
    left: 10px;
    width: 16px;
    height: 16px;
    color: rgba(255, 255, 255, 0.4);
    pointer-events: none;
  }

  .search-input {
    padding: 8px 12px 8px 36px;
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 8px;
    color: white;
    font-size: 13px;
    width: 200px;
    transition: all 0.2s ease;
  }

  .search-input::placeholder {
    color: rgba(255, 255, 255, 0.4);
  }

  .search-input:focus {
    outline: none;
    border-color: var(--accent-primary, #3b82f6);
    background: rgba(255, 255, 255, 0.08);
  }

  .filter-buttons {
    display: flex;
    gap: 4px;
  }

  .filter-btn {
    padding: 6px 14px;
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 6px;
    color: rgba(255, 255, 255, 0.7);
    font-size: 12px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s ease;
  }

  .filter-btn:hover {
    background: rgba(255, 255, 255, 0.1);
    color: white;
  }

  .filter-btn.active {
    background: var(--accent-primary, #3b82f6);
    border-color: var(--accent-primary, #3b82f6);
    color: white;
  }

  .filter-btn.high-risk.active {
    background: rgba(239, 68, 68, 0.8);
    border-color: rgba(239, 68, 68, 0.8);
  }

  .stats {
    display: flex;
    gap: 16px;
  }

  .stat {
    display: flex;
    flex-direction: column;
    align-items: center;
  }

  .stat-value {
    font-size: 16px;
    font-weight: 600;
    color: white;
  }

  .stat-label {
    font-size: 10px;
    color: rgba(255, 255, 255, 0.5);
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }

  .zoom-controls {
    display: flex;
    gap: 4px;
  }

  .icon-btn {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 32px;
    height: 32px;
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 6px;
    color: rgba(255, 255, 255, 0.7);
    cursor: pointer;
    transition: all 0.2s ease;
  }

  .icon-btn:hover {
    background: rgba(255, 255, 255, 0.1);
    color: white;
  }

  .icon-btn svg {
    width: 16px;
    height: 16px;
  }

  .graph-area {
    flex: 1;
    position: relative;
    min-height: 400px;
  }

  .network-container {
    width: 100%;
    height: 100%;
  }

  .loading-overlay {
    position: absolute;
    inset: 0;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    background: rgba(0, 0, 0, 0.7);
    z-index: 10;
    gap: 16px;
  }

  .loading-overlay p {
    color: rgba(255, 255, 255, 0.7);
    font-size: 14px;
  }

  .loading-spinner {
    width: 40px;
    height: 40px;
    border: 3px solid rgba(255, 255, 255, 0.1);
    border-top-color: var(--accent-primary, #3b82f6);
    border-radius: 50%;
    animation: spin 1s linear infinite;
  }

  @keyframes spin {
    to {
      transform: rotate(360deg);
    }
  }

  .legend {
    display: flex;
    justify-content: center;
    gap: 24px;
    padding: 12px 16px;
    background: rgba(0, 0, 0, 0.2);
    border-top: 1px solid rgba(255, 255, 255, 0.08);
  }

  .legend-item {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 12px;
    color: rgba(255, 255, 255, 0.6);
  }

  .legend-dot {
    width: 12px;
    height: 12px;
    border-radius: 50%;
    border: 2px solid;
  }

  .legend-dot.high {
    background: rgba(239, 68, 68, 0.3);
    border-color: #ef4444;
  }

  .legend-dot.medium {
    background: rgba(249, 115, 22, 0.3);
    border-color: #f97316;
  }

  .legend-dot.low {
    background: rgba(234, 179, 8, 0.3);
    border-color: #eab308;
  }

  .legend-dot.none {
    background: rgba(107, 114, 128, 0.3);
    border-color: #6b7280;
  }

  /* vis-network overrides */
  :global(.vis-tooltip) {
    background: transparent !important;
    border: none !important;
    padding: 0 !important;
    box-shadow: none !important;
  }
</style>
