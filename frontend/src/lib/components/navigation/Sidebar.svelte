<script lang="ts">
  import { page } from '$app/stores';
  import { uiStore, isSidebarOpen } from '$lib/stores/ui';
  import { hasAnalysis } from '$lib/stores/analysis';
  import { colors, borders, spacing, animation, shadows } from '$lib/styles/design-tokens';

  interface NavItem {
    href: string;
    label: string;
    icon: string;
    requiresAnalysis: boolean;
  }

  const navItems: NavItem[] = [
    { href: '/', label: 'Upload', icon: 'upload', requiresAnalysis: false },
    { href: '/dashboard', label: 'Dashboard', icon: 'dashboard', requiresAnalysis: true },
    { href: '/investigate/tree', label: 'Process Tree', icon: 'tree', requiresAnalysis: true },
    { href: '/investigate/timeline', label: 'Timeline', icon: 'timeline', requiresAnalysis: true },
    { href: '/help', label: 'Help', icon: 'help', requiresAnalysis: false },
  ];

  const currentPath = $derived($page.url.pathname);
  const sidebarWidth = $derived($isSidebarOpen ? '256px' : '64px');

  // Glass morphism sidebar styles
  const sidebarStyle = $derived(`
    position: fixed;
    left: 0;
    top: 0;
    height: 100vh;
    width: ${sidebarWidth};
    background: linear-gradient(180deg, rgba(15, 15, 25, 0.95) 0%, rgba(10, 10, 15, 0.98) 100%);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border-right: 1px solid ${colors.glass.border};
    z-index: 40;
    transition: width ${animation.duration.normal} ${animation.easing.easeInOut};
  `);

  function getNavItemStyle(isActive: boolean, isDisabled: boolean): string {
    if (isActive) {
      return `
        background: ${colors.accent.gradient};
        color: white;
        box-shadow: ${shadows.glow.primary};
      `;
    }
    if (isDisabled) {
      return `
        color: ${colors.text.muted};
        cursor: not-allowed;
        opacity: 0.5;
      `;
    }
    return `
      color: ${colors.text.secondary};
    `;
  }

  function getNavItemHoverStyle(isActive: boolean, isDisabled: boolean): string {
    if (isActive || isDisabled) return '';
    return `
      background: ${colors.glass.backgroundHover};
      color: ${colors.text.primary};
      transform: translateX(4px);
    `;
  }
</script>

<aside style={sidebarStyle}>
  <div style="height: 100%; display: flex; flex-direction: column;">
    <!-- Logo area with glow effect -->
    <div style="
      height: 64px;
      display: flex;
      align-items: center;
      justify-content: center;
      border-bottom: 1px solid {colors.glass.border};
      background: linear-gradient(180deg, rgba(59, 130, 246, 0.05) 0%, transparent 100%);
    ">
      {#if $isSidebarOpen}
        <span style="
          font-size: 1.25rem;
          font-weight: bold;
          background: {colors.accent.gradient};
          -webkit-background-clip: text;
          -webkit-text-fill-color: transparent;
          background-clip: text;
        ">ProcBench</span>
      {:else}
        <span style="
          font-size: 1.5rem;
          font-weight: bold;
          background: {colors.accent.gradient};
          -webkit-background-clip: text;
          -webkit-text-fill-color: transparent;
          background-clip: text;
        ">P</span>
      {/if}
    </div>

    <!-- Navigation -->
    <nav style="flex: 1; padding: {spacing.md} 0; overflow-y: auto;">
      <ul style="display: flex; flex-direction: column; gap: {spacing.xs}; padding: 0 {spacing.sm}; list-style: none;">
        {#each navItems as item}
          {@const isActive = currentPath === item.href}
          {@const isDisabled = item.requiresAnalysis && !$hasAnalysis}

          <li>
            <a
              href={isDisabled ? undefined : item.href}
              style="
                display: flex;
                align-items: center;
                gap: {spacing.md};
                padding: {spacing.sm} {spacing.md};
                border-radius: {borders.radius.lg};
                transition: all {animation.duration.normal} {animation.easing.easeInOut};
                text-decoration: none;
                {getNavItemStyle(isActive, isDisabled)}
              "
              title={isDisabled ? 'Upload a file first' : item.label}
              onmouseenter={(e) => {
                if (!isActive && !isDisabled) {
                  e.currentTarget.style.cssText += getNavItemHoverStyle(isActive, isDisabled);
                }
              }}
              onmouseleave={(e) => {
                if (!isActive && !isDisabled) {
                  e.currentTarget.style.cssText = `
                    display: flex;
                    align-items: center;
                    gap: ${spacing.md};
                    padding: ${spacing.sm} ${spacing.md};
                    border-radius: ${borders.radius.lg};
                    transition: all ${animation.duration.normal} ${animation.easing.easeInOut};
                    text-decoration: none;
                    ${getNavItemStyle(isActive, isDisabled)}
                  `;
                }
              }}
            >
              <span style="flex-shrink: 0; display: flex; align-items: center;">
                {#if item.icon === 'upload'}
                  <svg style="width: 20px; height: 20px;" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                  </svg>
                {:else if item.icon === 'dashboard'}
                  <svg style="width: 20px; height: 20px;" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z" />
                  </svg>
                {:else if item.icon === 'tree'}
                  <svg style="width: 20px; height: 20px;" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
                  </svg>
                {:else if item.icon === 'timeline'}
                  <svg style="width: 20px; height: 20px;" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                {:else if item.icon === 'help'}
                  <svg style="width: 20px; height: 20px;" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                {/if}
              </span>

              {#if $isSidebarOpen}
                <span style="
                  white-space: nowrap;
                  overflow: hidden;
                  text-overflow: ellipsis;
                  font-weight: 500;
                ">{item.label}</span>
              {/if}
            </a>
          </li>
        {/each}
      </ul>
    </nav>

    <!-- Collapse button -->
    <div style="padding: {spacing.sm}; border-top: 1px solid {colors.glass.border};">
      <button
        style="
          width: 100%;
          display: flex;
          align-items: center;
          justify-content: center;
          gap: {spacing.sm};
          padding: {spacing.sm} {spacing.md};
          border-radius: {borders.radius.lg};
          color: {colors.text.tertiary};
          background: transparent;
          border: none;
          cursor: pointer;
          transition: all {animation.duration.normal} {animation.easing.easeInOut};
        "
        onmouseenter={(e) => {
          e.currentTarget.style.backgroundColor = colors.glass.backgroundHover;
          e.currentTarget.style.color = colors.text.primary;
        }}
        onmouseleave={(e) => {
          e.currentTarget.style.backgroundColor = 'transparent';
          e.currentTarget.style.color = colors.text.tertiary;
        }}
        onclick={() => uiStore.toggleSidebar()}
      >
        <svg
          style="
            width: 20px;
            height: 20px;
            transition: transform {animation.duration.normal} {animation.easing.easeInOut};
            {$isSidebarOpen ? '' : 'transform: rotate(180deg);'}
          "
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 19l-7-7 7-7m8 14l-7-7 7-7" />
        </svg>
        {#if $isSidebarOpen}
          <span style="font-weight: 500;">Collapse</span>
        {/if}
      </button>
    </div>
  </div>
</aside>
