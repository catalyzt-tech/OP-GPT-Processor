from crewai import Agent
from langchain.agents import Tool
from langchain_openai import ChatOpenAI
import os
from citation import Citation
from crewai_tools import BaseTool

os.environ["GROQ_API_KEY"] = os.getenv("groq_api")


class InfoSearchTool(BaseTool):
    name: str = "Info Search Tool"
    description: str = "Search data related information."

    def _run(self, query: str) -> str:
        # Retrieve relevant documents based on the query
        cite = Citation()
        documents = cite.vector_store
        return documents.invoke(query)
        # Return the content of the retrieved documents


# Initialize the search tool with the specified directory and model configuration


class ResearchCrewAgents:

    def __init__(self):
        # Initialize the LLM to be used by the agents
        self.cite = Citation()
        # SELECT YOUR MODEL HERE
        self.selected_llm = self.cite.llm

    def researcher(self):
        # Setup the tool for the Researcher agent
        tools = [InfoSearchTool()]
        return Agent(
            role="Research and Verification Agent",
            goal="Search through the data to find relevant and accurate answers.",
            backstory=(
                "You are an assistant for question-answering tasks. "
                "Use the information present in the retrieved context to answer the question. "
                "Provide a clear, concise, and factually accurate answer. "
                "Verify the information and avoid any hallucinations or unsupported claims. "
                "If you don't know the answer, say 'I don't know'."
            ),
            verbose=True,
            allow_delegation=False,
            llm=self.selected_llm,
            tools=tools,  # Correctly pass the tools list
            max_iter=3,
        )

    def writer(self):
        # Setup the Writer agent
        return Agent(
            role="Content Writer",
            goal="Write engaging content based on the provided research or information.",
            backstory=(
                "You are a skilled writer who excels at turning raw data into captivating narratives."
                "Your task is to write clear, structured, and engaging content."
            ),
            verbose=True,
            allow_delegation=False,
            llm=self.selected_llm,
            max_iter=2,
        )

    def conclusion(self):
        # Setup the Conclusion agent
        return Agent(
            role="Conclusion Agent",
            goal="Generate a concise summary of the results from the previous tasks.",
            backstory=(
                "You are responsible for summarizing the key points and takeaways from the research and writing tasks. "
                "Your summary should be concise, informative, and capture the essence of the content."
            ),
            verbose=True,
            allow_delegation=False,
            llm=self.selected_llm,
            max_iter=2,
        )
