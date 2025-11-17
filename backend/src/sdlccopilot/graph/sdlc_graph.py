
from langgraph.graph import StateGraph, START, END
from src.sdlccopilot.states.sdlc import SDLCState
from langgraph.checkpoint.memory import MemorySaver
from src.sdlccopilot.nodes.user_story_nodes import UserStoryNodes
from src.sdlccopilot.nodes.functional_document_nodes import FunctionalDocumentNodes
from src.sdlccopilot.nodes.technical_document_nodes import TechnicalDocumentNodes
from src.sdlccopilot.nodes.development_nodes import DevelopmentNodes
from src.sdlccopilot.nodes.test_cases_nodes import TestCaseNodes
from src.sdlccopilot.nodes.security_review_nodes import SecurityReviewNodes
from src.sdlccopilot.nodes.qa_testing_nodes import QATestingNodes
from src.sdlccopilot.nodes.deployment_nodes import DeploymentNodes
from IPython.display import Image, display
from src.sdlccopilot.llms.gemini import GeminiLLM
from src.sdlccopilot.llms.groq import GroqLLM
from src.sdlccopilot.llms.anthropic import AnthropicLLM
from src.sdlccopilot.logger import logging

## LLMs 
gemini_llm = GeminiLLM("gemini-2.0-flash").get()
qwen_llm = GroqLLM("qwen/qwen3-32b").get()
anthropic_llm = AnthropicLLM("claude-3-5-sonnet-20241022").get()

