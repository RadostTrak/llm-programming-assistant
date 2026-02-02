from agents import Agent, RunContextWrapper, function_tool
from state import DebuggingState


def create_record_handoff_function(from_agent_name: str, to_agent: Agent):
    """
    Factory function that creates record handoff functions that record to state.
    """
    
    def record_handoff(ctx: RunContextWrapper[dict], reason: str):
        state: DebuggingState = ctx.context["state"]
        state.record_handoff(
            from_agent=from_agent_name,
            to_agent=to_agent.name,
            reason=reason
        )
        
        return None
    
    record_handoff.__name__ = f"transfer_to_{to_agent.name}"
    record_handoff.__doc__ = f"Transfer conversation to {to_agent.name} agent. Provide a reason for the transfer."
    
    return function_tool(record_handoff)