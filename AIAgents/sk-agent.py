import asyncio
from typing import Annotated
import os
from pathlib import Path
from azure.identity import DefaultAzureCredential
from semantic_kernel.agents import AzureAIAgent, AzureAIAgentSettings
from semantic_kernel.contents import ChatMessageContent, FunctionCallContent, FunctionResultContent, AuthorRole
from semantic_kernel.functions import kernel_function
from dotenv import load_dotenv
# Load environment variables from .env file
env_path = Path(__file__).resolve().parent.parent / "variables.env"
load_dotenv(dotenv_path=env_path)
azure_openai_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
azure_openai_api_key = os.getenv("AZURE_OPENAI_API_KEY")
gpt_deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
gpt_deployment_version = os.getenv("AZURE_OPENAI_DEPLOYMENT_VERSION")
azure_ai_project_endpoint = os.getenv("AZURE_AI_PROJECT_ENDPOINT")
azure_search_endpoint = os.getenv("AZURE_SEARCH_ENDPOINT")
azure_search_key = os.getenv("AZURE_SEARCH_KEY")




class MenuPlugin:
    """A sample Menu Plugin used for the concept sample."""
    @kernel_function(description="Provides a list of specials from the menu.")
    def get_specials(self) -> Annotated[str, "Returns the specials from the menu."]:
        return """
        Special Soup: Clam Chowder
        Special Salad: Cobb Salad
        Special Drink: Chai Tea
        """
    @kernel_function(description="Provides the price of the requested menu item.")
    def get_item_price(
        self, menu_item: Annotated[str, "The name of the menu item."]
    ) -> Annotated[str, "Returns the price of the menu item."]:
        return "$9.99"



async def main():
    ai_agent_settings = AzureAIAgentSettings(
        model_deployment_name=gpt_deployment, 
        endpoint=azure_openai_endpoint,  
        api_version= gpt_deployment_version
    )
    creds = DefaultAzureCredential()
    async with AzureAIAgent.create_client(
            credential=creds,
            conn_str=azure_ai_project_endpoint,
        ) as client:
        # Create agent definition
        agent_definition = await client.agents.create_agent(
            model=ai_agent_settings.model_deployment_name,
            name="restaurant-agent",
            instructions="A restaurant agent that provides menu information.",
        )

        # Create the AzureAI Agent
        agent = AzureAIAgent(
            client=client,
            definition=agent_definition,
            plugins=[MenuPlugin()],
        )
        user_inputs = [
            "Hello", 
            "What is the special soup?", 
            "What is the special drink?", 
            "How much is that?", 
            "Thank you",
        ]
        thread = None
        # Generate the agent response(s)
        for user_input in user_inputs:
            print(f"# {AuthorRole.USER}: '{user_input}'")
            async for response in agent.invoke(
                messages=user_input,
                thread=thread,
            ):
                thread = response.thread
                print(f"# {response.name}: {response.content}")

        # Delete the thread when it is no longer needed
        await thread.delete() if thread else None


if __name__ == "__main__":
    asyncio.run(main())