<script lang="ts">
  import type { PathHeatmapEntry } from '$lib/api/types';

  interface Props {
    data: PathHeatmapEntry[];
    totalAccesses: number;
    maxItems?: number;
  }

  let { data, totalAccesses, maxItems = 30 }: Props = $props();

  // Type for processed items
  interface ProcessedItem extends PathHeatmapEntry {
    percentage: number;
    intensity: number;
    isRegistry: boolean;
    isSystem: boolean;
    dominantOp: string;
    shortPath: string;
  }
  
  interface LayoutItem extends ProcessedItem {
    width: number;
    height: number;
    index: number;
  }

  // Process data for treemap visualization
  let processedData = $derived((): ProcessedItem[] => {
    if (!data || data.length === 0) return [];

    // Take top items
    const items = data.slice(0, maxItems);

    // Find max access count for color scaling
    const maxAccess = Math.max(...items.map((d) => d.access_count));

    return items.map((item) => {
      // Calculate relative size (percentage of total)
      const percentage = totalAccesses > 0 ? (item.access_count / totalAccesses) * 100 : 0;

      // Calculate color intensity (0-1)
      const intensity = maxAccess > 0 ? item.access_count / maxAccess : 0;

      // Determine path type
      const isRegistry = item.path.startsWith('HK') || item.path.includes('REGISTRY');
      const isSystem =
        item.path.toLowerCase().includes('windows') ||
        item.path.toLowerCase().includes('system32');

      // Get dominant operation type
      const operations = Object.entries(item.operation_types || {});
      const dominantOp = operations.length > 0 ? operations.sort((a, b) => b[1] - a[1])[0][0] : '';

      return {
        ...item,
        percentage,
        intensity,
        isRegistry,
        isSystem,
        dominantOp,
        shortPath: shortenPath(item.path),
      };
    });
  });

  // Shorten long paths for display
  function shortenPath(path: string): string {
    if (path.length <= 40) return path;

    const parts = path.split(/[/\\]/);
    if (parts.length <= 3) return path;

    // Keep first and last parts
    return `${parts[0]}/.../${parts[parts.length - 2]}/${parts[parts.length - 1]}`;
  }

  // Get color based on path type and intensity
  function getColor(item: ProcessedItem): string {
    const baseIntensity = Math.max(0.2, item.intensity);

    if (item.isRegistry) {
      // Purple gradient for registry
      return `rgba(139, 92, 246, ${baseIntensity})`;
    } else if (item.isSystem) {
      // Blue gradient for system paths
      return `rgba(59, 130, 246, ${baseIntensity})`;
    } else {
      // Green gradient for user paths
      return `rgba(34, 197, 94, ${baseIntensity})`;
    }
  }

  // Get text color for contrast
  function getTextColor(intensity: number): string {
    return intensity > 0.5 ? 'text-white' : 'text-gray-800';
  }

  // Format operation type name
  function formatOperation(op: string): string {
    return op
      .replace(/_/g, ' ')
      .toLowerCase()
      .replace(/\b\w/g, (c) => c.toUpperCase());
  }

  // Calculate cell sizes using squarified treemap algorithm (simplified)
  let cellLayout = $derived((): LayoutItem[] => {
    const items = processedData();
    if (items.length === 0) return [];

    // Simple grid-based layout based on percentage
    return items.map((item, index) => {
      // Base size on percentage, but ensure minimum visibility
      const minSize = 60;
      const maxSize = 200;
      const size = Math.max(minSize, Math.min(maxSize, item.percentage * 10 + minSize));

      return {
        ...item,
        width: size,
        height: Math.max(minSize, size * 0.7),
        index,
      };
    });
  });

  // Selected item for detail view
  let selectedItem: LayoutItem | null = $state(null);
</script>

