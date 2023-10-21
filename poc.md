# Initial PoC
- based on swapping all websocket interaction with nostr messaging
- only using Encrypted Direct Messages (nostr kind 4)
- Queenbee is a nostr client, workerbees are nostr clients
- workerbees only message  the Queenbee, using its public key
- normal business logic is not changed: queenbee receives api requests from clients, and selects the worker to be used normally.

### Diagram
     client                          queenbee                          workerbee
      |                                  |                                 |
      | -- POST /v1/chat/completions --> |                                 |
      |                             select worker                          |
      |                                  |                                 |
      |                                  | --- send DM (do_inference) ---> |
      |                                  |                                 |
      |                                  |                              process job
      |                                  |                                 |
      |                                  | <--- send DM (job_result) ----- |
      |                                  |                                 |
      |                                  |                                 |

# NIP-90 Path 1
- queenbee is a service provider of several kind of job types (right now "inference" and "training")
- workerbees come and go freely
- workerbees are the compute backend of queenbee
- when queenbee receives a job request, it communicates with workerbees with normal websocket logic

# NIP-90 Path 2
- queenbee is removed from flow

# Other ideas
- rest api is removed, queenbee is reachable via nostr nip-90