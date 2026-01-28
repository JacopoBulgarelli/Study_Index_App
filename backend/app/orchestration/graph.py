from langgraph.graph import StateGraph, END
from typing import TypedDict, List, Optional, Dict, Any
from .state import AgentState
from .nodes import detect_intent, retrieve_section, generate_answer, generate_quiz, update_memory

class StudyAssistantGraph:
    def __init__(self):
        workflow = StateGraph(AgentState)

        workflow.add_node("detect_intent", detect_intent)
        workflow.add_node("retrieve_section", retrieve_section)
        workflow.add_node("generate_answer", generate_answer)
        workflow.add_node("generate_quiz", generate_quiz)
        workflow.add_node("update_memory", update_memory)

        # Define edges
        workflow.set_entry_point("detect_intent")
        
        workflow.add_edge("detect_intent", "retrieve_section")
        workflow.add_conditional_edges(
            "retrieve_section",
            self._route_based_on_intent,
            {
                "answer": "generate_answer",
                "quiz": "generate_quiz",
                "review": "generate_quiz"  # Review mode quiz
            }
        )
        workflow.add_edge("generate_answer", "update_memory")
        workflow.add_edge("generate_quiz", "update_memory")
        workflow.add_edge("update_memory", END)
        
        self.graph = workflow.compile()

    def _route_based_on_intent(self, state: AgentState) -> str:
        """Route to appropriate node based on intent"""
        return state.get("intent", "answer")
    
    async def run(self, query: str, user_id: str, document_id: str = None) -> Dict[str, Any]:
        """Execute the graph"""
        initial_state = AgentState(
            query=query,
            user_id=user_id,
            document_id=document_id,
            memory_context=""
        )
        
        result = await self.graph.ainvoke(initial_state)
        return result