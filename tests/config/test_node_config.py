import pytest
from naptha_sdk.schemas import NodeConfigUser, NodeConfig
import structlog

logger = structlog.get_logger(__name__)

def test_node_config_schema():
    """Test both NodeConfig and NodeConfigUser schemas."""
    logger.info("checking_schemas")
    
    # Test NodeConfig
    config = NodeConfig(
        ip="localhost",
        http_port=7001,
        server_type="http",
        ports=[7001],
        id="test_node",
        owner="test_user",
        public_key="test_key",
        servers=[],
        models=[],
        docker_jobs=False
    )
    logger.info("node_config_instance", config=config.model_dump())
    
    # Test NodeConfigUser
    user_config = NodeConfigUser(
        ip="localhost",
        http_port=7001,
        server_type="http"
    )
    logger.info("node_config_user_instance", config=user_config.model_dump()) 