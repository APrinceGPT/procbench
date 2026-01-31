// UI State Store

import { writable, derived } from 'svelte/store';

export type ViewMode = 'dashboard' | 'tree' | 'timeline' | 'heatmap';
export type Theme = 'light' | 'dark' | 'system';

interface UIState {
  viewMode: ViewMode;
  theme: Theme;
  sidebarOpen: boolean;
  guidedModeEnabled: boolean;
  showHelpTooltips: boolean;
  selectedProcessPid: number | null;
  modalOpen: string | null; // modal id
}

const initialState: UIState = {
  viewMode: 'dashboard',
  theme: 'system',
  sidebarOpen: true,
  guidedModeEnabled: true,
  showHelpTooltips: true,
  selectedProcessPid: null,
  modalOpen: null,
};

function createUIStore() {
  const { subscribe, set, update } = writable<UIState>(initialState);

  return {
    subscribe,

    // Set view mode
    setViewMode: (mode: ViewMode) => {
      update(state => ({ ...state, viewMode: mode }));
    },

    // Toggle sidebar
    toggleSidebar: () => {
      update(state => ({ ...state, sidebarOpen: !state.sidebarOpen }));
    },

    // Set sidebar state
    setSidebarOpen: (open: boolean) => {
      update(state => ({ ...state, sidebarOpen: open }));
    },

    // Toggle guided mode
    toggleGuidedMode: () => {
      update(state => ({ ...state, guidedModeEnabled: !state.guidedModeEnabled }));
    },

    // Set theme
    setTheme: (theme: Theme) => {
      update(state => ({ ...state, theme }));
      // Apply theme to document
      if (typeof document !== 'undefined') {
        document.documentElement.classList.remove('light', 'dark');
        if (theme !== 'system') {
          document.documentElement.classList.add(theme);
        }
      }
    },

    // Select a process
    selectProcess: (pid: number | null) => {
      update(state => ({ ...state, selectedProcessPid: pid }));
    },

    // Open modal
    openModal: (modalId: string) => {
      update(state => ({ ...state, modalOpen: modalId }));
    },

    // Close modal
    closeModal: () => {
      update(state => ({ ...state, modalOpen: null }));
    },

    // Toggle help tooltips
    toggleHelpTooltips: () => {
      update(state => ({ ...state, showHelpTooltips: !state.showHelpTooltips }));
    },

    // Reset to initial state
    reset: () => {
      set(initialState);
    },
  };
}

export const uiStore = createUIStore();

// Derived stores
export const currentView = derived(uiStore, $state => $state.viewMode);
export const isSidebarOpen = derived(uiStore, $state => $state.sidebarOpen);
export const isModalOpen = derived(uiStore, $state => $state.modalOpen !== null);
export const selectedProcess = derived(uiStore, $state => $state.selectedProcessPid);
