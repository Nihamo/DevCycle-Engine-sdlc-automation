from src.sdlccopilot.graph.sdlc_graph import SDLCGraphBuilder
from IPython.display import Image, display
from langchain_core.messages import HumanMessage
from src.sdlccopilot.logger import logging
import uuid

thread = {"configurable": {"thread_id": str(uuid.uuid4())}}

if __name__ == "__main__":
    logging.info("***** Starting the workflow test *****")
    builder = SDLCGraphBuilder()
    sdlc_workflow = builder.build()
    
    # graph_png = sdlc_workflow.get_graph().draw_mermaid_png()
    # with open("workflow.png", "wb") as f:
    #     f.write(graph_png)
        
    project_title = "PayMate: Your Ultimate Payment Companion"
    project_description = "PayMate is a comprehensive payment application that allows users to perform seamless transactions using the Unified Payments Interface (UPI). Beyond basic payments, PayMate offers features such as quick loans, bill payments, and a user-friendly interface, making it a one-stop solution for all financial needs."
    requirements = ["Implement multi-factor authentication, including biometrics (fingerprint and facial recognition) and MPIN, to secure user accounts.​", "Enable users to link multiple bank accounts and perform instant fund transfers using UPI.", "Provide users with access to instant micro-loans with minimal documentation.", "Allow users to pay utility bills such as electricity, water, gas, and broadband directly through the app."]
    
    project_requirements = {
        "title" : project_title,
        "description" : project_description,
        "requirements" : requirements
    }

    ## 1. User Story Generation
    
    logging.info("** 1. User Story Generation **")
    initial_story_state = {
        "project_requirements" : project_requirements,
        "user_stories": [],
        "user_story_messages": HumanMessage(content=f"{project_requirements}"),
        "user_story_status": "in_progress",
        "revised_count" : 0,
    }
    # Thread
    
    print("Workflow Starting...")

    state = None
    for event in sdlc_workflow.stream(initial_story_state, thread, stream_mode="values"):
        state = event

    print("** User Story Generated Successfully **")
    print(state)
    
    user_feedback = "In above user stories, add a user story for buy insurance from the app and return all the user stories"
    logging.info(f"** User Feedback : {user_feedback} **")
    sdlc_workflow.update_state(thread, { "user_story_messages" : HumanMessage(content=f'{user_feedback}')})

    for event in sdlc_workflow.stream(None, thread, stream_mode="values"):
        state = event
    
    logging.info("** User Feedback Applied Successfully **")

    ## 2. User Story Approval
    logging.info("** Approving User Stories **")
    sdlc_workflow.update_state(thread, { "user_story_messages" : HumanMessage(content='Approved'), "revised_count" : 0})

    for event in sdlc_workflow.stream(None, thread, stream_mode="values"):
        state = event

    current_state = sdlc_workflow.get_state(thread) 
    print("Next Node : ", current_state.next)

    ## 2. Functional Document Review
    user_feedback = "Revised the document to book the flight tickets from the bookMyTrip.com site."
    sdlc_workflow.update_state(thread, { "functional_messages" : HumanMessage(content=f'{user_feedback}')})
    
    for event in sdlc_workflow.stream(None, thread, stream_mode="values"):
        state = event

    current_state = sdlc_workflow.get_state(thread) 
    print("Next Node : ", current_state.next)
    
    ## 3. Function Document Approve
    sdlc_workflow.update_state(thread, { "functional_messages" : HumanMessage(content='Approved'), "revised_count" : 0})
    
    for event in sdlc_workflow.stream(None, thread, stream_mode="values"):
        state = event
    
    ## 4. Technical Document User Feedback
    user_feedback = "Revised the technical document for book the flight tickets from the goibibo.com site."
    sdlc_workflow.update_state(thread, { "technical_messages" : HumanMessage(content=f'{user_feedback}')})
    
    for event in sdlc_workflow.stream(None, thread, stream_mode="values"):
        state = event

    current_state = sdlc_workflow.get_state(thread) 
    print("Next Node : ", current_state.next)
    
    ## 5. Technical Document Approval
    sdlc_workflow.update_state(thread, { "technical_messages" : HumanMessage(content='Approved'), "revised_count" : 0})
    
    for event in sdlc_workflow.stream(None, thread, stream_mode="values"):
        state = event
    
    current_state = sdlc_workflow.get_state(thread) 
    print("Next Node : ", current_state.next)
    
    ## 6. Frontend Code User Feedback - TODO 
    # user_feedback = "Revised the frontend code for buy insurance from the app"
    # sdlc_workflow.update_state(thread, { "frontend_messages" : HumanMessage(content=f'{user_feedback}')})
    
    # for event in sdlc_workflow.stream(None, thread, stream_mode="values"):
    #     state = event
    
    # current_state = sdlc_workflow.get_state(thread) 
    # print("Next Node : ", current_state.next)
    
    ## 7. Frontend Code Approval
    sdlc_workflow.update_state(thread, { "frontend_messages" : HumanMessage(content='Approved'), "revised_count" : 0})
    
    for event in sdlc_workflow.stream(None, thread, stream_mode="values"):
        state = event
    
    current_state = sdlc_workflow.get_state(thread) 
    print("Next Node : ", current_state.next)
    
    ## 8. Backend Code User Feedback - TODO 
    # user_feedback = "Revised the backend code for buy insurance from the app"
    # sdlc_workflow.update_state(thread, { "backend_messages" : HumanMessage(content=f'{user_feedback}')})
    
    # for event in sdlc_workflow.stream(None, thread, stream_mode="values"):
    #     state = event 
    
    ## 9. Backend Code Approval
    sdlc_workflow.update_state(thread, { "backend_messages" : HumanMessage(content='Approved'), "revised_count" : 0})
    
    for event in sdlc_workflow.stream(None, thread, stream_mode="values"):
        state = event
    
    current_state = sdlc_workflow.get_state(thread) 
    print("Next Node : ", current_state.next)
    
    print("updated state : ", state)
    
    ## 10. Security Review - Approved 
    sdlc_workflow.update_state(thread, { "security_reviews_messages" : HumanMessage(content='Approved'), "revised_count" : 0})
    
    for event in sdlc_workflow.stream(None, thread, stream_mode="values"):
        state = event
    
    current_state = sdlc_workflow.get_state(thread) 
    print("Next Node : ", current_state.next)
    
    ## 11. Test Cases Review 
    user_feedback = "Revised the test cases for buy insurance from the app"
    sdlc_workflow.update_state(thread, { "test_cases_messages" : HumanMessage(content=f'{user_feedback}')})
    
    for event in sdlc_workflow.stream(None, thread, stream_mode="values"):
        state = event
        
    ## 12. Test Cases Approval
    sdlc_workflow.update_state(thread, { "test_cases_messages" : HumanMessage(content='Approved'), "revised_count" : 0})
    
    for event in sdlc_workflow.stream(None, thread, stream_mode="values"):
        state = event
    
    current_state = sdlc_workflow.get_state(thread) 
    print("** Next Node : ", current_state.next)
    print("******* updated state ******* : ", state)

    print("Workflow Completed Successfully !!!")
