import asyncio
import logging
from pydantic import BaseModel, Field
from fastmcp import FastMCP
from fastmcp.contrib.mcp_mixin.mcp_mixin import MCPMixin, mcp_tool
from fastmcp.utilities.logging import get_logger, configure_logging
from uuid import uuid4

mcp = FastMCP()

configure_logging(level=logging.INFO)

logger = get_logger(__name__)

class Memory(BaseModel):
    id: str = Field(description="The id of the memory.", default_factory=lambda: str(uuid4()))
    topic: str = Field(description="The topic of the memory.", examples=[
        "Elasticsearch",
        "Git",
        "Python",
        "FastAPI",
        "FastMCP",
        "Planning",
        "Responses to the user",
    ])
    memory: str = Field(description="The memory to add to the memory bank.", examples=[
        "I learned that a tool called `X` is not particularly useful for a task where i need to do `Y`.",
        "I learned that calling tool X as the first step in a task related to Y helped me complete the task more quickly.",
    ])
    context: str = Field(description="The context of the memory.", examples=[
        "I was working on a project that involved using Elasticsearch to search for documents.",
        "I was working on a project that involved using Git to manage the codebase.",
        "I was working on a project that involved using Python to build a web application.",
        "I was working on a project that involved using FastAPI to build a web application.",
        "I was working on a project that involved using FastMCP to build a web application.",
    ])

class MemoryBank(MCPMixin):
    memories: list[Memory]

    def __init__(self):
        self.memories = []

    def get_memory_bank_info(self) -> str:
        """
        Get information about the memory bank. Useful when you first start a conversation with the user so you can recall what you've learned in the past.
        """
        return f"The memory bank has {len(self.memories)} memories."

    @mcp_tool()
    def add_memory(self, memory: Memory):
        """
        Add a memory to the memory bank. Useful when you've learned a valuable lesson or piece of information that you want to recall later.
        """
        self.memories.append(memory)
        logger.info(f"Added memory: {memory}")

    @mcp_tool()
    def add_memories(self, memories: list[Memory]):
        """
        Add multiple memories to the memory bank. Useful when you've learned a valuable lesson or piece of information that you want to recall later.
        """
        self.memories.extend(memories)
        logger.info(f"Added {len(memories)} memories")

    @mcp_tool()
    def search_memories(self, query: str) -> list[Memory]:
        """
        Search the memory bank for memories that match the query. Useful when you want to recall a memory that you've learned in the past.
        """
        logger.info(f"Searching for memories with query: {query}")
        return [memory for memory in self.memories if query in memory.memory]

    @mcp_tool()
    def get_memories(self) -> list[Memory]:
        """
        Get all memories from the memory bank. Useful when you first start a conversation with the user so you can recall what you've learned in the past.
        """
        logger.info(f"Getting all memories: {self.memories}")
        return self.memories

    @mcp_tool()
    def delete_memory(self, id: str):
        """
        Delete a memory from the memory bank. Useful when you've learned a valuable lesson or piece of information that you want to recall later.
        """
        self.memories = [memory for memory in self.memories if memory.id != id]
        logger.info(f"Deleted memory with id: {id}")


async def main():
    fastmcp = FastMCP()

    logger.info("Creating memory bank")
    memory_bank = MemoryBank()

    memory_bank.register_all(mcp_server=fastmcp)

    logger.info("Starting FastMCP server")
    await fastmcp.run_async(transport="sse")


if __name__ == "__main__":
    asyncio.run(main())
