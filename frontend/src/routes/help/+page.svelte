<script lang="ts">
  import { GlassCard } from '$lib/components/ui';
  import { colors, spacing, borders, animation } from '$lib/styles/design-tokens';

  // Accordion state
  let expandedSections: Set<string> = $state(new Set(['getting-started']));

  function toggleSection(id: string) {
    if (expandedSections.has(id)) {
      expandedSections.delete(id);
    } else {
      expandedSections.add(id);
    }
    expandedSections = new Set(expandedSections);
  }

  // Typed data for each section
  const gettingStartedSteps = [
    { step: 1, title: 'Export Process Monitor Log', description: 'In Process Monitor, go to File → Save and export your capture as PML, CSV, or XML format.' },
    { step: 2, title: 'Upload Your File', description: 'Navigate to the Upload page and drag & drop your file or click to browse. We support files up to 50MB.' },
    { step: 3, title: 'Wait for Analysis', description: 'Our AI-powered engine will analyze the events, detect suspicious patterns, and calculate risk scores.' },
    { step: 4, title: 'Review Dashboard', description: 'Check the Dashboard for an overview of findings, risk distribution, and top threats.' },
    { step: 5, title: 'Investigate Processes', description: 'Use the Process Tree to visualize parent-child relationships or Timeline for chronological analysis.' },
    { step: 6, title: 'Export Report', description: 'Generate a PDF report for documentation and sharing with your security team.' },
  ];

  const detectionMethods = [
    {
      title: 'LOLBAS Detection',
      description: 'Living Off The Land Binaries and Scripts - identifies legitimate Windows tools commonly abused by attackers (e.g., PowerShell, certutil, mshta).',
      tags: ['powershell.exe', 'certutil.exe', 'regsvr32.exe', 'mshta.exe'],
    },
    {
      title: 'Suspicious Path Analysis',
      description: 'Detects executables running from unusual locations like temp folders, user downloads, or AppData that may indicate malware.',
      tags: ['%TEMP%', '%APPDATA%', 'Downloads', 'Public'],
    },
    {
      title: 'Parent-Child Anomalies',
      description: 'Identifies unusual parent-child process relationships that may indicate process injection, lateral movement, or exploitation.',
      tags: ['cmd→powershell', 'office→cmd', 'browser→cmd'],
    },
    {
      title: 'Persistence Detection',
      description: 'Flags processes that modify registry run keys, scheduled tasks, or services for persistence.',
      tags: ['Run keys', 'Services', 'Scheduled Tasks'],
    },
    {
      title: 'AI Behavior Analysis',
      description: 'Advanced machine learning models analyze process behavior patterns to detect sophisticated threats.',
      tags: ['GPT-4o', 'Context-aware', 'Reasoning'],
    },
  ];

  const riskLevels = [
    { score: '70-100', level: 'High', color: colors.risk.high, bg: colors.risk.highBg, description: 'Requires immediate investigation. Likely malicious activity detected.' },
    { score: '30-69', level: 'Medium', color: colors.risk.medium, bg: colors.risk.mediumBg, description: 'Should be reviewed. Suspicious patterns or behaviors identified.' },
    { score: '1-29', level: 'Low', color: '#eab308', bg: 'rgba(234, 179, 8, 0.15)', description: 'May warrant attention. Minor anomalies detected.' },
    { score: '0', level: 'Safe', color: colors.status.success, bg: colors.status.successBg, description: 'Normal activity. No suspicious indicators found.' },
  ];

  const fileFormats = [
    { ext: '.pml', name: 'Process Monitor Log', description: 'Native binary format. Fastest parsing, full data fidelity. Recommended for best results.', recommended: true },
    { ext: '.csv', name: 'Comma-Separated Values', description: 'Text-based export. Widely compatible but may lose some event details.', recommended: false },
    { ext: '.xml', name: 'XML Format', description: 'Structured text export. Human-readable with full event data.', recommended: false },
  ];

  const keyboardShortcuts = [
    { keys: ['/', 'Ctrl', 'K'], action: 'Open global search' },
    { keys: ['↑', '↓'], action: 'Navigate search results' },
    { keys: ['Enter'], action: 'Select search result' },
    { keys: ['Esc'], action: 'Close search / dialogs' },
    { keys: ['D'], action: 'Go to Dashboard (when analysis active)' },
    { keys: ['T'], action: 'Go to Process Tree' },
    { keys: ['L'], action: 'Go to Timeline' },
  ];

  const faqItems = [
    { 
      q: 'How large can my log file be?', 
      a: 'We support files up to 50MB. For larger captures, consider filtering events in Process Monitor before exporting.' 
    },
    { 
      q: 'Is my data stored on your servers?', 
      a: 'Analysis is processed in-memory and results are stored temporarily. Data is automatically deleted after your session ends.' 
    },
    { 
      q: 'How accurate is the AI detection?', 
      a: 'Our AI models achieve high detection rates, but always verify findings manually. False positives can occur with legitimate administrative tools.' 
    },
    { 
      q: 'Can I analyze macOS or Linux logs?', 
      a: 'Currently, we only support Windows Process Monitor logs. Linux/macOS support is planned for future releases.' 
    },
    { 
      q: 'What if the analysis seems stuck?', 
      a: 'Large files may take several minutes. If analysis fails, try re-uploading or contact support.' 
    },
  ];

  // Section metadata for navigation
  const sections = [
    { id: 'getting-started', title: 'Getting Started', icon: '🚀' },
    { id: 'detection-methods', title: 'Detection Methods', icon: '🔍' },
    { id: 'risk-levels', title: 'Understanding Risk Levels', icon: '⚠️' },
    { id: 'file-formats', title: 'Supported File Formats', icon: '📄' },
    { id: 'keyboard-shortcuts', title: 'Keyboard Shortcuts', icon: '⌨️' },
    { id: 'faq', title: 'Frequently Asked Questions', icon: '❓' },
  ];
