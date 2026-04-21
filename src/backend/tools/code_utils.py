import ast
from typing import List, Dict

def analyze_code_structure(code_snippet: str) -> Dict:
    """
    Uses AST to extract function names, classes, and basic structure.
    Useful for DocGen and Reviewer agents.
    """
    try:
        tree = ast.parse(code_snippet)
        results = {
            "classes": [],
            "functions": [],
            "imports": []
        }
        
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                results["classes"].append(node.name)
            elif isinstance(node, ast.FunctionDef):
                results["functions"].append(node.name)
            elif isinstance(node, ast.Import) or isinstance(node, ast.ImportFrom):
                results["imports"].append(ast.dump(node))
                
        return results
    except Exception as e:
        return {"error": str(e)}

def scan_for_risks(code_snippet: str) -> List[str]:
    """
    Simple keyword-based security and quality scan.
    """
    risks = []
    keywords = {
        "eval(": "Risk: Usage of eval detected (Security)",
        "exec(": "Risk: Usage of exec detected (Security)",
        "os.system(": "Risk: Shell command execution (Security)",
        "subprocess.Popen(": "Risk: Subprocess execution (Security)",
        "password =": "Risk: Hardcoded password placeholder found",
        "print(": "Info: Print statements found (Performance/Logging)",
        "try: pass": "Warning: Silenced exceptions detected"
    }
    
    for key, msg in keywords.items():
        if key in code_snippet:
            risks.append(msg)
            
    return risks
