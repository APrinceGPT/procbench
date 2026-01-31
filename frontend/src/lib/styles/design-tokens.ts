/**
 * Design Tokens for ProcBench UI
 * 
 * Centralized design system values for consistent styling across the application.
 * Use these tokens instead of hardcoded values.
 */

// =============================================================================
// COLOR PALETTE
// =============================================================================

export const colors = {
  // Base backgrounds
  background: {
    primary: '#0a0a0f',
    secondary: '#12121a',
    tertiary: '#1a1a24',
  },

  // Glass morphism surfaces
  glass: {
    background: 'rgba(255, 255, 255, 0.03)',
    backgroundHover: 'rgba(255, 255, 255, 0.06)',
    backgroundActive: 'rgba(255, 255, 255, 0.08)',
    border: 'rgba(255, 255, 255, 0.08)',
    borderHover: 'rgba(255, 255, 255, 0.15)',
  },

  // Text colors
  text: {
    primary: '#ffffff',
    secondary: 'rgba(255, 255, 255, 0.7)',
    tertiary: 'rgba(255, 255, 255, 0.5)',
    muted: 'rgba(255, 255, 255, 0.4)',
  },

  // Accent colors
  accent: {
    primary: '#3b82f6',       // Blue
    primaryHover: '#2563eb',
    secondary: '#8b5cf6',     // Purple
    secondaryHover: '#7c3aed',
    gradient: 'linear-gradient(135deg, #3b82f6, #8b5cf6)',
    gradientHover: 'linear-gradient(135deg, #2563eb, #7c3aed)',
  },

  // Risk level colors
  risk: {
    high: '#ef4444',
    highBg: 'rgba(239, 68, 68, 0.15)',
    highBorder: 'rgba(239, 68, 68, 0.3)',
    medium: '#f97316',
    mediumBg: 'rgba(249, 115, 22, 0.15)',
    mediumBorder: 'rgba(249, 115, 22, 0.3)',
    low: '#eab308',
    lowBg: 'rgba(234, 179, 8, 0.15)',
    lowBorder: 'rgba(234, 179, 8, 0.3)',
    none: '#6b7280',
    noneBg: 'rgba(107, 114, 128, 0.15)',
    noneBorder: 'rgba(107, 114, 128, 0.3)',
  },

  // Status colors
  status: {
    success: '#22c55e',
    successBg: 'rgba(34, 197, 94, 0.15)',
    warning: '#f59e0b',
    warningBg: 'rgba(245, 158, 11, 0.15)',
    error: '#ef4444',
    errorBg: 'rgba(239, 68, 68, 0.15)',
    info: '#3b82f6',
    infoBg: 'rgba(59, 130, 246, 0.15)',
  },

  // Legitimacy colors
  legitimacy: {
    legitimate: '#22c55e',
    legitimateBg: 'rgba(34, 197, 94, 0.15)',
    suspicious: '#f97316',
    suspiciousBg: 'rgba(249, 115, 22, 0.15)',
    malicious: '#ef4444',
    maliciousBg: 'rgba(239, 68, 68, 0.15)',
    unknown: '#6b7280',
    unknownBg: 'rgba(107, 114, 128, 0.15)',
  },
} as const;

// =============================================================================
// SPACING
// =============================================================================

export const spacing = {
  xs: '0.25rem',   // 4px
  sm: '0.5rem',    // 8px
  md: '1rem',      // 16px
  lg: '1.5rem',    // 24px
  xl: '2rem',      // 32px
  '2xl': '3rem',   // 48px
  '3xl': '4rem',   // 64px
} as const;

// =============================================================================
// TYPOGRAPHY
// =============================================================================

export const typography = {
  fontFamily: {
    sans: "system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', sans-serif",
    mono: "ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, monospace",
  },
  fontSize: {
    xs: '0.75rem',     // 12px
    sm: '0.875rem',    // 14px
    base: '1rem',      // 16px
    lg: '1.125rem',    // 18px
    xl: '1.25rem',     // 20px
    '2xl': '1.5rem',   // 24px
    '3xl': '1.875rem', // 30px
    '4xl': '2.25rem',  // 36px
  },
  fontWeight: {
    normal: '400',
    medium: '500',
    semibold: '600',
    bold: '700',
  },
  lineHeight: {
    tight: '1.25',
    normal: '1.5',
    relaxed: '1.75',
  },
} as const;

// =============================================================================
// BORDERS & RADIUS
// =============================================================================

export const borders = {
  radius: {
    sm: '0.375rem',  // 6px
    md: '0.5rem',    // 8px
    lg: '0.75rem',   // 12px
    xl: '1rem',      // 16px
    '2xl': '1.5rem', // 24px
    full: '9999px',
  },
  width: {
    thin: '1px',
    medium: '2px',
    thick: '3px',
  },
} as const;

