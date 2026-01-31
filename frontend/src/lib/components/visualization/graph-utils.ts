/**
 * Graph Utilities for vis-network Process Graph
 * 
 * Transforms process tree data into vis-network compatible format
 * and provides configuration helpers.
 */

import type { ProcessTreeNode } from '$lib/api/types';
import { colors } from '$lib/styles/design-tokens';

// =============================================================================
// VIS-NETWORK TYPE DEFINITIONS
// =============================================================================

export interface VisNode {
	id: number;
	label: string;
	title: string;
	color: {
		background: string;
		border: string;
		highlight: {
			background: string;
			border: string;
		};
		hover: {
			background: string;
			border: string;
		};
	};
	font: {
		color: string;
		size: number;
	};
	borderWidth: number;
	borderWidthSelected: number;
	shape: string;
	size: number;
	// Custom data
	riskScore: number;
	legitimacy: string;
	processName: string;
	imagePath: string | null;
	behaviorTags: string[];
	eventCount: number;
}

export interface VisEdge {
	id: string;
	from: number;
	to: number;
	arrows: string;
	color: {
		color: string;
		highlight: string;
		hover: string;
		opacity: number;
	};
	width: number;
	smooth: {
		type: string;
		roundness: number;
	};
}

export interface GraphData {
	nodes: VisNode[];
	edges: VisEdge[];
}

// =============================================================================
// COLOR HELPERS
// =============================================================================

interface RiskColorScheme {
	background: string;
	border: string;
	highlight: string;
	hover: string;
}

/**
 * Get color scheme based on risk score
 */
export function getRiskColorScheme(riskScore: number): RiskColorScheme {
	if (riskScore >= 50) {
		return {
			background: 'rgba(239, 68, 68, 0.3)',
			border: colors.risk.high,
			highlight: 'rgba(239, 68, 68, 0.5)',
			hover: 'rgba(239, 68, 68, 0.4)',
		};
	}
	if (riskScore >= 20) {
		return {
			background: 'rgba(249, 115, 22, 0.3)',
			border: colors.risk.medium,
			highlight: 'rgba(249, 115, 22, 0.5)',
			hover: 'rgba(249, 115, 22, 0.4)',
		};
	}
	if (riskScore > 0) {
		return {
			background: 'rgba(234, 179, 8, 0.3)',
			border: colors.risk.low,
			highlight: 'rgba(234, 179, 8, 0.5)',
			hover: 'rgba(234, 179, 8, 0.4)',
		};
	}
	return {
		background: 'rgba(107, 114, 128, 0.3)',
		border: colors.text.muted,
		highlight: 'rgba(107, 114, 128, 0.5)',
		hover: 'rgba(107, 114, 128, 0.4)',
	};
}

/**
 * Calculate node size based on event count and risk
 */
export function calculateNodeSize(eventCount: number, riskScore: number): number {
	const baseSize = 20;
	const eventBonus = Math.min(Math.log10(eventCount + 1) * 5, 15);
	const riskBonus = riskScore >= 50 ? 10 : riskScore >= 20 ? 5 : 0;
	return baseSize + eventBonus + riskBonus;
}

// =============================================================================
// DATA TRANSFORMATION
// =============================================================================

/**
 * Flatten process tree into array with parent references
 */
interface FlattenedNode {
	node: ProcessTreeNode;
	parentPid: number | null;
}

function flattenTree(nodes: ProcessTreeNode[], parentPid: number | null = null): FlattenedNode[] {
	const result: FlattenedNode[] = [];
	
	for (const node of nodes) {
		result.push({ node, parentPid });
		if (node.children && node.children.length > 0) {
			result.push(...flattenTree(node.children, node.process.pid));
		}
	}
	
	return result;
}

/**
 * Transform process tree data to vis-network format
 */
export function transformTreeToGraph(tree: ProcessTreeNode[]): GraphData {
	const flatNodes = flattenTree(tree);
	const nodes: VisNode[] = [];
	const edges: VisEdge[] = [];
	const seenPids = new Set<number>();

	for (const { node, parentPid } of flatNodes) {
		const process = node.process;
		
		// Skip duplicate PIDs
		if (seenPids.has(process.pid)) continue;
		seenPids.add(process.pid);

		const colorScheme = getRiskColorScheme(process.risk_score);
		const nodeSize = calculateNodeSize(process.event_count, process.risk_score);

		// Create node
		const visNode: VisNode = {
			id: process.pid,
			label: `${process.process_name}\n(${process.pid})`,
			title: createNodeTooltip(process),
			color: {
				background: colorScheme.background,
				border: colorScheme.border,
				highlight: {
					background: colorScheme.highlight,
					border: colorScheme.border,
				},
				hover: {
					background: colorScheme.hover,
					border: colorScheme.border,
				},
			},
			font: {
				color: '#ffffff',
				size: 12,
			},
			borderWidth: 2,
			borderWidthSelected: 4,
			shape: 'dot',
			size: nodeSize,
			// Custom data
			riskScore: process.risk_score,
			legitimacy: process.legitimacy,
			processName: process.process_name,
			imagePath: process.image_path,
			behaviorTags: process.behavior_tags,
			eventCount: process.event_count,
		};

		nodes.push(visNode);

		// Create edge to parent
		if (parentPid !== null && seenPids.has(parentPid)) {
			const edge: VisEdge = {
				id: `${parentPid}-${process.pid}`,
				from: parentPid,
				to: process.pid,
				arrows: 'to',
				color: {
					color: 'rgba(255, 255, 255, 0.2)',
					highlight: colors.accent.primary,
					hover: 'rgba(255, 255, 255, 0.4)',
					opacity: 0.8,
				},
				width: 1,
				smooth: {
					type: 'cubicBezier',
					roundness: 0.5,
				},
			};
			edges.push(edge);
		}
	}

	return { nodes, edges };
}

