<script lang="ts">
  import { analysisResult, topThreats } from '$lib/stores/analysis';
  import type { ProcessSummary } from '$lib/api/types';
  import { colors, spacing, borders, animation, shadows } from '$lib/styles/design-tokens';

  // ==========================================================================
  // PROPS
  // ==========================================================================

  interface Props {
    onSelect?: (process: ProcessSummary) => void;
    placeholder?: string;
  }

  let { onSelect, placeholder = 'Search processes...' }: Props = $props();

  // ==========================================================================
  // STATE
  // ==========================================================================

  let searchQuery = $state('');
  let isOpen = $state(false);
  let selectedIndex = $state(-1);
  let inputRef: HTMLInputElement | null = $state(null);

  // ==========================================================================
  // COMPUTED
  // ==========================================================================

  // Search results filtered from top threats
  let searchResults = $derived(() => {
    if (!searchQuery.trim() || !$topThreats.length) return [];

    const query = searchQuery.toLowerCase().trim();

    return $topThreats
      .filter((process) => {
        const name = process.process_name?.toLowerCase() || '';
        const path = process.image_path?.toLowerCase() || '';
        const cmdLine = process.command_line?.toLowerCase() || '';
        const pid = process.pid.toString();
        const tags = process.behavior_tags?.join(' ').toLowerCase() || '';
        const rules = process.matched_rules?.join(' ').toLowerCase() || '';
        const reasoning = process.ai_reasoning?.toLowerCase() || '';

        return (
          name.includes(query) ||
          path.includes(query) ||
          cmdLine.includes(query) ||
          pid.includes(query) ||
          tags.includes(query) ||
          rules.includes(query) ||
          reasoning.includes(query)
        );
      })
      .slice(0, 8); // Limit to 8 results
  });

  // Whether we have results to show
  let hasResults = $derived(searchResults().length > 0);

  // ==========================================================================
  // HANDLERS
  // ==========================================================================

  function handleInput(e: Event) {
    const target = e.target as HTMLInputElement;
    searchQuery = target.value;
    isOpen = true;
    selectedIndex = -1;
  }

  function handleFocus() {
    isOpen = true;
  }

  function handleBlur() {
    // Delay close to allow click on results
    setTimeout(() => {
      isOpen = false;
    }, 200);
  }

  function handleKeydown(e: KeyboardEvent) {
    const results = searchResults();

    switch (e.key) {
      case 'ArrowDown':
        e.preventDefault();
        if (selectedIndex < results.length - 1) {
          selectedIndex++;
        }
        break;
      case 'ArrowUp':
        e.preventDefault();
        if (selectedIndex > 0) {
          selectedIndex--;
        }
        break;
      case 'Enter':
        e.preventDefault();
        if (selectedIndex >= 0 && selectedIndex < results.length) {
          selectProcess(results[selectedIndex]);
        }
        break;
      case 'Escape':
        e.preventDefault();
        isOpen = false;
        inputRef?.blur();
        break;
    }
  }

  function selectProcess(process: ProcessSummary) {
    searchQuery = '';
    isOpen = false;
    selectedIndex = -1;
    onSelect?.(process);
  }

  function getRiskColor(score: number): string {
    if (score >= 70) return colors.risk.high;
    if (score >= 30) return colors.risk.medium;
    if (score > 0) return '#eab308'; // yellow
    return colors.status.success;
  }

  function getLegitimacyBadgeStyle(legitimacy: string): string {
    const baseStyle = `
      font-size: 0.65rem;
      padding: 2px 6px;
      border-radius: ${borders.radius.full};
      font-weight: 500;
      text-transform: uppercase;
    `;

    switch (legitimacy) {
      case 'malicious':
        return `${baseStyle} background: ${colors.risk.highBg}; color: ${colors.risk.high};`;
      case 'suspicious':
        return `${baseStyle} background: ${colors.risk.mediumBg}; color: ${colors.risk.medium};`;
      case 'legitimate':
        return `${baseStyle} background: ${colors.status.successBg}; color: ${colors.status.success};`;
      default:
        return `${baseStyle} background: ${colors.glass.background}; color: ${colors.text.tertiary};`;
    }
  }

  function highlightMatch(text: string, query: string): string {
    if (!query.trim()) return text;

    const regex = new RegExp(`(${query.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')})`, 'gi');
    return text.replace(regex, '<mark style="background: rgba(99, 102, 241, 0.3); padding: 0 2px; border-radius: 2px;">$1</mark>');
  }
