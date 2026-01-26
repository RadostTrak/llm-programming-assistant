from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional
from enum import Enum

class Phase(Enum):
    INITIAL = 'initial'
    TRIAGING = 'triaging'
    DIAGNOSING = 'diagnosing'
    PROPOSING = 'proposing'
    TESTING = 'testing'
    RESOLVED = 'resolved'

@dataclass
class DebuggingState:
    """Shared state for multi-agent debugging system"""
    
    # Core debugging info
    issue_description: Optional[str] = None # User's description of the issue
    code_context: Dict[str, str] = field(default_factory=dict) # User-provided code snippets
    
    # Agent findings
    diagnostic_findings: Dict[str, str] = field(default_factory=dict) # Stores what each agent discovered
    attempted_solutions: List[Dict] = field(default_factory=list) # Track what solutions were attempted
    
    # Progress tracking
    current_phase: str = Phase.INITIAL.value # Current phase of debugging
    conversation_history: List[Dict] = field(default_factory=list) # Chat history between user and agents, Example: [{"role": "user", "message": "My code crashes"}, {"role": "agent", "message": "Can you share the error?"}]
    
    # Convert the entire state object to a dictionary (for storing in a database, etc.)
    def to_dict(self) -> dict:
        return asdict(self)
    
    # The opposite of to_dict: create a state object from a dictionary
    @classmethod
    def from_dict(cls, data: dict):
        return cls(**{k: v for k, v in data.items() if k in cls.__annotations__})