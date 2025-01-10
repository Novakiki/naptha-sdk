import asyncio
from naptha_sdk.client.naptha import Naptha
from naptha_sdk.modules.tool import Tool
from naptha_sdk.schemas import ToolDeployment, ToolRunInput, NodeConfig
from naptha_sdk.user import sign_consumer_id
import os
import pytest
import structlog

logger = structlog.get_logger(__name__)

pytestmark = pytest.mark.asyncio

TEST_KEY = "test_signing_key_123"  # Simple test key

@pytest.fixture(autouse=True)
def setup_test_keys():
    """Set up a simple test key for signing."""
    os.environ["PRIVATE_KEY"] = TEST_KEY
    return TEST_KEY

@pytest.mark.asyncio
async def test_tool(setup_test_keys):
    logger.info("starting_tool_test")
    try:
        naptha = Naptha()
        naptha.user.id = "test_user"

        # Get PRIVATE_KEY
        private_key = os.getenv("PRIVATE_KEY")
        logger.info("env_check", 
                   has_private_key=bool(private_key),
                   env_vars=dict(os.environ))

        tool_deployment = ToolDeployment(
            module={"name": "generate_image_tool"},
            node=NodeConfig(
                ip="localhost",
                http_port=7001,
                server_type="ws",
                ports=[7001],
                id="test_node",
                owner="test_user",
                public_key="test_key",
                servers=[],
                models=[],
                docker_jobs=False
            )
        )
        logger.info("deployment_created", deployment=tool_deployment)

        tool = Tool(tool_deployment)

        input_params = {
            "tool_name": "generate_image_tool",
            "tool_input_data": "A beautiful image of a cat"
        }

        tool_run_input = ToolRunInput(
            consumer_id=naptha.user.id,
            inputs=input_params,
            deployment=tool_deployment,
            signature=sign_consumer_id(naptha.user.id, os.getenv("PRIVATE_KEY"))
        )

        response = await tool.call_tool_func(tool_run_input)

        print(response)

    except Exception as e:
        logger.error("tool_test_error", error=str(e))
        raise

if __name__ == "__main__":
    asyncio.run(test_tool())