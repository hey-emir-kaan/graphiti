from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from neo4j import AsyncDriver

from graphiti_core.edges import Edge
from graphiti_core.nodes import Node
from graphiti_core.search.search_filters import SearchFilters
from graphiti_core.search.search_utils import RELEVANT_SCHEMA_LIMIT


class GraphStore(ABC):
    """Abstract interface for graph data stores."""

    driver: AsyncDriver | None = None

    @abstractmethod
    async def connect(self, uri: str, user: str, password: str) -> None:
        """Establish the connection to the backing store."""

    @abstractmethod
    async def close(self) -> None:
        """Close any open connections."""

    @abstractmethod
    async def execute_query(self, query: str, **params: Any) -> tuple:
        """Execute a raw query against the store."""

    # Node operations -----------------------------------------------------
    @abstractmethod
    async def save_node(self, node: Node) -> Any:
        """Persist a node in the store."""

    @abstractmethod
    async def get_node_by_uuid(self, node_cls: type[Node], uuid: str) -> Node:
        """Retrieve a node by UUID."""

    @abstractmethod
    async def delete_node(self, node: Node) -> Any:
        """Delete a node from the store."""

    # Edge operations -----------------------------------------------------
    @abstractmethod
    async def save_edge(self, edge: Edge) -> Any:
        """Persist an edge in the store."""

    @abstractmethod
    async def get_edge_by_uuid(self, edge_cls: type[Edge], uuid: str) -> Edge:
        """Retrieve an edge by UUID."""

    @abstractmethod
    async def delete_edge(self, edge: Edge) -> Any:
        """Delete an edge from the store."""

    # Search --------------------------------------------------------------
    @abstractmethod
    async def search_nodes(
        self,
        query: str,
        search_filter: SearchFilters,
        group_ids: list[str] | None = None,
        limit: int = RELEVANT_SCHEMA_LIMIT,
    ) -> list[Node]:
        """Search nodes in the store."""

    @abstractmethod
    async def search_edges(
        self,
        query: str,
        search_filter: SearchFilters,
        group_ids: list[str] | None = None,
        limit: int = RELEVANT_SCHEMA_LIMIT,
    ) -> list[Edge]:
        """Search edges in the store."""