</script>

<div style="padding: {spacing.lg}; max-width: 1000px; margin: 0 auto;">
  <!-- Header -->
  <div style="margin-bottom: {spacing.xl}; animation: fadeInUp {animation.duration.normal} {animation.easing.easeOut};">
    <h1 style="
      font-size: 1.75rem;
      font-weight: 700;
      color: {colors.text.primary};
      margin: 0;
      background: {colors.accent.gradient};
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      background-clip: text;
    ">
      Help & Documentation
    </h1>
    <p style="color: {colors.text.tertiary}; margin: {spacing.sm} 0 0 0;">
      Learn how to use ProcBench to analyze Process Monitor logs and detect threats.
    </p>
  </div>

  <!-- Quick Links -->
  <div style="display: flex; flex-wrap: wrap; gap: {spacing.sm}; margin-bottom: {spacing.xl};">
    {#each sections as section}
      <button
        type="button"
        onclick={() => {
          expandedSections.add(section.id);
          expandedSections = new Set(expandedSections);
          document.getElementById(section.id)?.scrollIntoView({ behavior: 'smooth' });
        }}
        style="
          display: flex;
          align-items: center;
          gap: {spacing.xs};
          padding: {spacing.sm} {spacing.md};
          background: {colors.glass.background};
          border: 1px solid {colors.glass.border};
          border-radius: {borders.radius.full};
          color: {colors.text.secondary};
          font-size: 0.875rem;
          cursor: pointer;
        "
      >
        <span>{section.icon}</span>
        <span>{section.title}</span>
      </button>
    {/each}
  </div>

  <!-- Help Sections -->
  <div style="display: flex; flex-direction: column; gap: {spacing.md};">
    <!-- Getting Started -->
    <div id="getting-started">
      <GlassCard>
        <button type="button" onclick={() => toggleSection('getting-started')} style="width: 100%; display: flex; align-items: center; justify-content: space-between; background: none; border: none; cursor: pointer; padding: 0;">
          <h2 style="font-size: 1.125rem; font-weight: 600; color: {colors.text.primary}; margin: 0; display: flex; align-items: center; gap: {spacing.sm};">
            <span>🚀</span> Getting Started
          </h2>
          <svg style="width: 20px; height: 20px; color: {colors.text.muted}; transform: rotate({expandedSections.has('getting-started') ? '180deg' : '0deg'});" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
          </svg>
        </button>
        {#if expandedSections.has('getting-started')}
          <div style="margin-top: {spacing.lg}; display: flex; flex-direction: column; gap: {spacing.md};">
            {#each gettingStartedSteps as item}
              <div style="display: flex; gap: {spacing.md};">
                <div style="flex-shrink: 0; width: 32px; height: 32px; display: flex; align-items: center; justify-content: center; background: {colors.status.infoBg}; color: {colors.accent.primary}; border-radius: 50%; font-weight: 700; font-size: 0.875rem;">
                  {item.step}
                </div>
                <div>
                  <h3 style="margin: 0 0 {spacing.xs} 0; color: {colors.text.primary}; font-weight: 600;">{item.title}</h3>
                  <p style="margin: 0; color: {colors.text.secondary}; font-size: 0.875rem;">{item.description}</p>
                </div>
              </div>
            {/each}
          </div>
        {/if}
      </GlassCard>
    </div>

    <!-- Detection Methods -->
    <div id="detection-methods">
      <GlassCard>
        <button type="button" onclick={() => toggleSection('detection-methods')} style="width: 100%; display: flex; align-items: center; justify-content: space-between; background: none; border: none; cursor: pointer; padding: 0;">
          <h2 style="font-size: 1.125rem; font-weight: 600; color: {colors.text.primary}; margin: 0; display: flex; align-items: center; gap: {spacing.sm};">
            <span>🔍</span> Detection Methods
          </h2>
          <svg style="width: 20px; height: 20px; color: {colors.text.muted}; transform: rotate({expandedSections.has('detection-methods') ? '180deg' : '0deg'});" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
          </svg>
        </button>
        {#if expandedSections.has('detection-methods')}
          <div style="margin-top: {spacing.lg}; display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: {spacing.md};">
            {#each detectionMethods as item}
              <div style="padding: {spacing.md}; background: {colors.glass.background}; border: 1px solid {colors.glass.border}; border-radius: {borders.radius.lg};">
                <h3 style="margin: 0 0 {spacing.sm} 0; color: {colors.text.primary}; font-weight: 600;">{item.title}</h3>
                <p style="margin: 0 0 {spacing.sm} 0; color: {colors.text.secondary}; font-size: 0.875rem;">{item.description}</p>
                <div style="display: flex; flex-wrap: wrap; gap: 4px;">
                  {#each item.tags as tag}
                    <span style="font-size: 0.7rem; padding: 2px 6px; background: {colors.glass.backgroundHover}; color: {colors.text.tertiary}; border-radius: {borders.radius.sm}; font-family: monospace;">{tag}</span>
                  {/each}
                </div>
              </div>
            {/each}
          </div>
        {/if}
      </GlassCard>
    </div>

    <!-- Risk Levels -->
    <div id="risk-levels">
      <GlassCard>
        <button type="button" onclick={() => toggleSection('risk-levels')} style="width: 100%; display: flex; align-items: center; justify-content: space-between; background: none; border: none; cursor: pointer; padding: 0;">
          <h2 style="font-size: 1.125rem; font-weight: 600; color: {colors.text.primary}; margin: 0; display: flex; align-items: center; gap: {spacing.sm};">
            <span>⚠️</span> Understanding Risk Levels
          </h2>
          <svg style="width: 20px; height: 20px; color: {colors.text.muted}; transform: rotate({expandedSections.has('risk-levels') ? '180deg' : '0deg'});" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
          </svg>
        </button>
        {#if expandedSections.has('risk-levels')}
          <div style="margin-top: {spacing.lg}; display: flex; flex-direction: column; gap: {spacing.sm};">
            {#each riskLevels as item}
              <div style="display: flex; align-items: center; gap: {spacing.md}; padding: {spacing.sm} {spacing.md}; background: {item.bg}; border-radius: {borders.radius.lg}; border: 1px solid {item.color}33;">
                <div style="flex-shrink: 0; width: 50px; height: 32px; display: flex; align-items: center; justify-content: center; background: {item.color}22; color: {item.color}; border-radius: {borders.radius.md}; font-weight: 700; font-size: 0.75rem;">
                  {item.score}
                </div>
                <div style="flex: 1;">
                  <span style="font-weight: 600; color: {item.color};">{item.level} Risk</span>
                  <span style="margin-left: {spacing.sm}; color: {colors.text.secondary}; font-size: 0.875rem;">— {item.description}</span>
                </div>
              </div>
            {/each}
          </div>
        {/if}
      </GlassCard>
    </div>

    <!-- File Formats -->
    <div id="file-formats">
      <GlassCard>
        <button type="button" onclick={() => toggleSection('file-formats')} style="width: 100%; display: flex; align-items: center; justify-content: space-between; background: none; border: none; cursor: pointer; padding: 0;">
          <h2 style="font-size: 1.125rem; font-weight: 600; color: {colors.text.primary}; margin: 0; display: flex; align-items: center; gap: {spacing.sm};">
            <span>📄</span> Supported File Formats
          </h2>
          <svg style="width: 20px; height: 20px; color: {colors.text.muted}; transform: rotate({expandedSections.has('file-formats') ? '180deg' : '0deg'});" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
          </svg>
        </button>
        {#if expandedSections.has('file-formats')}
          <div style="margin-top: {spacing.lg}; display: flex; flex-direction: column; gap: {spacing.md};">
            {#each fileFormats as item}
              <div style="display: flex; align-items: flex-start; gap: {spacing.md}; padding: {spacing.md}; background: {colors.glass.background}; border: 1px solid {item.recommended ? colors.accent.primary : colors.glass.border}; border-radius: {borders.radius.lg};">
                <code style="flex-shrink: 0; padding: {spacing.xs} {spacing.sm}; background: {item.recommended ? colors.status.infoBg : colors.glass.backgroundHover}; color: {item.recommended ? colors.accent.primary : colors.text.primary}; border-radius: {borders.radius.md}; font-weight: 600;">
                  {item.ext}
                </code>
                <div>
                  <h3 style="margin: 0 0 {spacing.xs} 0; color: {colors.text.primary}; font-weight: 600; display: flex; align-items: center; gap: {spacing.sm};">
                    {item.name}
                    {#if item.recommended}
                      <span style="font-size: 0.65rem; padding: 2px 6px; background: {colors.status.successBg}; color: {colors.status.success}; border-radius: {borders.radius.full}; font-weight: 500;">RECOMMENDED</span>
                    {/if}
                  </h3>
                  <p style="margin: 0; color: {colors.text.secondary}; font-size: 0.875rem;">{item.description}</p>
                </div>
              </div>
            {/each}
          </div>
        {/if}
      </GlassCard>
    </div>

    <!-- Keyboard Shortcuts -->
    <div id="keyboard-shortcuts">
      <GlassCard>
        <button type="button" onclick={() => toggleSection('keyboard-shortcuts')} style="width: 100%; display: flex; align-items: center; justify-content: space-between; background: none; border: none; cursor: pointer; padding: 0;">
          <h2 style="font-size: 1.125rem; font-weight: 600; color: {colors.text.primary}; margin: 0; display: flex; align-items: center; gap: {spacing.sm};">
            <span>⌨️</span> Keyboard Shortcuts
          </h2>
          <svg style="width: 20px; height: 20px; color: {colors.text.muted}; transform: rotate({expandedSections.has('keyboard-shortcuts') ? '180deg' : '0deg'});" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
          </svg>
        </button>
        {#if expandedSections.has('keyboard-shortcuts')}
          <div style="margin-top: {spacing.lg}; display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: {spacing.sm};">
            {#each keyboardShortcuts as item}
              <div style="display: flex; align-items: center; justify-content: space-between; padding: {spacing.sm} {spacing.md}; background: {colors.glass.background}; border-radius: {borders.radius.lg};">
                <span style="color: {colors.text.secondary}; font-size: 0.875rem;">{item.action}</span>
                <div style="display: flex; gap: 4px;">
                  {#each item.keys as key}
                    <kbd style="padding: 4px 8px; background: {colors.glass.backgroundHover}; border: 1px solid {colors.glass.border}; border-radius: {borders.radius.sm}; color: {colors.text.primary}; font-size: 0.75rem; font-family: inherit;">{key}</kbd>
                  {/each}
                </div>
              </div>
            {/each}
          </div>
        {/if}
      </GlassCard>
    </div>

    <!-- FAQ -->
    <div id="faq">
      <GlassCard>
        <button type="button" onclick={() => toggleSection('faq')} style="width: 100%; display: flex; align-items: center; justify-content: space-between; background: none; border: none; cursor: pointer; padding: 0;">
          <h2 style="font-size: 1.125rem; font-weight: 600; color: {colors.text.primary}; margin: 0; display: flex; align-items: center; gap: {spacing.sm};">
            <span>❓</span> Frequently Asked Questions
          </h2>
          <svg style="width: 20px; height: 20px; color: {colors.text.muted}; transform: rotate({expandedSections.has('faq') ? '180deg' : '0deg'});" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
          </svg>
        </button>
        {#if expandedSections.has('faq')}
          <div style="margin-top: {spacing.lg}; display: flex; flex-direction: column; gap: {spacing.md};">
            {#each faqItems as item}
              <div style="padding: {spacing.md}; background: {colors.glass.background}; border-radius: {borders.radius.lg};">
                <h3 style="margin: 0 0 {spacing.sm} 0; color: {colors.text.primary}; font-weight: 600; display: flex; gap: {spacing.sm};">
                  <span style="color: {colors.accent.primary};">Q:</span>
                  {item.q}
                </h3>
                <p style="margin: 0; color: {colors.text.secondary}; font-size: 0.875rem; padding-left: 1.5rem;">
                  {item.a}
                </p>
              </div>
            {/each}
          </div>
        {/if}
      </GlassCard>
    </div>
  </div>

  <!-- Contact Section -->
  <div style="margin-top: {spacing.xl}; padding: {spacing.lg}; background: {colors.accent.gradient}; border-radius: {borders.radius.xl}; text-align: center;">
    <h2 style="margin: 0 0 {spacing.sm} 0; color: white; font-size: 1.25rem; font-weight: 600;">
      Still need help?
    </h2>
    <p style="margin: 0 0 {spacing.md} 0; color: rgba(255, 255, 255, 0.8); font-size: 0.875rem;">
      Check out the documentation or reach out to the community.
    </p>
    <a
      href="https://github.com"
      target="_blank"
      rel="noopener noreferrer"
      style="display: inline-flex; align-items: center; gap: {spacing.sm}; padding: {spacing.sm} {spacing.lg}; background: rgba(255, 255, 255, 0.2); color: white; text-decoration: none; border-radius: {borders.radius.lg}; font-weight: 500;"
    >
      <svg style="width: 18px; height: 18px;" fill="currentColor" viewBox="0 0 24 24">
        <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
      </svg>
      View on GitHub
    </a>
  </div>
</div>

<style>
  @keyframes fadeInUp {
    from {
      opacity: 0;
      transform: translateY(10px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }
</style>
