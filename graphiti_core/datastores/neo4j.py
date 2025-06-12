from __future__ import annotations

from typing import Any

from neo4j import AsyncGraphDatabase, AsyncDriver

from graphiti_core.datastores.base import GraphStore
from graphiti_core.edges import Edge
from graphiti_core.nodes import Node
from graphiti_core.search.search_filters import SearchFilters
from graphiti_core.search.search_utils import (
    RELEVANT_SCHEMA_LIMIT,
    edge_fulltext_search,
    node_fulltext_search,
)


class Neo4jGraphStore(GraphStore):
    """Neo4j-based implementation of :class:`GraphStore`."""

    def __init__(self, uri: str | None = None, user: str | None = None, password: str | None = None) -> None:
        if uri and user and password:
            self.driver = AsyncGraphDatabase.driver(uri, auth=(user, password))
        else:
            self.driver = None

    async def connect(self, uri: str, user: str, password: str) -> None:
        self.driver = AsyncGraphDatabase.driver(uri, auth=(user, password))

    async def close(self) -> None:
        if self.driver:
            await self.driver.close()

    async def execute_query(self, query: str, **params: Any) -> tuple:
        if not self.driver:
            raise RuntimeError("GraphStore not connected")
        return await self.driver.execute_query(query, **params)

    # Node operations -----------------------------------------------------
    async def save_node(self, node: Node) -> Any:
        if not self.driver:
            raise RuntimeError("GraphStore not connected")
        return await node.save(self.driver)

    async def get_node_by_uuid(self, node_cls: type[Node], uuid: str) -> Node:
        if not self.driver:
            raise RuntimeError("GraphStore not connected")
        return await node_cls.get_by_uuid(self.driver, uuid)

    async def delete_node(self, node: Node) -> Any:
        if not self.driver:
            raise RuntimeError("GraphStore not connected")
        return await node.delete(self.driver)

    # Edge operations -----------------------------------------------------
    async def save_edge(self, edge: Edge) -> Any:
        if not self.driver:
            raise RuntimeError("GraphStore not connected")
        return await edge.save(self.driver)

    async def get_edge_by_uuid(self, edge_cls: type[Edge], uuid: str) -> Edge:
        if not self.driver:
            raise RuntimeError("GraphStore not connected")
        return await edge_cls.get_by_uuid(self.driver, uuid)

    async def delete_edge(self, edge: Edge) -> Any:
        if not self.driver:
            raise RuntimeError("GraphStore not connected")
        return await edge.delete(self.driver)

    # Search --------------------------------------------------------------
    async def search_nodes(
        self,
        query: str,
        search_filter: SearchFilters,
        group_ids: list[str] | None = None,
        limit: int = RELEVANT_SCHEMA_LIMIT,
    ) -> list[Node]:
        if not self.driver:
            raise RuntimeError("GraphStore not connected")
        return await node_fulltext_search(self.driver, query, search_filter, group_ids, limit)

    async def search_edges(
        self,
        query: str,
        search_filter: SearchFilters,
        group_ids: list[str] | None = None,
        limit: int = RELEVANT_SCHEMA_LIMIT,
    ) -> list[Edge]:
        if not self.driver:
            raise RuntimeError("GraphStore not connected")
        return await edge_fulltext_search(self.driver, query, search_filter, group_ids, limit)

