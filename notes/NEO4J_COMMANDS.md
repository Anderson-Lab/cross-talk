# Neo4J Command Collection

## Modifying Nodes

```
MATCH (n: Resource)
SET n.base_uri = split(n.uri,"#")[0]
RETURN n
LIMIT 100
```

## Finding annotations

Below is an example that annotates the contents field within each of the texts.
```
$APPDIR/scripts/annotate_dir.sh $DATADIR/texts contents | grep 'Completed\|Failed'
```

## Loading text



## Annotating text to entities

