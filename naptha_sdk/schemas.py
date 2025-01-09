from enum import Enum
from typing import Dict, List, Optional, Union, Any
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict
from naptha_sdk.storage.schemas import StorageType

class User(BaseModel):
    id: str

class NodeServer(BaseModel):
    server_type: str
    port: int
    node_id: str

class NodeConfig(BaseModel):
    model_config = ConfigDict(
        arbitrary_types_allowed=True
    )
    id: str
    owner: str
    public_key: str
    ip: str
    http_port: int
    server_type: str
    servers: List[str]
    models: List[str]
    docker_jobs: bool
    ports: List[int]

class NodeConfigUser(BaseModel):
    ip: str
    http_port: Optional[int] = None
    server_type: Optional[str] = None

class LLMClientType(str, Enum):
    OPENAI = "openai"
    AZURE_OPENAI = "azure_openai"
    ANTHROPIC = "anthropic"
    VLLM = "vllm"
    LITELLM = "litellm"
    OLLAMA = "ollama"
    STABILITY = "stability"

class LLMConfig(BaseModel):
    config_name: Optional[str] = "llm_config"
    client: Optional[LLMClientType] = None
    model: Optional[str] = None
    max_tokens: Optional[int] = None
    temperature: Optional[float] = None
    api_base: Optional[str] = None

class AgentModuleType(str, Enum):
    package = "package"
    docker = "docker"

class AgentConfig(BaseModel):
    config_name: Optional[str] = "agent_config"
    llm_config: Optional[LLMConfig] = None
    persona_module: Optional[Union[Dict, BaseModel]] = None
    system_prompt: Optional[Union[Dict, BaseModel]] = None

class ToolConfig(BaseModel):
    config_name: Optional[str] = None
    llm_config: Optional[LLMConfig] = None

class OrchestratorConfig(BaseModel):
    config_name: Optional[str] = "orchestrator_config"
    max_rounds: Optional[int] = 5

class EnvironmentConfig(BaseModel):
    config_name: Optional[str] = "environment_config"
    environment_type: Optional[str] = None

class KBConfig(BaseModel):
    model_config = ConfigDict(
        arbitrary_types_allowed=True
    )
    config_name: Optional[str] = None
    storage_type: StorageType
    path: str
    kb_schema: Dict[str, Any]
    options: Optional[Dict[str, Any]] = None

    def model_dict(self):
        if isinstance(self.storage_type, StorageType):
            self.storage_type = self.storage_type.value
        model_dict = self.dict()
        model_dict['storage_type'] = self.storage_type
        return model_dict

class DataGenerationConfig(BaseModel):
    save_outputs: Optional[bool] = None
    save_outputs_location: Optional[str] = None
    save_outputs_path: Optional[str] = None
    save_inputs: Optional[bool] = None
    save_inputs_location: Optional[str] = None
    default_filename: Optional[str] = None