class SDLCGraphBuilder:
    def __init__(self):
        self.sdlc_graph_builder=StateGraph(SDLCState)
        self.story_node = UserStoryNodes(gemini_llm)
        self.functional_document_node = FunctionalDocumentNodes(qwen_llm)
        self.technical_document_node = TechnicalDocumentNodes(qwen_llm)
        self.development_node = DevelopmentNodes(anthropic_llm)
        self.security_review_node = SecurityReviewNodes(gemini_llm, anthropic_llm)
        self.test_case_node = TestCaseNodes(gemini_llm)
        self.qa_testing_node = QATestingNodes(gemini_llm, anthropic_llm)
        self.deployment_node = DeploymentNodes(qwen_llm)
        
    def build(self):
        """
        Builds the SDLC graph.
        """
        logging.info("Building SDLC graph...")
        
        # User Story
        self.sdlc_graph_builder.add_node("process_project_requirements", self.story_node.process_project_requirements)
        self.sdlc_graph_builder.add_node("generate_user_stories", self.story_node.generate_user_stories)
        self.sdlc_graph_builder.add_node("review_user_stories", self.story_node.review_user_stories)
        self.sdlc_graph_builder.add_node("revised_user_stories", self.story_node.revised_user_stories)
        
        ## Functional documents 
        self.sdlc_graph_builder.add_node("create_functional_documents", self.functional_document_node.create_functional_documents)
        self.sdlc_graph_builder.add_node("review_functional_documents", self.functional_document_node.review_functional_documents)
        self.sdlc_graph_builder.add_node("revise_functional_documents", self.functional_document_node.revise_functional_documents)

        ## Technical documents 
        self.sdlc_graph_builder.add_node("create_technical_documents", self.technical_document_node.create_technical_documents)
        self.sdlc_graph_builder.add_node("review_technical_documents", self.technical_document_node.review_technical_documents)
        self.sdlc_graph_builder.add_node("revise_technical_documents", self.technical_document_node.revise_technical_documents)
        
        ## Frontend Code Development
        self.sdlc_graph_builder.add_node("generate_frontend_code", self.development_node.generate_frontend_code)
        self.sdlc_graph_builder.add_node("review_frontend_code", self.development_node.review_frontend_code)
        self.sdlc_graph_builder.add_node("fix_frontend_code", self.development_node.fix_frontend_code)
        
        ## Backend Code Development
        self.sdlc_graph_builder.add_node("generate_backend_code", self.development_node.generate_backend_code)
        self.sdlc_graph_builder.add_node("review_backend_code", self.development_node.review_backend_code)
        self.sdlc_graph_builder.add_node("fix_backend_code", self.development_node.fix_backend_code)
        
        ## Security Review
        self.sdlc_graph_builder.add_node("generate_security_reviews", self.security_review_node.generate_security_reviews)
        self.sdlc_graph_builder.add_node("security_review", self.security_review_node.security_review)
        self.sdlc_graph_builder.add_node("fix_code_after_security_review", self.security_review_node.fix_code_after_security_review)
    
        ## Test Cases
        self.sdlc_graph_builder.add_node("generate_test_cases", self.test_case_node.generate_test_cases)
        self.sdlc_graph_builder.add_node("test_cases_review", self.test_case_node.test_cases_review)
        self.sdlc_graph_builder.add_node("revised_test_cases", self.test_case_node.revised_test_cases)
        
        ## QA testing
        self.sdlc_graph_builder.add_node("perform_qa_testing", self.qa_testing_node.perform_qa_testing)
        self.sdlc_graph_builder.add_node("fix_code_after_qa_testing", self.qa_testing_node.fix_code_after_qa_testing)
        
        ## Deployment
        self.sdlc_graph_builder.add_node("generate_deployment_steps", self.deployment_node.generate_deployment_steps)
        
        ## Adding edges
        ## User Story
        self.sdlc_graph_builder.add_edge(START, "process_project_requirements")
        self.sdlc_graph_builder.add_edge("process_project_requirements", "generate_user_stories")
        self.sdlc_graph_builder.add_edge("generate_user_stories", "review_user_stories")
        self.sdlc_graph_builder.add_conditional_edges(
            "review_user_stories", self.story_node.should_revise_user_stories, {'approved' : "create_functional_documents", 'feedback' : 'revised_user_stories'}
        )
        self.sdlc_graph_builder.add_edge("revised_user_stories", "review_user_stories")
        
        # Functional documents
        self.sdlc_graph_builder.add_edge("create_functional_documents", "review_functional_documents")
        self.sdlc_graph_builder.add_conditional_edges(
            "review_functional_documents", self.functional_document_node.should_revise_functional_documents, {'approved' : "create_technical_documents", 'feedback' : 'revise_functional_documents'}
        )
        self.sdlc_graph_builder.add_edge("revise_functional_documents", "review_functional_documents")
        
        # Technical documents
        self.sdlc_graph_builder.add_edge("create_technical_documents", "review_technical_documents")
        self.sdlc_graph_builder.add_conditional_edges(
            "review_technical_documents", self.technical_document_node.should_revise_technical_documents, {'approved' : "generate_frontend_code", 'feedback' : 'revise_technical_documents'}
        )
        self.sdlc_graph_builder.add_edge("revise_technical_documents", "review_technical_documents")
        
        ## Frontend code 
        self.sdlc_graph_builder.add_edge("generate_frontend_code", "review_frontend_code")
        self.sdlc_graph_builder.add_conditional_edges(
            "review_frontend_code",
            self.development_node.should_fix_frontend_code,
            {
                "feedback" : "fix_frontend_code",
                "approved" : "generate_backend_code"
            }
        )
        self.sdlc_graph_builder.add_edge("fix_frontend_code", "review_frontend_code")

        ## Backend code 
        self.sdlc_graph_builder.add_edge("generate_backend_code", "review_backend_code")
        self.sdlc_graph_builder.add_conditional_edges(
            "review_backend_code",
            self.development_node.should_fix_backend_code,
            {
                "feedback" : "fix_backend_code",
                "approved" : "generate_security_reviews" 
            }
        )
        self.sdlc_graph_builder.add_edge("fix_backend_code", "review_backend_code")
        
        ## Security Review
        self.sdlc_graph_builder.add_edge("generate_security_reviews", "security_review")
        self.sdlc_graph_builder.add_conditional_edges(
            "security_review",
            self.security_review_node.should_fix_code_after_security_review,
            {
                "feedback" : "fix_code_after_security_review",
                "approved" : "generate_test_cases"
            }
        )
        self.sdlc_graph_builder.add_edge("fix_code_after_security_review", "review_backend_code")

        ## test cases
        self.sdlc_graph_builder.add_edge("generate_test_cases", "test_cases_review")
        self.sdlc_graph_builder.add_conditional_edges(
            "test_cases_review",
            self.test_case_node.should_fix_test_cases,
            {
                "feedback" : "revised_test_cases",
                "approved" : "perform_qa_testing"
            }
        )

        self.sdlc_graph_builder.add_edge("revised_test_cases", "test_cases_review")
        
        ## QA testing 
        self.sdlc_graph_builder.add_conditional_edges(
            "perform_qa_testing",
            self.qa_testing_node.should_fix_code_after_qa_testing,
            {
                "failed" : "fix_code_after_qa_testing",
                "passed" : "generate_deployment_steps"
            }
        )
        
        self.sdlc_graph_builder.add_edge("fix_code_after_qa_testing", "review_backend_code")
        
        ## Deployment
        self.sdlc_graph_builder.add_edge("generate_deployment_steps", END)
                
        memory = MemorySaver()
        sdlc_workflow = self.sdlc_graph_builder.compile(checkpointer=memory, interrupt_before=['review_user_stories', 'review_functional_documents', 'review_technical_documents', 'review_frontend_code', 'review_backend_code', 'security_review', 'test_cases_review'])
        logging.info("SDLC workflow built successfully !!!")
        return sdlc_workflow
    
if __name__ == "__main__":
    pass
    # sdlc_graph_builder = SDLCGraphBuilder()
    # sdlc_workflow = sdlc_graph_builder.build()
    # # # Save it to a file
    # png_data = sdlc_workflow.get_graph().draw_mermaid_png()
    # with open("sdlc_workflow.png", "wb") as f:
    #     f.write(png_data)