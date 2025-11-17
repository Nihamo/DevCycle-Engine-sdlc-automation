from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser

json_output_parser = JsonOutputParser()

json_prompt_template = PromptTemplate(
    template="{system_prompt} \n {format_instruction} \n {human_query} \n",
    input_variables= ["system_prompt", "human_query",],
    partial_variables={"format_instruction" : json_output_parser.get_format_instructions()}
)

prompt_template = PromptTemplate(
    template="{system_prompt} \n {human_query} \n",
    input_variables= ["system_prompt", "human_query",],
)

