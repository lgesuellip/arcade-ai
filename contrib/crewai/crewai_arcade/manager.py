from typing import Any, Callable

from arcadepy import Arcade
from arcadepy.types.shared import ToolDefinition
from common_arcade.exceptions import ToolExecutionError
from common_arcade.manager import BaseArcadeManager
from common_arcade.utils import tool_definition_to_pydantic_model

from crewai_arcade.structured import StructuredTool


class CrewAIToolManager(BaseArcadeManager):
    """CrewAI-specific implementation of the BaseArcadeManager.

    This manager requires a user_id during initialization as it's needed for tool authorization.
    """

    def __init__(
        self,
        client: Arcade,
        user_id: str,
        **kwargs: Any,
    ) -> None:
        """Initialize the CrewAIToolManager.

        Args:
            client: Arcade client instance.
            user_id: User ID required for tool authorization.
            **kwargs: Additional keyword arguments.

        Raises:
            ValueError: If user_id is empty or None.
        """
        if not user_id:
            raise ValueError("user_id is required for CrewAIToolManager")
        super().__init__(client=client, user_id=user_id, **kwargs)

    def create_tool_function(self, tool_name: str, **kwargs: Any) -> Callable[..., Any]:
        """Creates a function wrapper for an Arcade tool.

        Args:
            tool_name: The name of the tool to create a function for.
            **kwargs: Additional keyword arguments for tool configuration.

        Returns:
            A callable function that executes the tool.
        """

        def tool_function(*args: Any, **kwargs: Any) -> Any:
            # Handle authorization if required
            if self.requires_auth(tool_name):
                # Get authorization status
                auth_response = self.authorize(tool_name, self.user_id)  # type: ignore[arg-type]
                if not auth_response.authorization_id:
                    return ToolExecutionError(
                        f"Authorization failed for {tool_name}: No authorization ID received"
                    )
                # Wait for authorization completion with timeout
                auth_response = self.wait_for_completion(
                    auth_response,
                )

                if auth_response.status != "completed":
                    return ToolExecutionError(
                        f"Authorization failed for {tool_name}. "
                        f"URL: {auth_response.authorization_url}"
                    )

            # Tool execution
            response = self.client.tools.execute(
                tool_name=tool_name,
                inputs=kwargs,
                user_id=self.user_id,  # type: ignore[arg-type]
            )
            if response.success:
                if response.output is None:
                    return ToolExecutionError(f"No output received from {tool_name}")
                return response.output.value

            error_msg = (
                response.output.error.message
                if response.output and response.output.error
                else f"Execution failed for {tool_name}"
            )
            return ToolExecutionError(error_msg)

        return tool_function

    def wrap_tool(self, name: str, tool_def: ToolDefinition, **kwargs: Any) -> Any:
        """Wrap a tool as a CrewAI StructuredTool.

        Args:
            name: The name of the tool to wrap.
            tool_def: The definition of the tool to wrap.
            **kwargs: Additional keyword arguments for tool configuration.

        Returns:
            A StructuredTool instance.
        """
        description = tool_def.description or "No description provided."
        args_schema = tool_definition_to_pydantic_model(tool_def)
        tool_function = self.create_tool_function(name, **kwargs)

        return StructuredTool.from_function(
            func=tool_function,
            name=name,
            description=description,
            args_schema=args_schema,
        )
