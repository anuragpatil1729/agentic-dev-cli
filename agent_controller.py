import os

from agent_pipeline import AgentPipeline


class AgentController:

    def __init__(self, os_type):

        self.pipeline = AgentPipeline(os_type)

    def handle_prompt(self, prompt):

        return self.pipeline.process_prompt(prompt)