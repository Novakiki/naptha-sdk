import pytest
import structlog
from unittest.mock import AsyncMock, patch
from naptha_sdk.client.naptha import Naptha

logger = structlog.get_logger(__name__)

@pytest.fixture
async def naptha():
    """Provide test Naptha client with mocked connections."""
    logger.info("initializing_test_client")
    
    # Create mock for SurrealDB connection
    mock_surrealdb = AsyncMock()
    mock_surrealdb.connect = AsyncMock()
    
    with patch('naptha_sdk.client.hub.SurrealDB') as mock_db:
        mock_db.return_value = mock_surrealdb
        
        client = Naptha()
        client.node_url = "http://localhost:7001"
        client.hub.url = "ws://localhost:3001/rpc"
        client.hub.username = "test_user"
        client.hub.password = "test_pass"
        
        logger.info("client_configured",
                   node_url=client.node_url,
                   hub_url=client.hub.url)
        
        async with client as c:
            logger.info("client_ready")
            return c 