# Neo4J Command Collection

## Modifying Nodes

```
MATCH (n: Resource)
SET n.base_uri = split(n.uri,"#")[0]
RETURN n
LIMIT 100
```