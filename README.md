### Site agent
|Type  |Query        |Identifier|Next Best Action|
|------|-------------|----------|----------------|
|Generic|Find the top impacted site|NA|Locate site|
|Generic|Find the top n impacted sites|NA|Locate site (topmost)|
|Specific|Find the top impacted node in the site 123|123|Locate node
|Specific|Find the top n impacted nodes in the site 123|123|Locate site
|Specific|Find the top reported alarms in the site 123|123|Locate site

### Node agent
|Type  |Query        |Identifier|Next Best Action|
|------|-------------|----------|----------------|
|Generic|Find the top impacted node|NA|Locate node|
|Generic|Find the top n impacted nodes|NA|Locate node (topmost)|
|Specific|Find the insights for node abc|abc|Locate node
|Specific|Find the top reported alarms in the node abc|abc|Locate node
|Specific|Find the occurences of 'BGP session down' on node abc|abc|Locate node

### Alarm agent
|Type  |Query        |Identifier|Next Best Action|
|------|-------------|----------|----------------|
|Generic|Find the top reported alarms|NA|Locate events monitor (filter applied)|
|Specific|Find the occurences of alarm 'BGP session down'|'BGP session down'|Locate events monitor (filter applied)|
|Specific|Find the insights for alarm xyz|xyz|Locate events monitor(filter applied)|
|Specific|How to resolve the alarm xyz|xyz|Create ticket|


### Ticket agent
|Type  |Query        |Identifier|Next Best Action|
|------|-------------|----------|----------------|
|Specific|Find the tickets for the alarm 'BGP session down'|BGP session down|Locate ticket(recent)|
|Generic|Find the ticket for the alarm xyz|xyz|Locate ticket|
|Specific|Create a ticket for resolving the alarm xyz|xyz|Create ticket
