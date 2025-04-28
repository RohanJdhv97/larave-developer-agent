# Database Schema Design

Normalization Level: 3NF

## Tables

### users
Description: Stores user account information

#### Columns
- id: bigint NOT NULL
- name: varchar(255) NOT NULL
- email: varchar(255) NOT NULL
- password: varchar(255) NOT NULL
- remember_token: varchar(100) NULL

#### Indexes
- UNIQUE KEY on (email)

#### Relationships
- One To One relationship with profiles (id -> user_id)

#### Features
- Timestamps (created_at, updated_at)

### profiles
Description: Stores user profile information

#### Columns
- id: bigint NOT NULL
- user_id: bigint NOT NULL
- bio: text NULL
- avatar: varchar(255) NULL

#### Indexes
- INDEX KEY on (user_id)

#### Features
- Timestamps (created_at, updated_at)

## Entity Relationships

```
+------------------+
| USERS            |
+------------------+
| id               |
| name             |
| email            |
| password         |
| remember_token   |
+------------------+

+------------------+
| PROFILES         |
+------------------+
| id               |
| user_id          |
| bio              |
| avatar           |
+------------------+

Relationships:
users.id 1:1 profiles.user_id
```