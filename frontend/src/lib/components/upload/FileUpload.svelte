<script lang="ts">
  import { onMount } from 'svelte';
  import { api } from '$lib/api/client';
  import { analysisStore } from '$lib/stores/analysis';
  import { goto } from '$app/navigation';
  import { colors, spacing, borders, animation, shadows } from '$lib/styles/design-tokens';

  let dragActive = $state(false);
  let uploading = $state(false);
  let error: string | null = $state(null);
  let supportedFormats: string[] = $state(['.pml', '.csv', '.xml']);

  // Load supported formats on mount
  onMount(async () => {
    try {
      const response = await api.getSupportedFormats();
      supportedFormats = response.formats;
    } catch (e) {
      console.error('Failed to load supported formats:', e);
    }
  });

  // Handle file drop
  function handleDrop(e: DragEvent) {
    e.preventDefault();
    dragActive = false;

    const files = e.dataTransfer?.files;
    if (files && files.length > 0) {
      processFile(files[0]);
    }
  }

  // Handle file input change
  function handleFileInput(e: Event) {
    const input = e.target as HTMLInputElement;
    if (input.files && input.files.length > 0) {
      processFile(input.files[0]);
    }
  }

  // Process and upload file
  async function processFile(file: File) {
    // Validate file extension
    const ext = '.' + file.name.split('.').pop()?.toLowerCase();
    if (!supportedFormats.includes(ext)) {
      error = `Unsupported file format. Please use: ${supportedFormats.join(', ')}`;
      return;
    }

    uploading = true;
    error = null;
    analysisStore.setLoading(true);

    try {
      const response = await api.analyzeFile(file);
      analysisStore.setAnalysisId(response.analysis_id);

      // Fetch full results
      const result = await api.getAnalysis(response.analysis_id);
      analysisStore.setResult(result);

      // Navigate to dashboard
      goto('/dashboard');
    } catch (e) {
      const message = e instanceof Error ? e.message : 'Upload failed';
      error = message;
      analysisStore.setError(message);
    } finally {
      uploading = false;
      analysisStore.setLoading(false);
    }
  }

  function handleDragOver(e: DragEvent) {
    e.preventDefault();
    dragActive = true;
  }

  function handleDragLeave() {
    dragActive = false;
  }

  function triggerFileInput() {
    document.getElementById('file-input')?.click();
  }

  function handleKeydown(e: KeyboardEvent) {
    if (e.key === 'Enter' || e.key === ' ') {
      e.preventDefault();
      triggerFileInput();
    }
  }
</script>

<div style="width: 100%; max-width: 48rem; margin: 0 auto;">
  <div
    role="button"
    tabindex="0"
    style="
      position: relative;
      border: 2px dashed {dragActive ? colors.accent.primary : colors.glass.border};
      border-radius: {borders.radius.xl};
      padding: {spacing['2xl']};
      text-align: center;
      transition: all {animation.duration.normal} {animation.easing.easeInOut};
      background: {dragActive ? 'rgba(59, 130, 246, 0.1)' : colors.glass.background};
      backdrop-filter: blur(12px);
      -webkit-backdrop-filter: blur(12px);
      cursor: {uploading ? 'not-allowed' : 'pointer'};
      opacity: {uploading ? '0.7' : '1'};
      pointer-events: {uploading ? 'none' : 'auto'};
      box-shadow: {dragActive ? shadows.glow.primary : 'none'};
    "
    ondrop={handleDrop}
    ondragover={handleDragOver}
    ondragleave={handleDragLeave}
    onclick={triggerFileInput}
    onkeydown={handleKeydown}
    onmouseenter={(e) => {
      if (!uploading && !dragActive) {
        const el = e.currentTarget as HTMLElement;
        el.style.borderColor = colors.text.muted;
        el.style.background = colors.glass.backgroundHover;
      }
    }}
    onmouseleave={(e) => {
      if (!uploading && !dragActive) {
        const el = e.currentTarget as HTMLElement;
        el.style.borderColor = colors.glass.border;
        el.style.background = colors.glass.background;
      }
    }}
  >
    <input
      type="file"
      id="file-input"
      style="display: none;"
      accept={supportedFormats.join(',')}
      onchange={handleFileInput}
      disabled={uploading}
    />

    {#if uploading}
      <div style="display: flex; flex-direction: column; align-items: center;">
        <div style="
          width: 64px; 
          height: 64px; 
          margin-bottom: {spacing.lg};
          border: 3px solid {colors.glass.border};
          border-top-color: {colors.accent.primary};
          border-radius: 50%;
          animation: spin 1s linear infinite;
        "></div>
        <p style="font-size: 1.125rem; font-weight: 600; color: {colors.text.primary}; margin: 0;">
          Analyzing file...
        </p>
        <p style="font-size: 0.875rem; color: {colors.text.tertiary}; margin-top: {spacing.xs};">
          This may take a few moments for large files
        </p>
      </div>
    {:else}
      <div style="display: flex; flex-direction: column; align-items: center;">
        <div style="
          width: 72px;
          height: 72px;
          margin-bottom: {spacing.lg};
          background: {colors.glass.backgroundHover};
          border-radius: 50%;
          display: flex;
          align-items: center;
          justify-content: center;
          border: 1px solid {colors.glass.border};
        ">
          <svg
            style="width: 36px; height: 36px; color: {colors.accent.primary};"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="1.5"
              d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"
            />
          </svg>
        </div>
        <p style="font-size: 1.25rem; font-weight: 600; color: {colors.text.primary}; margin: 0;">
          Drop your Process Monitor log here
        </p>
        <p style="font-size: 0.9rem; color: {colors.text.tertiary}; margin-top: {spacing.xs};">
          or <span style="color: {colors.accent.primary}; text-decoration: underline;">click to browse</span>
        </p>
        <div style="
          margin-top: {spacing.lg}; 
          display: flex; 
          gap: {spacing.sm}; 
          justify-content: center;
        ">
          {#each supportedFormats as format}
            <span style="
              padding: {spacing.xs} {spacing.sm};
              background: {colors.glass.backgroundHover};
              border: 1px solid {colors.glass.border};
              border-radius: {borders.radius.md};
              font-size: 0.75rem;
              font-weight: 500;
              color: {colors.text.secondary};
              font-family: monospace;
            ">
              {format}
            </span>
          {/each}
        </div>
      </div>
    {/if}
  </div>

  {#if error}
    <div style="
      margin-top: {spacing.md}; 
      padding: {spacing.md}; 
      background: {colors.risk.highBg}; 
      border: 1px solid {colors.risk.highBorder}; 
      border-radius: {borders.radius.lg};
      animation: fadeIn {animation.duration.fast} {animation.easing.easeOut};
    ">
      <div style="display: flex; align-items: center;">
        <svg
          style="width: 20px; height: 20px; color: {colors.risk.high}; margin-right: {spacing.sm}; flex-shrink: 0;"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
          />
        </svg>
        <p style="font-size: 0.875rem; color: {colors.risk.high}; margin: 0;">{error}</p>
      </div>
    </div>
  {/if}
</div>

<style>
  @keyframes spin {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
  }
  
  @keyframes fadeIn {
    from { opacity: 0; transform: translateY(-4px); }
    to { opacity: 1; transform: translateY(0); }
  }
</style>
