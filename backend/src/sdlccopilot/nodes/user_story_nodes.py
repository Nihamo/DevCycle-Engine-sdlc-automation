from langchain_core.messages import AIMessage
from src.sdlccopilot.states.sdlc import SDLCState
from src.sdlccopilot.logger import logging
from src.sdlccopilot.helpers.user_story import UserStoryHelper
from typing_extensions import Literal
from src.sdlccopilot.utils.constants import CONSTANT_USER_STORIES, CONSTANT_REVISED_USER_STORIES
import os
import time

class UserStoryNodes:
    def __init__(self, llm): 
        self.user_story_helper = UserStoryHelper(llm)

    def process_project_requirements(self, state : SDLCState) -> SDLCState:
        logging.info("In process_project_requirements...")
        return {
            "user_story_messages" : AIMessage(content="I've received your project requirements. I'll now generate user stories based on these requirements.")
        }
        
    def generate_user_stories(self, state : SDLCState) -> SDLCState:
        logging.info("In generate_user_stories...") 
        project_title = state.project_requirements.title
        project_description = state.project_requirements.description
        requirements = state.project_requirements.requirements
        user_stories = None
        if os.environ.get("PROJECT_ENVIRONMENT") != "development":
            user_stories = self.user_story_helper.generate_user_stories_with_llm(project_title, project_description, requirements);
        else:
            time.sleep(10)
            user_stories = CONSTANT_USER_STORIES
        logging.info("User stories generated successfully !!!")
        return {
            "user_story_status" : 'pending_approval',
            "user_stories" : user_stories,
            "user_story_messages" : AIMessage(
                content = f"Based on your requirements, I've generated {len(user_stories)} user stories. Please review these user stories and provide feedback or type 'Approved' if you're satisfied."
            ),
            "revised_count" : 0
        }

    def review_user_stories(self, state : SDLCState) -> SDLCState:
        logging.info("In review_user_stories...")
        user_review = state.user_story_messages[-1].content
        user_review = user_review.lower().strip()
        logging.info(f"user_feedback : {user_review}")  
        if user_review == "approved":
            logging.info("User stories approved !!!")
            return {
                "user_story_messages" : AIMessage(content="Great! Your user stories have been finalized. You can now proceed with your design process."),
                "user_story_status" : "approved",
            }
        else:
            logging.info("User stories feedback received !!!")
            return {
                "user_story_messages" :  AIMessage(content="I've received your feedback. I'll revise the user stories accordingly."),
                "user_story_status" : "feedback"
            }

    def should_revise_user_stories(self, state : SDLCState) -> Literal["feedback", "approved"]:
        return "approved" if state.user_story_status == "approved" else "feedback"   

    def revised_user_stories(self, state : SDLCState) -> SDLCState:
        logging.info("In revised_user_stories...")
        user_review = state.user_story_messages[-2].content
        user_review = user_review.lower().strip()
        if state.user_story_status == 'feedback':
            revised_count = state.revised_count + 1
            logging.info(f"revised_count : {revised_count}")
            if revised_count == 3:
                logging.info("User stories revision maxed out !!!")
                return {
                    "user_story_messages" :  AIMessage(
                        content = f"User stories have been revision maxed out. Please review the user stories and continue with the next step."
                    ),
                    "user_story_status" : "approved"
                }
            user_stories = None
            if os.environ.get("PROJECT_ENVIRONMENT") != "development":
                user_stories = self.user_story_helper.revised_user_stories_with_llm(state.user_stories, user_review)
            else:
                time.sleep(10)  # Add 10 second wait
                user_stories = CONSTANT_REVISED_USER_STORIES
            
            logging.info("User stories revised successfully !!!")
           
            return {
                    "user_stories" : user_stories,
                    "user_story_messages" : AIMessage(
                        content = "I've revised the user stories based on your feedback.\n\nPlease review these updated user stories and provide additional feedback or type 'Approved' if you're satisfied."),
                    "user_story_status" : "pending_approval",
                    "revised_count" : revised_count
                }