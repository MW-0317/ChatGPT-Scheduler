import os
import ast
from collections import defaultdict, deque

def parse_imports(file_path):
    """Parse a Python file to extract import statements."""
    imports = set()
    with open(file_path, 'r') as file:
        tree = ast.parse(file.read(), filename=file_path)
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.add(alias.name.split('.')[0])  # Handle module name only
            elif isinstance(node, ast.ImportFrom):
                imports.add(node.module.split('.')[0])  # Handle module name only
    return imports

def build_dependency_graph(files):
    """Build a dependency graph from the import statements in each file."""
    graph = defaultdict(set)
    all_files = set(files)
    
    for file in files:
        imports = parse_imports(file)
        for imp in imports:
            for other_file in files:
                # Check if the import matches the base name of another file
                if imp == os.path.splitext(other_file)[0]:
                    graph[other_file].add(file)  # other_file depends on file
    
    return graph

def topological_sort(graph):
    """Perform topological sort on the dependency graph."""
    # Initialize indegree for all nodes
    indegree = defaultdict(int)
    for node in graph:
        for neighbor in graph[node]:
            indegree[neighbor] += 1
    
    # Nodes with zero indegree
    queue = deque(node for node in graph if indegree[node] == 0)
    sorted_files = []
    
    while queue:
        node = queue.popleft()
        sorted_files.append(node)
        for neighbor in graph[node]:
            indegree[neighbor] -= 1
            if indegree[neighbor] == 0:
                queue.append(neighbor)
    
    # Check if sorting was possible (i.e., no cycles)
    if len(sorted_files) != len(graph):
        raise ValueError("A cycle was detected in the dependency graph")
    
    return sorted_files

def remove_internal_imports(file_path, included_files):
    """Remove import statements not necessary between files."""
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    imports_to_remove = set()
    for line in lines:
        if line.strip().startswith('import ') or line.strip().startswith('from '):
            import_name = line.split()[1].split('.')[0]
            if f"{import_name}.py" in included_files:
                imports_to_remove.add(line.strip())
    
    cleaned_lines = [line for line in lines if line.strip() not in imports_to_remove]
    
    return cleaned_lines

def concatenate_scripts(output_file):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    files = [f for f in os.listdir(current_dir) if f.endswith('.py') and f not in (os.path.basename(__file__), output_file)]
    
    graph = build_dependency_graph(files)
    sorted_files = topological_sort(graph)

    included_files = {file for file in sorted_files}
    
    with open(output_file, 'w') as outfile:
        for file_name in sorted_files:
            print(f"Processing {file_name}")
            cleaned_lines = remove_internal_imports(file_name, included_files)
            outfile.writelines(cleaned_lines)
            outfile.write("\n\n")  # Add newline between files
    
    print(f"Done. All Python scripts have been concatenated into {output_file}.")

if __name__ == "__main__":
    concatenate_scripts('scheduler-gpt.py')
