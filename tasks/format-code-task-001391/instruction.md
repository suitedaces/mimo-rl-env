Query range step does not support duration string.
From slack:

> prometheus seems to accept a "step" parameter as either a duration string or float, but loki seems to >only accept integers representing seconds - are there plans for loki's API to be brought more in line with >Prometheus' API in this respect?


Easy change to support and we should be as close as possible to Prometheus.

Please also update the doc.
