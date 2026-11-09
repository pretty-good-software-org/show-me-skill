# Mermaid diagram types

Choose the diagram whose structure answers the user's question with the fewest nodes and edges. Keep labels concrete,
omit unrelated implementation detail, and prefer one focused diagram over a comprehensive map.

| Question                                              | Diagram                            |
| ----------------------------------------------------- | ---------------------------------- |
| What happens, including decisions and parallel paths? | Flowchart or activity diagram      |
| Which states exist and what causes transitions?       | State diagram                      |
| How do code or domain types relate?                   | Class or domain model              |
| How do persisted entities relate?                     | Entity-relationship diagram        |
| Which modules or services depend on each other?       | Architecture or dependency diagram |
| Where do runtime components execute?                  | Deployment diagram                 |

## Flowchart or activity diagram

Use for workflows, algorithms with branches, and parallel activities. Name decisions as questions and label outgoing
edges with their conditions.

```mermaid
flowchart TD
    Receive[Receive order] --> Authorized{Payment authorized?}
    Authorized -- Yes --> Reserve[Reserve inventory]
    Authorized -- No --> Reject[Reject order]
    Reserve --> Available{Inventory available?}
    Available -- Yes --> Ship[Create shipment]
    Available -- No --> Refund[Issue refund]
```

## State diagram

Use for lifecycle states and event-driven transitions. Show initial and terminal states when they matter; label each
transition with the event or condition that causes it.

```mermaid
stateDiagram-v2
    [*] --> Draft
    Draft --> Submitted: submit
    Submitted --> Approved: approve
    Submitted --> Rejected: reject
    Rejected --> Draft: revise
    Approved --> Archived: archive
    Archived --> [*]
```

## Class or domain model

Use for types, ownership, cardinality, and inheritance. Include only members needed to explain the relationship under
discussion.

```mermaid
classDiagram
    class Customer {
        +CustomerID id
        +placeOrder()
    }
    class Order {
        +OrderID id
        +OrderStatus status
        +calculateTotal()
    }
    class LineItem {
        +int quantity
        +subtotal()
    }
    class Product {
        +ProductID id
        +Money price
    }

    Customer "1" --> "*" Order : places
    Order "1" *-- "*" LineItem : contains
    LineItem "*" --> "1" Product : references
```

## Entity-relationship diagram

Use for persisted data, keys, and cardinality. Distinguish it from a class diagram: model storage entities and database
relationships rather than runtime behavior.

```mermaid
erDiagram
    CUSTOMER ||--o{ ORDER : places
    ORDER ||--|{ LINE_ITEM : contains
    PRODUCT ||--o{ LINE_ITEM : appears_in

    CUSTOMER {
        uuid id PK
        string email UK
    }
    ORDER {
        uuid id PK
        uuid customer_id FK
        string status
    }
    LINE_ITEM {
        uuid order_id FK
        uuid product_id FK
        int quantity
    }
    PRODUCT {
        uuid id PK
        string name
        decimal price
    }
```

## Architecture or dependency diagram

Use for service, package, or module boundaries and their directional dependencies. Group nodes only when the boundary
changes ownership, trust, or responsibility.

```mermaid
flowchart LR
    Browser --> WebApp
    WebApp --> API
    API --> Orders
    API --> Payments
    Orders --> Database[(PostgreSQL)]
    Payments --> Provider[Payment provider]
    Orders --> Queue[(Event queue)]
    Queue --> Worker
```

## Deployment diagram

Use for runtime placement, infrastructure boundaries, replicas, and managed dependencies. Show logical architecture
instead when physical placement is irrelevant to the question.

```mermaid
flowchart TB
    User --> CDN

    subgraph Cloud
        CDN --> LoadBalancer[Load balancer]

        subgraph ApplicationCluster[Application cluster]
            LoadBalancer --> API1[API replica]
            LoadBalancer --> API2[API replica]
            Worker[Background worker]
        end

        API1 --> Database[(Managed PostgreSQL)]
        API2 --> Database
        Worker --> Database
        API1 --> Queue[(Managed queue)]
        API2 --> Queue
        Queue --> Worker
    end
```