class ToolDeployment(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    node: Union[NodeConfigUser, NodeConfig, Dict]
    name: Optional[str] = None
    module: Optional[Dict] = None
    config: Optional[ToolConfig] = None

class KBDeployment(BaseModel):
    node: Union[NodeConfigUser, NodeConfig, Dict]
    name: Optional[str] = None
    module: Optional[Dict] = None
    config: Optional[KBConfig] = None

    def model_dict(self):
        model_dict = self.dict()
        if isinstance(self.config, KBConfig):
            model_dict['config'] = self.config.model_dict()
        return model_dict

class EnvironmentDeployment(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    node: Union[NodeConfigUser, NodeConfig, Dict]
    name: Optional[str] = None
    module: Optional[Dict] = None
    config: Optional[EnvironmentConfig] = None

class AgentDeployment(BaseModel):
    model_config = ConfigDict(
        arbitrary_types_allowed=True
    )
    node: NodeConfig
    module: Dict[str, Any]
    name: str
    config: Optional[AgentConfig] = None
    data_generation_config: Optional[DataGenerationConfig] = None
    tool_deployments: Optional[List[ToolDeployment]] = None
    environment_deployments: Optional[List[EnvironmentDeployment]] = None
    kb_deployments: Optional[List[KBDeployment]] = None

class OrchestratorDeployment(BaseModel):
    node: Union[NodeConfigUser, NodeConfig, Dict]
    name: Optional[str] = None
    module: Optional[Dict] = None
    config: Optional[OrchestratorConfig] = None
    agent_deployments: Optional[List[AgentDeployment]] = None
    environment_deployments: Optional[List[EnvironmentDeployment]] = None
    kb_deployments: Optional[List[KBDeployment]] = None

class DockerParams(BaseModel):
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        validate_assignment=True,
        json_encoders={
            datetime: lambda v: v.isoformat(),
        }
    )
    docker_image: str
    docker_command: Optional[str] = ""
    docker_num_gpus: Optional[int] = 0
    docker_env_vars: Optional[Dict] = None
    input_dir: Optional[str] = None
    input_ipfs_hash: Optional[str] = None
    docker_input_dir: Optional[str] = None
    docker_output_dir: Optional[str] = None
    save_location: str = "node"

    def model_dict(self):
        model_dict = self.dict()
        for key, value in model_dict.items():
            if isinstance(value, datetime):
                model_dict[key] = value.isoformat()
        return model_dict

class AgentRun(BaseModel):
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        validate_assignment=True,
        json_encoders={
            datetime: lambda v: v.isoformat(),
        }
    )
    consumer_id: str
    inputs: Optional[Union[Dict, BaseModel, DockerParams]] = None
    deployment: AgentDeployment
    tool_deployments: Optional[List[ToolDeployment]] = None
    environment_deployments: Optional[List[EnvironmentDeployment]] = None
    orchestrator_runs: List['OrchestratorRun'] = []
    status: str = "pending"
    error: bool = False
    id: Optional[str] = None
    results: list[str] = []
    error_message: Optional[str] = None
    created_time: Optional[str] = None
    start_processing_time: Optional[str] = None
    completed_time: Optional[str] = None
    duration: Optional[float] = None
    input_schema_ipfs_hash: Optional[str] = None
    signature: str

    def model_dict(self):
        model_dict = self.dict()
        for key, value in model_dict.items():
            if isinstance(value, datetime):
                model_dict[key] = value.isoformat()
            elif isinstance(value, AgentModuleType):
                model_dict[key] = value.value
        for i, orchestrator_run in enumerate(model_dict['orchestrator_runs']):
            for key, value in orchestrator_run.items():
                if isinstance(value, datetime):
                    model_dict['orchestrator_runs'][i][key] = value.isoformat()
        return model_dict

class AgentRunInput(BaseModel):
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        validate_assignment=True
    )
    consumer_id: str
    inputs: Optional[Union[Dict, BaseModel, DockerParams]] = None
    deployment: AgentDeployment
    tool_deployments: Optional[List[ToolDeployment]] = None
    environment_deployments: Optional[List[EnvironmentDeployment]] = None
    kb_deployment: Optional[KBDeployment] = None
    orchestrator_runs: List['OrchestratorRun'] = []
    signature: str

    def model_dict(self):
        model_dict = self.dict()
        if isinstance(self.deployment.config, BaseModel):
            config = self.deployment.config.model_dump()
            model_dict['deployment']['config'] = config
        return model_dict


class ToolRunInput(BaseModel):
    consumer_id: str
    inputs: Optional[Union[Dict, BaseModel, DockerParams]] = None
    deployment: ToolDeployment
    agent_run: Optional[AgentRun] = None
    signature: str

    def model_dict(self):
        if isinstance(self.inputs, BaseModel):
            self.inputs = self.inputs.model_dump()
        model_dict = self.dict()
        model_dict['inputs'] = self.inputs
        return model_dict

