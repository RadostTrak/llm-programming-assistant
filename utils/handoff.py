from agents import Agent, RunContextWrapper, Agent, function_tool
from state import DebuggingState

def create_handoff_function(from_agent_name: str, to_agent: Agent):
    """
    Factory function that creates handoff functions that automatically record to state.
    """
    
    @function_tool
    def handoff_function(ctx: RunContextWrapper[dict], reason: str):
        state: DebuggingState = ctx.context["state"]
        state.record_handoff(
            from_agent=from_agent_name,
            to_agent=to_agent.name,
            reason=reason
        )
        
        return to_agent
    
    handoff_function.__name__ = f"transfer_to_{to_agent.name}"
    return handoff_function