# tools/context_management.py
import os
import json
from typing import List, Optional
from models.context import ContextEntry

class ContextManagementTool:
    def __init__(self, session_id: str, persistence_path: str = "./context_data/"):
        self.session_id = session_id
        self.persistence_path = persistence_path
        self.context_entries: List[ContextEntry] = []
        
        # Ensure directory exists
        os.makedirs(persistence_path, exist_ok=True)
        
        # Load existing context if available
        self._load_context()
    
    def _get_file_path(self):
        return os.path.join(self.persistence_path, f"{self.session_id}.json")
    
    def _load_context(self):
        file_path = self._get_file_path()
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r') as f:
                    data = json.load(f)
                    self.context_entries = [ContextEntry(**entry) for entry in data]
            except Exception as e:
                print(f"Error loading context: {e}")
    
    def _save_context(self):
        file_path = self._get_file_path()
        try:
            with open(file_path, 'w') as f:
                json.dump([entry.dict() for entry in self.context_entries], f, indent=2)
        except Exception as e:
            print(f"Error saving context: {e}")
    
    def add_entry(self, entry: ContextEntry):
        """Add a new context entry and persist it"""
        self.context_entries.append(entry)
        self._save_context()
    
    def get_entries(self, tool_name: Optional[str] = None) -> List[ContextEntry]:
        """Get all entries or filter by tool name"""
        if tool_name:
            return [entry for entry in self.context_entries if entry.tool_name == tool_name]
        return self.context_entries
    
    def get_latest_entry(self, tool_name: str) -> Optional[ContextEntry]:
        """Get the most recent entry from a specific tool"""
        entries = self.get_entries(tool_name)
        if entries:
            return sorted(entries, key=lambda x: x.timestamp, reverse=True)[0]
        return None
    
    def clear(self):
        """Clear all context entries"""
        self.context_entries = []
        self._save_context()