</script>

<div style="position: relative;">
  <!-- Search Input -->
  <div
    style="
      display: flex;
      align-items: center;
      gap: {spacing.sm};
      padding: {spacing.sm} {spacing.md};
      background: {colors.glass.background};
      backdrop-filter: blur(12px);
      border: 1px solid {isOpen && hasResults ? colors.accent.primary : colors.glass.border};
      border-radius: {borders.radius.xl};
      transition: all {animation.duration.normal} {animation.easing.easeInOut};
    "
  >
    <svg
      style="width: 18px; height: 18px; color: {colors.text.muted}; flex-shrink: 0;"
      fill="none"
      viewBox="0 0 24 24"
      stroke="currentColor"
    >
      <path
        stroke-linecap="round"
        stroke-linejoin="round"
        stroke-width="2"
        d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
      />
    </svg>

    <input
      bind:this={inputRef}
      type="text"
      value={searchQuery}
      {placeholder}
      oninput={handleInput}
      onfocus={handleFocus}
      onblur={handleBlur}
      onkeydown={handleKeydown}
      style="
        flex: 1;
        border: none;
        background: transparent;
        outline: none;
        font-size: 0.875rem;
        color: {colors.text.primary};
      "
    />

    {#if searchQuery}
      <button
        type="button"
        onclick={() => {
          searchQuery = '';
          inputRef?.focus();
        }}
        aria-label="Clear search"
        style="
          display: flex;
          align-items: center;
          justify-content: center;
          width: 20px;
          height: 20px;
          border-radius: 50%;
          background: {colors.glass.background};
          border: none;
          cursor: pointer;
          color: {colors.text.muted};
          transition: all {animation.duration.fast};
        "
        onmouseenter={(e) => {
          const el = e.currentTarget as HTMLElement;
          el.style.background = colors.glass.backgroundHover;
          el.style.color = colors.text.secondary;
        }}
        onmouseleave={(e) => {
          const el = e.currentTarget as HTMLElement;
          el.style.background = colors.glass.background;
          el.style.color = colors.text.muted;
        }}
      >
        <svg style="width: 12px; height: 12px;" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
        </svg>
      </button>
    {/if}

    <!-- Keyboard shortcut hint -->
    <kbd
      style="
        display: none;
        font-size: 0.65rem;
        padding: 2px 6px;
        background: {colors.glass.background};
        border: 1px solid {colors.glass.border};
        border-radius: {borders.radius.sm};
        color: {colors.text.muted};
        font-family: inherit;
      "
    >
      /
    </kbd>
  </div>

  <!-- Results Dropdown -->
  {#if isOpen && searchQuery.trim()}
    <div
      style="
        position: absolute;
        top: 100%;
        left: 0;
        right: 0;
        margin-top: {spacing.sm};
        background: {colors.glass.background};
        backdrop-filter: blur(20px);
        border: 1px solid {colors.glass.border};
        border-radius: {borders.radius.xl};
        box-shadow: {shadows.lg};
        max-height: 400px;
        overflow-y: auto;
        z-index: 50;
        animation: fadeIn {animation.duration.fast} {animation.easing.easeOut};
      "
    >
      {#if hasResults}
        <div style="padding: {spacing.sm};">
          {#each searchResults() as process, index}
            <button
              type="button"
              onclick={() => selectProcess(process)}
              style="
                width: 100%;
                text-align: left;
                display: flex;
                align-items: flex-start;
                gap: {spacing.md};
                padding: {spacing.sm} {spacing.md};
                border: none;
                background: {index === selectedIndex ? colors.glass.backgroundHover : 'transparent'};
                border-radius: {borders.radius.lg};
                cursor: pointer;
                transition: background {animation.duration.fast};
              "
              onmouseenter={(e) => {
                selectedIndex = index;
                const el = e.currentTarget as HTMLElement;
                el.style.background = colors.glass.backgroundHover;
              }}
              onmouseleave={(e) => {
                const el = e.currentTarget as HTMLElement;
                el.style.background = index === selectedIndex ? colors.glass.backgroundHover : 'transparent';
              }}
            >
              <!-- Risk Score Indicator -->
              <div
                style="
                  flex-shrink: 0;
                  width: 36px;
                  height: 36px;
                  display: flex;
                  align-items: center;
                  justify-content: center;
                  border-radius: {borders.radius.lg};
                  background: {getRiskColor(process.risk_score)}22;
                  color: {getRiskColor(process.risk_score)};
                  font-size: 0.75rem;
                  font-weight: 700;
                "
              >
                {process.risk_score}
              </div>

              <!-- Process Details -->
              <div style="flex: 1; min-width: 0;">
                <div style="display: flex; align-items: center; gap: {spacing.sm}; margin-bottom: 2px;">
                  <span
                    style="
                      font-weight: 600;
                      color: {colors.text.primary};
                      font-size: 0.875rem;
                    "
                  >
                    {@html highlightMatch(process.process_name, searchQuery)}
                  </span>
                  <span style="color: {colors.text.muted}; font-size: 0.75rem;">
                    PID: {process.pid}
                  </span>
                  <span style={getLegitimacyBadgeStyle(process.legitimacy)}>
                    {process.legitimacy}
                  </span>
                </div>

                {#if process.image_path}
                  <p
                    style="
                      font-size: 0.75rem;
                      color: {colors.text.tertiary};
                      margin: 0;
                      white-space: nowrap;
                      overflow: hidden;
                      text-overflow: ellipsis;
                    "
                    title={process.image_path}
                  >
                    {@html highlightMatch(process.image_path, searchQuery)}
                  </p>
                {/if}

                {#if process.behavior_tags && process.behavior_tags.length > 0}
                  <div style="display: flex; flex-wrap: wrap; gap: 4px; margin-top: 4px;">
                    {#each process.behavior_tags.slice(0, 3) as tag}
                      <span
                        style="
                          font-size: 0.6rem;
                          padding: 1px 4px;
                          background: {colors.status.infoBg};
                          color: {colors.accent.primary};
                          border-radius: {borders.radius.sm};
                        "
                      >
                        {@html highlightMatch(tag, searchQuery)}
                      </span>
                    {/each}
                    {#if process.behavior_tags.length > 3}
                      <span
                        style="
                          font-size: 0.6rem;
                          color: {colors.text.muted};
                        "
                      >
                        +{process.behavior_tags.length - 3} more
                      </span>
                    {/if}
                  </div>
                {/if}
              </div>

              <!-- Arrow -->
              <svg
                style="width: 16px; height: 16px; color: {colors.text.muted}; flex-shrink: 0; margin-top: 2px;"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
              </svg>
            </button>
          {/each}
        </div>

        <!-- Results count footer -->
        <div
          style="
            padding: {spacing.sm} {spacing.md};
            border-top: 1px solid {colors.glass.border};
            font-size: 0.75rem;
            color: {colors.text.muted};
            display: flex;
            justify-content: space-between;
          "
        >
          <span>Found {searchResults().length} result(s)</span>
          <span>↑↓ Navigate · ↵ Select · Esc Close</span>
        </div>
      {:else}
        <div
          style="
            padding: {spacing.xl};
            text-align: center;
            color: {colors.text.tertiary};
          "
        >
          <svg
            style="width: 32px; height: 32px; margin: 0 auto {spacing.sm}; opacity: 0.5;"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
            />
          </svg>
          <p style="margin: 0; font-size: 0.875rem;">No processes found for "{searchQuery}"</p>
          <p style="margin: {spacing.xs} 0 0 0; font-size: 0.75rem; color: {colors.text.muted};">
            Try searching by process name, PID, path, or behavior tags
          </p>
        </div>
      {/if}
    </div>
  {/if}
</div>

<style>
  @keyframes fadeIn {
    from {
      opacity: 0;
      transform: translateY(-4px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }

  input::placeholder {
    color: var(--text-muted, #6b7280);
  }

  /* Custom scrollbar for results */
  div::-webkit-scrollbar {
    width: 6px;
  }

  div::-webkit-scrollbar-track {
    background: transparent;
  }

  div::-webkit-scrollbar-thumb {
    background: rgba(255, 255, 255, 0.1);
    border-radius: 3px;
  }

  div::-webkit-scrollbar-thumb:hover {
    background: rgba(255, 255, 255, 0.2);
  }
</style>