/**
 * Create HTML tooltip content for a node
 */
function createNodeTooltip(process: ProcessTreeNode['process']): string {
	const legitimacyColor = 
		process.legitimacy === 'malicious' ? colors.risk.high :
		process.legitimacy === 'suspicious' ? colors.risk.medium :
		process.legitimacy === 'legitimate' ? colors.status.success :
		colors.text.muted;

	const tags = process.behavior_tags.length > 0 
		? process.behavior_tags.slice(0, 3).join(', ') 
		: 'None';

	return `
		<div style="
			background: rgba(10, 10, 15, 0.95);
			border: 1px solid rgba(255, 255, 255, 0.1);
			border-radius: 8px;
			padding: 12px;
			font-family: system-ui, sans-serif;
			font-size: 12px;
			color: #ffffff;
			max-width: 280px;
		">
			<div style="font-weight: 600; font-size: 14px; margin-bottom: 8px;">
				${process.process_name}
			</div>
			<div style="color: rgba(255,255,255,0.6); margin-bottom: 4px;">
				PID: ${process.pid}
			</div>
			${process.image_path ? `
				<div style="color: rgba(255,255,255,0.5); font-size: 11px; margin-bottom: 8px; word-break: break-all;">
					${process.image_path}
				</div>
			` : ''}
			<div style="display: flex; gap: 8px; margin-bottom: 8px;">
				<span style="
					padding: 2px 8px;
					border-radius: 4px;
					font-size: 11px;
					font-weight: 600;
					color: ${process.risk_score >= 50 ? colors.risk.high : process.risk_score >= 20 ? colors.risk.medium : colors.text.secondary};
					background: ${process.risk_score >= 50 ? colors.risk.highBg : process.risk_score >= 20 ? colors.risk.mediumBg : 'rgba(107, 114, 128, 0.2)'};
				">
					Risk: ${process.risk_score}
				</span>
				<span style="
					padding: 2px 8px;
					border-radius: 4px;
					font-size: 11px;
					color: ${legitimacyColor};
					background: rgba(255, 255, 255, 0.05);
					text-transform: capitalize;
				">
					${process.legitimacy}
				</span>
			</div>
			<div style="color: rgba(255,255,255,0.5); font-size: 11px;">
				Events: ${process.event_count} | Tags: ${tags}
			</div>
		</div>
	`;
}

// =============================================================================
// VIS-NETWORK CONFIGURATION
// =============================================================================

/**
 * Get vis-network options for process graph
 */
export function getGraphOptions(): object {
	return {
		autoResize: true,
		height: '100%',
		width: '100%',
		nodes: {
			shape: 'dot',
			font: {
				face: 'system-ui, sans-serif',
				color: '#ffffff',
				size: 12,
				strokeWidth: 0,
			},
			scaling: {
				min: 15,
				max: 40,
			},
		},
		edges: {
			arrows: {
				to: {
					enabled: true,
					scaleFactor: 0.5,
				},
			},
			smooth: {
				enabled: true,
				type: 'cubicBezier',
				roundness: 0.5,
			},
		},
		physics: {
			enabled: true,
			solver: 'forceAtlas2Based',
			forceAtlas2Based: {
				gravitationalConstant: -50,
				centralGravity: 0.01,
				springLength: 100,
				springConstant: 0.08,
				damping: 0.4,
				avoidOverlap: 0.5,
			},
			stabilization: {
				enabled: true,
				iterations: 200,
				updateInterval: 25,
			},
		},
		interaction: {
			hover: true,
			tooltipDelay: 100,
			hideEdgesOnDrag: true,
			hideEdgesOnZoom: true,
			multiselect: false,
			navigationButtons: true,
			keyboard: {
				enabled: true,
				speed: { x: 10, y: 10, zoom: 0.02 },
			},
			zoomView: true,
		},
		layout: {
			improvedLayout: true,
			hierarchical: false,
		},
	};
}

// =============================================================================
// FILTERING HELPERS
// =============================================================================

export type FilterMode = 'all' | 'flagged' | 'high-risk';

/**
 * Filter nodes based on mode
 */
export function filterNodes(nodes: VisNode[], mode: FilterMode): VisNode[] {
	switch (mode) {
		case 'flagged':
			return nodes.filter(n => n.riskScore > 0);
		case 'high-risk':
			return nodes.filter(n => n.riskScore >= 50);
		default:
			return nodes;
	}
}

/**
 * Filter edges to only include those connecting visible nodes
 */
export function filterEdges(edges: VisEdge[], visibleNodeIds: Set<number>): VisEdge[] {
	return edges.filter(e => visibleNodeIds.has(e.from) && visibleNodeIds.has(e.to));
}

/**
 * Search nodes by process name
 */
export function searchNodes(nodes: VisNode[], query: string): VisNode[] {
	if (!query.trim()) return nodes;
	const lowerQuery = query.toLowerCase();
	return nodes.filter(n => 
		n.processName.toLowerCase().includes(lowerQuery) ||
		n.id.toString().includes(lowerQuery) ||
		(n.imagePath?.toLowerCase().includes(lowerQuery) ?? false)
	);
}
