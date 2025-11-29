from src.sdlccopilot.prompts.prompt_template import prompt_template
from src.sdlccopilot.prompts.code import CODE_SYSTEM_PROMPT, FRONTEND_PROMPT, BACKEND_PROMPT
from src.sdlccopilot.logger import logging
from src.sdlccopilot.exception import CustomException
import sys

class CodeHelper:
    def __init__(self, llm):
        self.llm = llm
    
    def generate_frontend_code_from_llm(self, user_stories, functional_document=None, technical_document=None):
        try:
            logging.info("Generating frontend code with LLM...")
            
            # Build comprehensive context
            context_parts = [f"User Stories: {user_stories}"]
            
            if functional_document:
                # Include key sections from functional document
                func_summary = functional_document[:2000] if len(functional_document) > 2000 else functional_document
                context_parts.append(f"Functional Requirements: {func_summary}")
            
            if technical_document:
                # Include frontend-relevant sections from technical document
                tech_summary = technical_document[:2000] if len(technical_document) > 2000 else technical_document
                context_parts.append(f"Technical Design (Frontend): {tech_summary}")
            
            context = "\n\n".join(context_parts)
            user_query = f"Analyze the following project requirements and generate a professional, production-ready frontend React + Vite + TypeScript application:\n\n{context}\n\n{FRONTEND_PROMPT}"
            
            chain = prompt_template | self.llm 
            response = chain.invoke({"system_prompt" : CODE_SYSTEM_PROMPT, "human_query" : user_query})
            logging.info("Frontend code generated with LLM.")
            logging.info(f"In generate_frontend_code_from_llm : {response.content}")
            return response.content
        except Exception as e:
            logging.error(f"Error generating frontend code: {str(e)}")
            raise CustomException(e, sys)

    def revised_frontend_code_from_llm(self, code, user_feedback):
        try:
            logging.info("Revising frontend code with LLM...")
            user_query = f"""EXISTING FRONTEND CODE (PRESERVE ALL CODE NOT MENTIONED IN FEEDBACK):
{code}

USER FEEDBACK (APPLY ONLY THESE CHANGES):
{user_feedback}

INSTRUCTIONS:
- Keep ALL existing files, components, functions, and code that are NOT mentioned in the feedback
- Only modify the specific parts requested in the user feedback
- Return the complete codebase with all preserved code and incremental changes applied
- Maintain code structure, imports, and dependencies unless explicitly changed

{FRONTEND_PROMPT}"""
            chain = prompt_template | self.llm 
            response = chain.invoke({"system_prompt" : CODE_SYSTEM_PROMPT, "human_query" : user_query})
            logging.info("Frontend code revised with LLM.")
            logging.info(f"In revised_frontend_code_from_llm : {response.content}")
            return response.content
        except Exception as e:
            logging.error(f"Error revising frontend code: {str(e)}")
            raise CustomException(e, sys)
    
    def generate_backend_code_from_llm(self, user_stories, functional_document=None, technical_document=None):
        try:
            logging.info("Generating backend code with LLM...")
            
            # Build comprehensive context
            context_parts = [f"User Stories: {user_stories}"]
            
            if functional_document:
                # Include key sections from functional document
                func_summary = functional_document[:2000] if len(functional_document) > 2000 else functional_document
                context_parts.append(f"Functional Requirements: {func_summary}")
            
            if technical_document:
                # Include backend-relevant sections from technical document
                tech_summary = technical_document[:3000] if len(technical_document) > 3000 else technical_document
                context_parts.append(f"Technical Design (Backend): {tech_summary}")
            
            context = "\n\n".join(context_parts)
            user_query = f"Analyze the following project requirements and generate a professional, production-ready backend application (Node.js/Express or Python/FastAPI):\n\n{context}\n\n{BACKEND_PROMPT}"
            
            chain = prompt_template | self.llm 
            response = chain.invoke({"system_prompt" : CODE_SYSTEM_PROMPT, "human_query" : user_query})
            logging.info("Backend code generated with LLM.")
            logging.info(f"In generate_backend_code_from_llm : {response.content}")
            return response.content
        except Exception as e:
            logging.error(f"Error generating backend code: {str(e)}")
            raise CustomException(e, sys)
    
    def revised_backend_code_from_llm(self, code, user_feedback):
        try:
            logging.info("Revising backend code with LLM...")
            user_query = f"""EXISTING BACKEND CODE (PRESERVE ALL CODE NOT MENTIONED IN FEEDBACK):
{code}

USER FEEDBACK (APPLY ONLY THESE CHANGES):
{user_feedback}

INSTRUCTIONS:
- Keep ALL existing files, modules, functions, and code that are NOT mentioned in the feedback
- Only modify the specific parts requested in the user feedback
- Return the complete codebase with all preserved code and incremental changes applied
- Maintain code structure, imports, and dependencies unless explicitly changed

{BACKEND_PROMPT}"""
            chain = prompt_template | self.llm 
            response = chain.invoke({"system_prompt" : CODE_SYSTEM_PROMPT, "human_query" : user_query})
            logging.info("Backend code revised with LLM.")
            logging.info(f"In revised_backend_code_from_llm : {response.content}")
            return response.content
        except Exception as e:
            logging.error(f"Error revising backend code: {str(e)}")
            raise CustomException(e, sys)