// =============================================================================
// SHADOWS & EFFECTS
// =============================================================================

export const shadows = {
  sm: '0 1px 2px rgba(0, 0, 0, 0.3)',
  md: '0 4px 6px rgba(0, 0, 0, 0.3)',
  lg: '0 10px 15px rgba(0, 0, 0, 0.3)',
  xl: '0 20px 25px rgba(0, 0, 0, 0.4)',
  glow: {
    primary: '0 0 20px rgba(59, 130, 246, 0.3)',
    success: '0 0 20px rgba(34, 197, 94, 0.3)',
    danger: '0 0 20px rgba(239, 68, 68, 0.3)',
    warning: '0 0 20px rgba(249, 115, 22, 0.3)',
  },
  inner: 'inset 0 2px 4px rgba(0, 0, 0, 0.2)',
} as const;

export const blur = {
  sm: '4px',
  md: '8px',
  lg: '12px',
  xl: '16px',
  '2xl': '24px',
} as const;

// =============================================================================
// ANIMATIONS
// =============================================================================

export const animation = {
  duration: {
    instant: '0ms',
    fast: '150ms',
    normal: '250ms',
    slow: '350ms',
    slower: '500ms',
  },
  easing: {
    linear: 'linear',
    easeIn: 'cubic-bezier(0.4, 0, 1, 1)',
    easeOut: 'cubic-bezier(0, 0, 0.2, 1)',
    easeInOut: 'cubic-bezier(0.4, 0, 0.2, 1)',
    spring: 'cubic-bezier(0.34, 1.56, 0.64, 1)',
  },
} as const;

// =============================================================================
// BREAKPOINTS
// =============================================================================

export const breakpoints = {
  sm: '640px',
  md: '768px',
  lg: '1024px',
  xl: '1280px',
  '2xl': '1536px',
} as const;

// =============================================================================
// Z-INDEX LAYERS
// =============================================================================

export const zIndex = {
  base: 0,
  dropdown: 100,
  sticky: 200,
  modal: 300,
  popover: 400,
  tooltip: 500,
  toast: 600,
} as const;

// =============================================================================
// COMPONENT-SPECIFIC TOKENS
// =============================================================================

export const components = {
  sidebar: {
    widthExpanded: '16rem',   // 256px
    widthCollapsed: '4rem',   // 64px
  },
  card: {
    padding: spacing.lg,
    borderRadius: borders.radius.xl,
  },
  button: {
    heightSm: '2rem',         // 32px
    heightMd: '2.5rem',       // 40px
    heightLg: '3rem',         // 48px
  },
  input: {
    height: '2.5rem',         // 40px
    borderRadius: borders.radius.md,
  },
} as const;

// =============================================================================
// HELPER FUNCTIONS
// =============================================================================

/**
 * Get risk color based on score
 */
export function getRiskColors(score: number): { color: string; bg: string; border: string } {
  if (score >= 50) {
    return { color: colors.risk.high, bg: colors.risk.highBg, border: colors.risk.highBorder };
  }
  if (score >= 20) {
    return { color: colors.risk.medium, bg: colors.risk.mediumBg, border: colors.risk.mediumBorder };
  }
  if (score > 0) {
    return { color: colors.risk.low, bg: colors.risk.lowBg, border: colors.risk.lowBorder };
  }
  return { color: colors.risk.none, bg: colors.risk.noneBg, border: colors.risk.noneBorder };
}

/**
 * Get legitimacy color based on status
 */
export function getLegitimacyColors(legitimacy: string): { color: string; bg: string; border: string } {
  switch (legitimacy) {
    case 'legitimate':
      return { 
        color: colors.legitimacy.legitimate, 
        bg: colors.legitimacy.legitimateBg,
        border: 'rgba(34, 197, 94, 0.3)'
      };
    case 'suspicious':
      return { 
        color: colors.legitimacy.suspicious, 
        bg: colors.legitimacy.suspiciousBg,
        border: 'rgba(249, 115, 22, 0.3)'
      };
    case 'malicious':
      return { 
        color: colors.legitimacy.malicious, 
        bg: colors.legitimacy.maliciousBg,
        border: 'rgba(239, 68, 68, 0.3)'
      };
    default:
      return { 
        color: colors.legitimacy.unknown, 
        bg: colors.legitimacy.unknownBg,
        border: 'rgba(107, 114, 128, 0.3)'
      };
  }
}

// Type exports for TypeScript support
export type ColorToken = typeof colors;
export type SpacingToken = typeof spacing;
export type TypographyToken = typeof typography;
export type BorderToken = typeof borders;
export type ShadowToken = typeof shadows;
export type AnimationToken = typeof animation;
