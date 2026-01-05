import json
import os
from datetime import datetime
from typing import Dict, Any, Optional
from pathlib import Path

class FileManager:
    def __init__(self, base_dir: Optional[str] = None):
        if base_dir is None:
            base_dir = os.path.expanduser("~/.cubesat_budget_analyzer")
        self.base_dir = Path(base_dir)
        self.projects_dir = self.base_dir / "projects"
        self.config_dir = self.base_dir / "config"
        self._ensure_directories()

    def _ensure_directories(self):
        """Create necessary directories if they don't exist."""
        self.base_dir.mkdir(exist_ok=True)
        self.projects_dir.mkdir(exist_ok=True)
        self.config_dir.mkdir(exist_ok=True)

    def save_project(self, name: str, data: Dict[str, Any]) -> str:
        """Save project data to a file."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{name}_{timestamp}.json"
        filepath = self.projects_dir / filename

        # Add metadata
        data["metadata"] = {
            "name": name,
            "timestamp": timestamp,
            "version": "1.0.0"
        }

        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        
        return str(filepath)

    def load_project(self, filepath: str) -> Dict[str, Any]:
        """Load project data from a file."""
        with open(filepath, 'r') as f:
            return json.load(f)

    def list_projects(self) -> list[Dict[str, Any]]:
        """List all saved projects with their metadata."""
        projects = []
        for file in self.projects_dir.glob("*.json"):
            try:
                with open(file, 'r') as f:
                    data = json.load(f)
                    metadata = data.get("metadata", {})
                    metadata["filepath"] = str(file)
                    projects.append(metadata)
            except Exception as e:
                print(f"Error loading {file}: {e}")
        return sorted(projects, key=lambda x: x.get("timestamp", ""), reverse=True)

    def save_config(self, config: Dict[str, Any]):
        """Save application configuration."""
        filepath = self.config_dir / "config.json"
        with open(filepath, 'w') as f:
            json.dump(config, f, indent=2)

    def load_config(self) -> Dict[str, Any]:
        """Load application configuration."""
        filepath = self.config_dir / "config.json"
        if not filepath.exists():
            return {}
        with open(filepath, 'r') as f:
            return json.load(f)

    def export_report(self, data: Dict[str, Any], format: str = "pdf") -> str:
        """Export analysis results to a report file."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"report_{timestamp}.{format}"
        filepath = self.base_dir / "reports" / filename
        
        # Ensure reports directory exists
        (self.base_dir / "reports").mkdir(exist_ok=True)
        
        if format == "json":
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2)
        elif format == "csv":
            # TODO: Implement CSV export
            pass
        elif format == "pdf":
            # TODO: Implement PDF export using reportlab
            pass
        
        return str(filepath) 