class ToolRun(BaseModel):
    consumer_id: str
    inputs: Optional[Union[Dict, BaseModel, DockerParams]] = None
    deployment: ToolDeployment
    agent_run: Optional[AgentRun] = None
    status: str = "pending"
    error: bool = False
    id: Optional[str] = None
    results: list[str] = []
    error_message: Optional[str] = None
    created_time: Optional[str] = None
    start_processing_time: Optional[str] = None
    completed_time: Optional[str] = None
    duration: Optional[float] = None
    signature: str
class OrchestratorRunInput(BaseModel):
    consumer_id: str
    inputs: Optional[Union[Dict, BaseModel, DockerParams]] = None
    deployment: OrchestratorDeployment
    signature: str

    def model_dict(self):
        model_dict = self.dict()
        return model_dict

class OrchestratorRun(BaseModel):
    consumer_id: str
    inputs: Optional[Union[Dict, BaseModel, DockerParams]] = None
    deployment: OrchestratorDeployment
    status: str = "pending"
    error: bool = False
    id: Optional[str] = None
    results: list[str] = []
    error_message: Optional[str] = None
    created_time: Optional[str] = None
    start_processing_time: Optional[str] = None
    completed_time: Optional[str] = None
    duration: Optional[float] = None
    agent_runs: List['AgentRun'] = []
    input_schema_ipfs_hash: Optional[str] = None
    signature: str

class EnvironmentRunInput(BaseModel):
    consumer_id: str
    inputs: Optional[Union[Dict, BaseModel, DockerParams]] = None
    deployment: EnvironmentDeployment
    orchestrator_runs: List['OrchestratorRun'] = []
    signature: str

    def model_dict(self):
        model_dict = self.dict()
        return model_dict

class EnvironmentRun(BaseModel):
    consumer_id: str
    inputs: Optional[Union[Dict, BaseModel, DockerParams]] = None
    deployment: EnvironmentDeployment
    orchestrator_runs: List['OrchestratorRun'] = []
    status: str = "pending"
    error: bool = False
    id: Optional[str] = None
    results: list[str] = []
    error_message: Optional[str] = None
    created_time: Optional[str] = None
    start_processing_time: Optional[str] = None
    completed_time: Optional[str] = None
    duration: Optional[float] = None
    input_schema_ipfs_hash: Optional[str] = None
    signature: str

class KBRunInput(BaseModel):
    consumer_id: str
    inputs: Optional[Union[Dict, BaseModel, DockerParams]] = None
    deployment: KBDeployment
    orchestrator_runs: List['OrchestratorRun'] = []
    signature: str

    def model_dict(self):
        model_dict = self.dict()
        if isinstance(self.deployment, KBDeployment):
            model_dict['deployment'] = self.deployment.model_dict()
        return model_dict

class KBRun(BaseModel):
    consumer_id: str
    inputs: Optional[Union[Dict, BaseModel, DockerParams]] = None
    deployment: KBDeployment
    orchestrator_runs: List['OrchestratorRun'] = []
    status: str = "pending"
    error: bool = False
    id: Optional[str] = None
    results: list[Optional[str]] = []
    error_message: Optional[str] = None
    created_time: Optional[str] = None
    start_processing_time: Optional[str] = None
    completed_time: Optional[str] = None
    duration: Optional[float] = None
    signature: str

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatCompletionRequest(BaseModel):
    model: str
    messages: List[ChatMessage]
    temperature: Optional[float] = None
    max_tokens: Optional[int] = None
    top_p: Optional[float] = None
    frequency_penalty: Optional[float] = None
    presence_penalty: Optional[float] = None
    stop: Optional[List[str]] = None
    stream: Optional[bool] = None
    stream_options: Optional[dict] = None
    n: Optional[int] = None
    response_format: Optional[dict] = None
    seed: Optional[int] = None
    tools: Optional[List] = None
    tool_choice: Optional[str] = None
    parallel_tool_calls: Optional[bool] = None

class Choices(BaseModel):
    message: ChatMessage
    finish_reason: str
    index: int

class ModelResponse(BaseModel):
    id: str
    choices: List[Choices]
    created: int
    model: str
    object: str
