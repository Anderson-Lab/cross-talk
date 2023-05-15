# First KG Example Figure

```
MATCH (p:Paper {title:'41.pdf'})-[r:HAS_ENTITY]->(e:ResourceMESH)<-[r2:HAS_ENTITY]-(p2:Paper {title:'49.pdf'})
RETURN *
```