

# from src.sdlccopilot.graph.user_story_graph import UserStoryGraphBuilder
# from langchain_core.messages import HumanMessage


# class UserStoryWorkflow:
#     def __init__(self):
#         self.user_story_graph_builder = UserStoryGraphBuilder()
#         self.user_story_workflow = self.user_story_graph_builder.build()

#     def compile(self):
#         return self.user_story_workflow
    
#     def run(self, project_requirements: str):
#         initial_state = {
#             "project_requirements" : project_requirements,
#             "user_stories_messages": HumanMessage(content=f"{project_requirements}"),
#             "user_stories": [],
#             "status": "in_progress",
#             "owner_feedback": "",
#             "revised_count" : 0
#         }   

#         # Thread
#         thread = {"configurable": {"thread_id": "10"}}

#         # print(self.user_  
#         # story_workflow.get_graph())
#         # print(self.user_story_workflow.get_graph().get_graph_image())

#         # Stream the workflow

#         user
#         for event in self.user_story_workflow.stream(initial_state, thread, stream_mode="values"):
#             print(event)

#         user_state = self.user_story_workflow.get_state(thread) 
#         print("next node to call : ", user_state.next)
#         print("user_state : ", user_state)

# # if __name__ == "__main__":
# #     user_story_workflow = UserStoryWorkflow()
#     # user_story_workflow.run("A snake and ladder game in web-app")


