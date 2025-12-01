from src.sdlccopilot.prompts.prompt_template import prompt_template
from src.sdlccopilot.prompts.document import functional_document_system_prompt, revised_functional_document_system_prompt, technical_document_system_prompt, revised_technical_document_system_prompt
from src.sdlccopilot.logger import logging
from src.sdlccopilot.exception import CustomException
import sys
import re

class DocumentHelper:
    def __init__(self, llm):
        self.llm = llm
    
    def _estimate_tokens(self, text):
        """Rough token estimation: ~1 token per 4 characters for English text"""
        return len(text) // 4
    
    def _condense_technical_document(self, technical_document, user_feedback, max_tokens=4000):
        """
        Condense technical document to fit within token limits.
        Preserves structure and relevant sections based on feedback.
        """
        # Estimate current tokens
        doc_tokens = self._estimate_tokens(technical_document)
        feedback_tokens = self._estimate_tokens(user_feedback)
        system_prompt_tokens = 1000  # Rough estimate for system prompt
        
        total_estimated = doc_tokens + feedback_tokens + system_prompt_tokens
        
        # If within limits, return as-is
        if total_estimated <= max_tokens:
            return technical_document
        
        logging.info(f"Document too large ({total_estimated} tokens), condensing to fit within {max_tokens} tokens")
        
        # Extract document structure (section headings)
        sections = []
        # Match markdown headings (both # and ** formats)
        heading_pattern = r'^(#{1,6}\s+.+?$|\*\*\d+\.\s+[^*]+\*\*)'
        
        lines = technical_document.split('\n')
        current_section = None
        current_content = []
        
        for line in lines:
            # Check if line is a heading
            if re.match(heading_pattern, line.strip()):
                # Save previous section
                if current_section:
                    sections.append({
                        'heading': current_section,
                        'content': '\n'.join(current_content)
                    })
                # Start new section
                current_section = line.strip()
                current_content = []
            else:
                if current_section:
                    current_content.append(line)
        
        # Add last section
        if current_section:
            sections.append({
                'heading': current_section,
                'content': '\n'.join(current_content)
            })
        
        # If no sections found, use simple truncation
        if not sections:
            # Truncate document to fit
            max_doc_chars = (max_tokens - feedback_tokens - system_prompt_tokens) * 4
            if len(technical_document) > max_doc_chars:
                logging.warning("Could not parse sections, using simple truncation")
                return technical_document[:max_doc_chars] + "\n\n[Document truncated due to size limits. Please note that the full document structure is preserved in the original.]"
            return technical_document
        
        # Identify relevant sections based on feedback keywords
        feedback_lower = user_feedback.lower()
        relevant_keywords = []
        section_keywords = {
            'architecture': ['architecture', 'system design', 'overview', 'diagram'],
            'technology': ['technology', 'stack', 'framework', 'library', 'tool'],
            'module': ['module', 'component', 'service', 'function'],
            'database': ['database', 'schema', 'table', 'entity', 'er diagram'],
            'api': ['api', 'endpoint', 'request', 'response', 'rest'],
            'security': ['security', 'authentication', 'authorization', 'encryption'],
            'performance': ['performance', 'scalability', 'caching', 'load'],
            'error': ['error', 'exception', 'handling', 'logging'],
            'deployment': ['deployment', 'ci/cd', 'docker', 'infrastructure'],
            'risk': ['risk', 'mitigation', 'constraint', 'assumption']
        }
        
        for keyword, terms in section_keywords.items():
            if any(term in feedback_lower for term in terms):
                relevant_keywords.append(keyword)
        
        # Build condensed document - always include all section headings
        condensed_parts = []
        tokens_used = feedback_tokens + system_prompt_tokens
        
        # First, calculate how much space we have for content
        # Reserve tokens for all headings (essential structure)
        all_headings_text = '\n'.join([s['heading'] for s in sections])
        headings_tokens = self._estimate_tokens(all_headings_text)
        available_tokens = max_tokens - tokens_used - headings_tokens - 500  # Reserve 500 for notes/formatting
        
        # Distribute available tokens among sections, prioritizing relevant ones
        section_priorities = []
        for i, section in enumerate(sections):
            heading_lower = section['heading'].lower()
            is_relevant = any(kw in heading_lower for kw in relevant_keywords) if relevant_keywords else False
            section_priorities.append({
                'index': i,
                'section': section,
                'is_relevant': is_relevant,
                'content_length': len(section['content'])
            })
        
        # Sort by relevance, then by size (smaller first to fit more)
        section_priorities.sort(key=lambda x: (not x['is_relevant'], x['content_length']))
        
        # Allocate tokens to sections
        allocated_tokens = {}
        remaining_tokens = available_tokens
        
        for priority in section_priorities:
            section = priority['section']
            section_full_tokens = self._estimate_tokens(section['content'])
            
            if priority['is_relevant']:
                # Relevant sections get more tokens, up to their full size
                allocated = min(section_full_tokens, remaining_tokens // 2 if remaining_tokens > 1000 else remaining_tokens)
            else:
                # Non-relevant sections get minimal tokens (just enough for structure)
                allocated = min(200, remaining_tokens // len(sections))
            
            allocated_tokens[priority['index']] = allocated
            remaining_tokens -= allocated
        
        # Build condensed document with allocated tokens
        for i, section in enumerate(sections):
            heading = section['heading']
            content = section['content']
            allocated = allocated_tokens.get(i, 200)
            
            # Estimate how much content we can include
            content_tokens = self._estimate_tokens(content)
            
            if content_tokens <= allocated:
                # Include full content
                condensed_parts.append(f"{heading}\n{content}")
            else:
                # Include heading and truncated content
                # Convert tokens back to characters (rough estimate)
                max_chars = allocated * 4
                if max_chars > 0:
                    truncated_content = content[:max_chars]
                    # Try to end at a sentence or paragraph boundary
                    last_period = truncated_content.rfind('.')
                    last_newline = truncated_content.rfind('\n')
                    cut_point = max(last_period, last_newline)
                    if cut_point > max_chars * 0.7:  # If we can find a good break point
                        truncated_content = truncated_content[:cut_point + 1]
                    else:
                        truncated_content = truncated_content[:max_chars]
                    condensed_parts.append(f"{heading}\n{truncated_content}...")
                else:
                    # Just include heading
                    condensed_parts.append(heading)
        
        condensed_doc = '\n\n'.join(condensed_parts)
        
        # Add note about condensation with document structure
        structure_note = f"\n\n[IMPORTANT NOTE: This document has been condensed to fit token limits. The original document contains {len(sections)} sections with the following structure:\n"
        structure_note += '\n'.join([f"- {s['heading']}" for s in sections])
        structure_note += "\n\nYou MUST preserve ALL sections from the original document in your response, maintaining the exact same structure, order, and numbering. For sections that appear condensed above, preserve their original content structure and apply only the changes requested in the feedback. Return the COMPLETE document with all sections.]"
        condensed_doc += structure_note
        
        logging.info(f"Condensed document from {doc_tokens} to {self._estimate_tokens(condensed_doc)} tokens")
        return condensed_doc

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
            user_query = f"""EXISTING FUNCTIONAL DOCUMENT (PRESERVE ALL CONTENT, STRUCTURE, AND ORDER):
{functional_document}

USER FEEDBACK (APPLY ONLY THESE CHANGES):
{user_feedback}

CRITICAL INSTRUCTIONS:
- Keep ALL existing sections, paragraphs, and content that are NOT mentioned in the feedback
- MAINTAIN THE EXACT SAME SECTION ORDER and numbering as in the original document above
- DO NOT reorganize, reorder, or restructure any sections
- Only modify the specific parts requested in the user feedback
- If adding new content, add it within the relevant existing section or at the end of that section
- If adding a completely new section, add it at the end of the document
- Return the complete document with the exact same structure, order, and numbering, with only the requested changes applied"""
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
            
            # Handle "approved" feedback - no revision needed, return original
            feedback_lower = user_feedback.lower().strip()
            if feedback_lower == "approved" or feedback_lower == "approve":
                logging.info("Feedback is 'approved', returning original document without revision")
                return technical_document
            
            # Condense document if needed to fit token limits (Groq limit is 6000, use 3500 as safe margin)
            # Use a more conservative limit to account for system prompt and response overhead
            condensed_document = self._condense_technical_document(technical_document, user_feedback, max_tokens=3500)
            
            # Double-check token estimation before sending
            # System prompt is typically ~1000-1500 tokens, use 1500 as estimate
            final_estimate = (self._estimate_tokens(condensed_document) + 
                            self._estimate_tokens(user_feedback) + 
                            1500 +  # System prompt estimate
                            500)  # Buffer for formatting
            
            if final_estimate > 5500:  # Still too large, use more aggressive truncation
                logging.warning(f"Document still too large after condensation ({final_estimate} tokens), using aggressive truncation")
                # Simple character-based truncation as last resort
                max_chars = 12000  # Roughly 3000 tokens
                if len(condensed_document) > max_chars:
                    condensed_document = condensed_document[:max_chars] + "\n\n[Document truncated - preserving structure only]"
            
            user_query = f"""EXISTING TECHNICAL DOCUMENT (PRESERVE ALL CONTENT, STRUCTURE, AND ORDER):
{condensed_document}

USER FEEDBACK (APPLY ONLY THESE CHANGES):
{user_feedback}

CRITICAL INSTRUCTIONS:
- Keep ALL existing sections, paragraphs, diagrams, tables, and content that are NOT mentioned in the feedback
- MAINTAIN THE EXACT SAME SECTION ORDER and numbering as in the original document above
- DO NOT reorganize, reorder, or restructure any sections
- Only modify the specific parts requested in the user feedback
- If adding new content, add it within the relevant existing section or at the end of that section
- If adding a completely new section, add it at the end of the document
- Return the complete document with the exact same structure, order, and numbering, with only the requested changes applied
- IMPORTANT: If the document above appears condensed, you must still return the FULL original document structure with all sections, applying only the changes requested in the feedback"""
            chain = prompt_template | self.llm
            response = chain.invoke({"system_prompt" : revised_technical_document_system_prompt, "human_query" : user_query})
            logging.info("Technical document revised with LLM.")
            logging.info(f"In revised_technical_document_from_llm : {response.content}")
            return response.content
        except Exception as e:
            error_str = str(e)
            # Check if it's a token limit error
            if "413" in error_str or "rate_limit_exceeded" in error_str or "too large" in error_str.lower():
                logging.error(f"Token limit exceeded: {error_str}")
                # Try one more time with even more aggressive truncation
                logging.info("Retrying with more aggressive document truncation...")
                try:
                    # Extract just the structure and minimal content
                    max_chars = 8000  # Very aggressive - roughly 2000 tokens
                    ultra_condensed = technical_document[:max_chars] if len(technical_document) > max_chars else technical_document
                    ultra_condensed += f"\n\n[NOTE: Document truncated due to size. Original document has {len(technical_document)} characters. Preserve all section structure and apply only the requested changes: {user_feedback}]"
                    
                    user_query = f"""EXISTING TECHNICAL DOCUMENT (PRESERVE ALL CONTENT, STRUCTURE, AND ORDER):
{ultra_condensed}

USER FEEDBACK (APPLY ONLY THESE CHANGES):
{user_feedback}

CRITICAL INSTRUCTIONS:
- Keep ALL existing sections, paragraphs, diagrams, tables, and content that are NOT mentioned in the feedback
- MAINTAIN THE EXACT SAME SECTION ORDER and numbering as in the original document above
- Return the complete document with the exact same structure, order, and numbering, with only the requested changes applied"""
                    retry_chain = prompt_template | self.llm
                    response = retry_chain.invoke({"system_prompt" : revised_technical_document_system_prompt, "human_query" : user_query})
                    logging.info("Technical document revised with LLM after retry.")
                    return response.content
                except Exception as retry_error:
                    logging.error(f"Retry also failed: {str(retry_error)}")
                    raise CustomException(f"Document too large for LLM processing. Original error: {error_str}", sys)
            else:
                logging.error(f"Error revising technical document: {error_str}")
                raise CustomException(e, sys)