<div class="space-y-4">
  <!-- Legend -->
  <div class="flex items-center justify-between text-sm">
    <div class="flex items-center gap-4">
      <div class="flex items-center gap-1.5">
        <div class="h-3 w-3 rounded bg-purple-500"></div>
        <span class="text-gray-600">Registry</span>
      </div>
      <div class="flex items-center gap-1.5">
        <div class="h-3 w-3 rounded bg-blue-500"></div>
        <span class="text-gray-600">System</span>
      </div>
      <div class="flex items-center gap-1.5">
        <div class="h-3 w-3 rounded bg-green-500"></div>
        <span class="text-gray-600">User</span>
      </div>
    </div>
    <div class="text-gray-500">{data.length} paths · {totalAccesses.toLocaleString()} accesses</div>
  </div>

  <!-- Treemap Grid -->
  <div class="flex min-h-[300px] flex-wrap gap-1 rounded-lg border border-gray-200 bg-gray-50 p-2">
    {#each cellLayout() as cell}
      <button
        type="button"
        class="group relative flex cursor-pointer flex-col justify-between overflow-hidden rounded-md p-2 text-left transition-all duration-200 hover:ring-2 hover:ring-offset-1 focus:ring-2 focus:ring-offset-1 focus:outline-none {cell.isRegistry ? 'hover:ring-purple-400 focus:ring-purple-400' : cell.isSystem ? 'hover:ring-blue-400 focus:ring-blue-400' : 'hover:ring-green-400 focus:ring-green-400'}"
        style="background-color: {getColor(cell)}; min-width: {cell.width}px; min-height: {cell.height}px; flex-grow: {Math.max(1, Math.floor(cell.percentage))};"
        onclick={() => (selectedItem = selectedItem?.path === cell.path ? null : cell)}
      >
        <!-- Path name -->
        <div
          class="line-clamp-2 text-xs font-medium {getTextColor(cell.intensity)}"
          title={cell.path}
        >
          {cell.shortPath}
        </div>

        <!-- Stats -->
        <div class="mt-1 flex items-end justify-between">
          <span class="text-xs font-bold {getTextColor(cell.intensity)}">
            {cell.access_count.toLocaleString()}
          </span>
          <span class="text-xs opacity-75 {getTextColor(cell.intensity)}">
            {cell.percentage.toFixed(1)}%
          </span>
        </div>

        <!-- Hover overlay -->
        <div
          class="pointer-events-none absolute inset-0 bg-black opacity-0 transition-opacity group-hover:opacity-10"
        ></div>
      </button>
    {/each}

    {#if cellLayout().length === 0}
      <div class="flex w-full items-center justify-center py-8 text-gray-500">
        No path access data available
      </div>
    {/if}
  </div>

  <!-- Selected Item Detail -->
  {#if selectedItem}
    <div
      class="rounded-lg border {selectedItem.isRegistry ? 'border-purple-200 bg-purple-50' : selectedItem.isSystem ? 'border-blue-200 bg-blue-50' : 'border-green-200 bg-green-50'} p-4"
    >
      <div class="mb-3 flex items-start justify-between">
        <div>
          <h4 class="font-medium text-gray-900">Path Details</h4>
          <p class="mt-1 break-all font-mono text-sm text-gray-600">{selectedItem.path}</p>
        </div>
        <button
          type="button"
          class="rounded-full p-1 text-gray-400 hover:bg-gray-200 hover:text-gray-600"
          onclick={() => (selectedItem = null)}
          aria-label="Close details"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            class="h-4 w-4"
            viewBox="0 0 20 20"
            fill="currentColor"
          >
            <path
              fill-rule="evenodd"
              d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z"
              clip-rule="evenodd"
            />
          </svg>
        </button>
      </div>

      <div class="grid grid-cols-2 gap-4 text-sm md:grid-cols-4">
        <div>
          <dt class="text-gray-500">Access Count</dt>
          <dd class="mt-1 font-semibold text-gray-900">
            {selectedItem.access_count.toLocaleString()}
          </dd>
        </div>
        <div>
          <dt class="text-gray-500">Percentage</dt>
          <dd class="mt-1 font-semibold text-gray-900">{selectedItem.percentage.toFixed(2)}%</dd>
        </div>
        <div>
          <dt class="text-gray-500">Type</dt>
          <dd class="mt-1 font-semibold text-gray-900">
            {selectedItem.isRegistry ? 'Registry' : selectedItem.isSystem ? 'System' : 'User'}
          </dd>
        </div>
        <div>
          <dt class="text-gray-500">Dominant Operation</dt>
          <dd class="mt-1 font-semibold text-gray-900">
            {formatOperation(selectedItem.dominantOp) || 'N/A'}
          </dd>
        </div>
      </div>

      {#if selectedItem.processes.length > 0}
        <div class="mt-4">
          <dt class="text-sm text-gray-500">Accessing Processes</dt>
          <dd class="mt-1.5 flex flex-wrap gap-1.5">
            {#each selectedItem.processes as proc}
              <span class="rounded-full bg-white px-2.5 py-0.5 text-xs font-medium text-gray-700">
                {proc}
              </span>
            {/each}
          </dd>
        </div>
      {/if}

      {#if Object.keys(selectedItem.operation_types || {}).length > 0}
        <div class="mt-4">
          <dt class="text-sm text-gray-500">Operation Breakdown</dt>
          <dd class="mt-1.5 grid grid-cols-2 gap-2 md:grid-cols-4">
            {#each Object.entries(selectedItem.operation_types) as [op, count]}
              <div class="flex items-center justify-between rounded bg-white px-2 py-1">
                <span class="truncate text-xs text-gray-600" title={formatOperation(op)}>
                  {formatOperation(op)}
                </span>
                <span class="ml-2 text-xs font-semibold text-gray-900">
                  {typeof count === 'number' ? count.toLocaleString() : count}
                </span>
              </div>
            {/each}
          </dd>
        </div>
      {/if}
    </div>
  {/if}
</div>
