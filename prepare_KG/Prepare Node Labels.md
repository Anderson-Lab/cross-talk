# Prepare the node labels for analysis

```
match (e:Resource)
WHERE e.uri starts with 'http://purl.bioontology.org/ontology/MESH'
set e:ResourceMESH
return *;
```

```
match (e:Resource)
WHERE e.uri starts with 'http://purl.bioontology.org/ontology/MESH'
set e:ResourceMESH
return *;
```