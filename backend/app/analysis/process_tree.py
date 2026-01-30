"""
Process tree builder - creates hierarchical process relationships.
"""

from app.models import ProcessInfo, ProcessTreeNode


def build_process_tree(processes: list[ProcessInfo]) -> list[ProcessTreeNode]:
    """
    Build a hierarchical process tree from a flat list of processes.
    
    Returns a list of root nodes (processes without parents in our data).
    """
    # Create PID lookup
    pid_to_process = {p.pid: p for p in processes}
    pid_to_node: dict[int, ProcessTreeNode] = {}
    
    # Create nodes for all processes
    for process in processes:
        pid_to_node[process.pid] = ProcessTreeNode(
            process=process,
            children=[],
            depth=0
        )
    
    # Build parent-child relationships
    roots: list[ProcessTreeNode] = []
    
    for process in processes:
        node = pid_to_node[process.pid]
        
        if process.parent_pid and process.parent_pid in pid_to_node:
            # Has a parent in our data
            parent_node = pid_to_node[process.parent_pid]
            parent_node.children.append(node)
        else:
            # Root process (no parent or parent not in data)
            roots.append(node)
    
    # Set depths
    def set_depth(node: ProcessTreeNode, depth: int) -> None:
        node.depth = depth
        for child in node.children:
            set_depth(child, depth + 1)
    
    for root in roots:
        set_depth(root, 0)
    
    # Sort roots by risk (highest first)
    roots.sort(key=lambda n: n.process.risk_score, reverse=True)
    
    # Sort children by risk within each level
    def sort_children(node: ProcessTreeNode) -> None:
        node.children.sort(key=lambda n: n.process.risk_score, reverse=True)
        for child in node.children:
            sort_children(child)
    
    for root in roots:
        sort_children(root)
    
    return roots


def flatten_tree(tree: list[ProcessTreeNode]) -> list[ProcessInfo]:
    """Flatten a tree back to a list, preserving parent-first order."""
    result: list[ProcessInfo] = []
    
    def traverse(node: ProcessTreeNode) -> None:
        result.append(node.process)
        for child in node.children:
            traverse(child)
    
    for root in tree:
        traverse(root)
    
    return result


def tree_to_dict(tree: list[ProcessTreeNode]) -> list[dict]:
    """Convert process tree to dictionary format for JSON serialization."""
    def node_to_dict(node: ProcessTreeNode) -> dict:
        return {
            "process": {
                "pid": node.process.pid,
                "process_name": node.process.process_name,
                "image_path": node.process.image_path,
                "risk_score": node.process.risk_score,
                "legitimacy": node.process.legitimacy.value,
                "behavior_tags": node.process.behavior_tags,
                "event_count": node.process.event_count,
            },
            "depth": node.depth,
            "children": [node_to_dict(c) for c in node.children]
        }
    
    return [node_to_dict(root) for root in tree]
