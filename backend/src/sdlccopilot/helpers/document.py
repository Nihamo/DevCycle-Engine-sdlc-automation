from src.sdlccopilot.prompts.prompt_template import prompt_template
from src.sdlccopilot.prompts.document import functional_document_system_prompt, revised_functional_document_system_prompt, technical_document_system_prompt, revised_technical_document_system_prompt
from src.sdlccopilot.logger import logging
from src.sdlccopilot.exception import CustomException
import sys

class DocumentHelper:
    def __init__(self, llm):
        self.llm = llm

    def generate_functional_document_from_llm(self, user_stories):
        try:
            logging.info("Generating functional document with LLM...")
            # Truncate user_stories if too long to avoid token limits
            user_stories_str = str(user_stories)
            if len(user_stories_str) > 2000:
                user_stories_str = user_stories_str[:2000] + "... (truncated for token limits)"
            user_query = f"Create a functional document for these user stories: {user_stories_str}."
            chain = prompt_template | self.llm 
            response = chain.invoke({"system_prompt" : functional_document_system_prompt, "human_query" : user_query})
            logging.info("Functional document generated with LLM.")
            logging.info(f"In generate_functional_document_from_llm : {response.content}")
            return response.content
        except Exception as e:
            logging.error(f"Error generating functional document: {str(e)}")
            raise CustomException(e, sys)
    
    def revised_functional_document_from_llm(self, functional_document, user_feedback):
        try:
            logging.info("Revising functional document with LLM...")
            user_query = f"""EXISTING FUNCTIONAL DOCUMENT (PRESERVE ALL CONTENT NOT MENTIONED IN FEEDBACK):
{functional_document}

USER FEEDBACK (APPLY ONLY THESE CHANGES):
{user_feedback}

INSTRUCTIONS:
- Keep ALL existing sections, paragraphs, and content that are NOT mentioned in the feedback
- Only modify the specific parts requested in the user feedback
- Return the complete document with all preserved content and incremental changes applied"""
            chain = prompt_template | self.llm 
            response = chain.invoke({"system_prompt" : revised_functional_document_system_prompt, "human_query" : user_query})
            logging.info("Functional document revised with LLM.")
            logging.info(f"In revised_functional_document_from_llm : {response.content}")
            return response.content
        except Exception as e:
            logging.error(f"Error revising functional document: {str(e)}")
            raise CustomException(e, sys)

    def generate_technical_document_from_llm(self, functional_document, user_stories):
        try:
            logging.info("Generating technical document with LLM...")
            # Summarize functional document to reduce token usage (keep only key sections)
            # Extract key sections: functional requirements, data requirements, NFRs
            import re
            func_summary = ""
            if functional_document:
                # Extract main sections (1-12) headings and first paragraph of each
                sections = re.findall(r'\*\*(\d+\.\s+[^*]+)\*\*', functional_document)
                func_summary = f"Functional document covers: {', '.join(sections[:5])}. "
                # Extract functional requirements section if present
                fr_match = re.search(r'\*\*4\.\s+SPECIFIC FUNCTIONAL REQUIREMENTS\*\*([^*]+)', functional_document, re.DOTALL)
                if fr_match:
                    fr_text = fr_match.group(1)[:500]  # First 500 chars
                    func_summary += f"Key functional requirements: {fr_text}..."
            
            # Truncate user_stories if too long
            user_stories_str = str(user_stories)
            if len(user_stories_str) > 1500:
                user_stories_str = user_stories_str[:1500] + "... (truncated)"
            
            user_query = f"Create a comprehensive Technical Design Document based on these user stories: {user_stories_str}. "
            if func_summary:
                user_query += f"Reference this functional document summary: {func_summary}"
            
            chain = prompt_template | self.llm 
            response = chain.invoke({"system_prompt" : technical_document_system_prompt, "human_query" : user_query})
            logging.info("Technical document generated with LLM.")
            logging.info(f"In generate_technical_document_from_llm : {response.content}")
            return response.content
        except Exception as e:
            logging.error(f"Error generating technical document: {str(e)}")
            raise CustomException(e, sys)

    def revised_technical_document_from_llm(self, technical_document, user_feedback):
        try:
            logging.info("Revising technical document with LLM...")
            user_query = f"""EXISTING TECHNICAL DOCUMENT (PRESERVE ALL CONTENT NOT MENTIONED IN FEEDBACK):
{technical_document}

USER FEEDBACK (APPLY ONLY THESE CHANGES):
{user_feedback}

INSTRUCTIONS:
- Keep ALL existing sections, paragraphs, diagrams, tables, and content that are NOT mentioned in the feedback
- Only modify the specific parts requested in the user feedback
- Return the complete document with all preserved content and incremental changes applied"""
            chain = prompt_template | self.llm 
            response = chain.invoke({"system_prompt" : revised_technical_document_system_prompt, "human_query" : user_query})
            logging.info("Technical document revised with LLM.")
            logging.info(f"In revised_technical_document_from_llm : {response.content}")
            return response.content
        except Exception as e:
            logging.error(f"Error revising technical document: {str(e)}")
            raise CustomException(e, sys)
