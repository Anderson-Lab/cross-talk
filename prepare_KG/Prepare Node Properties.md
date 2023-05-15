# Prepare the node properties

```
MATCH (p:Paper)
set p.ref_number = split(p.title,".")[0]
return *
```