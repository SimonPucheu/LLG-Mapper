# LLG-Mapper API

A modern Python Flask REST API for managing school room scheduling, built with **SQLAlchemy ORM** and **Marshmallow** for robust data validation and serialization.

---

## Table of Contents

- [Quick Start](#quick-start)
- [Architecture](#architecture)
- [Database Schema](#database-schema)
- [API Endpoints](#api-endpoints)
- [Request/Response Examples](#requestresponse-examples)
- [Data Types & Enums](#data-types--enums)

---

## Quick Start

### Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Initialize database
python scripts/dbCreate.bat  # Windows
# or
bash scripts/dbCreate.sh     # Linux/Mac

# Run development server
python app.py
```

The API will be available at `http://localhost:5000`

---

## Architecture

### Tech Stack

- **Framework**: Flask 3.1.2
- **Database**: SQLAlchemy 2.0.45 (with SQLite)
- **Migrations**: Flask-Migrate (Alembic)
- **Serialization**: Marshmallow 3.21.3
- **CORS**: Flask-CORS 6.0.2

### Project Structure

```
api/
├── app/
│   ├── __init__.py           # Flask app factory
│   ├── config.py             # Configuration management
│   ├── extensions.py         # Flask extensions (db, migrate)
│   ├── models/               # SQLAlchemy ORM models
│   │   ├── building.py
│   │   ├── room.py
│   │   ├── class_.py
│   │   ├── teacher.py
│   │   ├── group.py
│   │   ├── subject.py
│   │   ├── feature.py
│   │   ├── room_type.py
│   │   └── enums.py
│   ├── schemas/              # Marshmallow validation/serialization
│   │   ├── building.py
│   │   ├── room.py
│   │   ├── class_.py
│   │   ├── teacher.py
│   │   ├── group.py
│   │   ├── subject.py
│   │   ├── feature.py
│   │   └── room_type.py
│   ├── routes/               # API endpoints
│   │   ├── buildings.py
│   │   ├── rooms.py
│   │   ├── classes.py
│   │   └── health.py
│   └── services/             # Business logic
│       └── availability_service.py
├── migrations/               # Database migrations (Alembic)
├── requirements.txt
└── README.md
```

---

## Database Schema

### Data Models

#### Building
Main building/campus entity for organizing rooms.

| Field | Type | Constraints |
|-------|------|-------------|
| id | Integer | Primary Key |
| name | String(50) | Unique, Required |
| code | String(3) | Unique, Required |
| floor | Integer | Default: 0 (for uneven grounds) |

**Example:**
```json
{
  "id": 1,
  "name": "Victor Hugo",
  "code": "VH",
  "floor": 1
}
```

---

#### RoomType
Classification of room types (classroom, lab, auditorium, etc.).

| Field | Type | Constraints |
|-------|------|-------------|
| id | Integer | Primary Key |
| name | String(50) | Unique, Required |
| code | String(10) | Unique, Required |

**Example:**
```json
{
  "id": 1,
  "name": "Laboratory",
  "code": "LAB"
}
```

---

#### Feature
Room amenities/equipment (projector, whiteboard, computers, etc.).

| Field | Type | Constraints |
|-------|------|-------------|
| id | Integer | Primary Key |
| name | String(50) | Unique, Required |
| code | String(10) | Unique, Required |

**Example:**
```json
{
  "id": 1,
  "name": "Projector",
  "code": "PROJ"
}
```

---

#### Room
Physical classroom or space.

| Field | Type | Constraints |
|-------|------|-------------|
| id | Integer | Primary Key |
| number | Integer | Required |
| name | String(50) | Optional (auto: `{building.code}{number}`) |
| building_id | Integer | Foreign Key → Building |
| floor | Integer | Required |
| capacity | Integer | Optional |
| is_open | Boolean | Default: true |
| type_id | Integer | Foreign Key → RoomType |
| locationX | Integer | Required (map coordinate) |
| locationY | Integer | Required (map coordinate) |
| sizeX | Integer | Required (map dimension) |
| sizeY | Integer | Required (map dimension) |

**Relationships:**
- Building (Many-to-One)
- RoomType (Many-to-One)
- Features (Many-to-Many via room_features)
- Classes (One-to-Many)

**Example:**
```json
{
  "id": 1,
  "number": 209,
  "name": "VH209",
  "building": {"id": 1, "name": "Victor Hugo", "code": "VH", "floor": 1},
  "floor": 2,
  "capacity": 40,
  "is_open": true,
  "type": {"id": 1, "name": "Classroom", "code": "CLASS"},
  "location": [130, 47],
  "size": [60, 40],
  "features": [
    {"id": 1, "name": "Projector", "code": "PROJ"},
    {"id": 2, "name": "Whiteboard", "code": "WBOARD"}
  ]
}
```

---

#### Subject
Academic subject (Math, French, Physics, etc.).

| Field | Type | Constraints |
|-------|------|-------------|
| id | Integer | Primary Key |
| name | String(50) | Unique, Required |
| code | String(10) | Unique, Required |
| color | Enum(Color) | Default: BLUE |

**Color Options:** `BLUE`, `GREEN`, `RED`, `YELLOW`, `PURPLE`, `ORANGE`, `GRAY`

**Example:**
```json
{
  "id": 1,
  "name": "Mathematics",
  "code": "MATH",
  "color": "BLUE"
}
```

---

#### Teacher
Instructor information.

| Field | Type | Constraints |
|-------|------|-------------|
| id | Integer | Primary Key |
| name | String(50) | Required |
| surname | String(50) | Required |
| gender | Boolean | Required (true=F, false=M) |
| subject_id | Integer | Foreign Key → Subject (Optional) |

**Relationships:**
- Subject (Many-to-One)
- Classes (One-to-Many)

**Example:**
```json
{
  "id": 1,
  "name": "Michel Dupont",
  "surname": "Dupont",
  "gender": false,
  "subject": {"id": 1, "name": "Mathematics", "code": "MATH", "color": "BLUE"}
}
```

> **Note:** Response includes formatted name with gender prefix (`M`/`Mme.`)

---

#### Group
Student class/cohort.

| Field | Type | Constraints |
|-------|------|-------------|
| id | Integer | Primary Key |
| name | String(50) | Required |
| grade | Enum(Grade) | Required |

**Grade Options:**
- `10` = 2nde (Grade 10)
- `11` = 1ère (Grade 11)
- `12` = Terminale (Grade 12)
- `13` = CPGE 1 (Grade 13)
- `14` = CPGE 2 (Grade 14)

**Example:**
```json
{
  "id": 1,
  "name": "2nd-1",
  "grade": 10
}
```

---

#### Class
Scheduled class session.

| Field | Type | Constraints |
|-------|------|-------------|
| id | Integer | Primary Key |
| room_id | Integer | Foreign Key → Room (Required) |
| teacher_id | Integer | Foreign Key → Teacher (Required) |
| group_id | Integer | Foreign Key → Group (Required) |
| subject_id | Integer | Foreign Key → Subject (Required) |
| start_date | Date | Required |
| end_date | Date | Optional (NULL = one-off session) |
| start_time | Time | Required |
| end_time | Time | Required |
| recurrence | Enum(Frequency) | Default: WEEKLY |
| weekday | Integer | 0=Monday, 6=Sunday (optional) |

**Weekdays**
0 = Monday
...
6 = Sunday

**Recurrence Options:**
- `ONCE` = One-time session
- `WEEKLY` = Every week
- `WEEK_A` = Alternating week A
- `WEEK_B` = Alternating week B

**Relationships:**
- Room (Many-to-One)
- Teacher (Many-to-One)
- Group (Many-to-One)
- Subject (Many-to-One)

**Example:**
```json
{
  "id": 1,
  "room": {...},
  "teacher": {...},
  "group": {...},
  "subject": {...},
  "start_date": "2024-01-15",
  "end_date": "2024-06-30",
  "start_time": "09:00:00",
  "end_time": "10:00:00",
  "recurrence": "WEEKLY",
  "weekday": 0
}
```

---

## API Endpoints

### Endpoint Reference

**Active Endpoints:**
- [Health Check](#health-check)
  - `GET /health`

- [Buildings](#buildings)
  - [`GET /buildings`](#list-all-buildings) - List all buildings
  - [`GET /buildings/{id}`](#get-building-by-id) - Get building by ID
  - [`POST /buildings`](#create-building) - Create building
  - [`PUT /buildings/{id}`](#update-building) - Update building
  - [`DELETE /buildings/{id}`](#delete-building) - Delete building

- [Rooms](#rooms)
  - [`GET /rooms`](#list-rooms-with-filtering--availability) - List rooms (with filtering & availability)
  - [`GET /rooms/{id}`](#get-room-by-id) - Get room by ID
  - [`POST /rooms`](#create-room) - Create room
  - [`PUT /rooms/{id}`](#update-room) - Update room
  - [`DELETE /rooms/{id}`](#delete-room) - Delete room

- [Classes](#classes)
  - [`GET /classes`](#list-classes) - List classes
  - [`GET /classes/{id}`](#get-class-by-id) - Get class by ID
  - [`POST /classes`](#create-class) - Create class
  - [`PUT /classes/{id}`](#update-class) - Update class
  - [`DELETE /classes/{id}`](#delete-class) - Delete class

**Planned Endpoints (Coming Soon):**
- Room Types
  - `GET /room-types` - List room types
  - `POST /room-types` - Create room type

- Features
  - `GET /features` - List features
  - `POST /features` - Create feature

- Teachers
  - `GET /teachers` - List teachers
  - `GET /teachers/{id}` - Get teacher by ID
  - `POST /teachers` - Create teacher

- Groups
  - `GET /groups` - List groups
  - `POST /groups` - Create group

### Health Check

```http
GET /health
```

**Response (200 OK):**
```json
{
  "status": "ok"
}
```

---

### Buildings

#### List All Buildings
```http
GET /buildings
```

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "name": "Victor Hugo",
    "code": "VH",
    "floor": 1
  }
]
```

#### Get Building by ID
```http
GET /buildings/{id}
```

#### Create Building
```http
POST /buildings
Content-Type: application/json

{
  "name": "Molière",
  "code": "M",
  "floor": 0
}
```

**Response (201 Created):**
```json
{
  "id": 1,
  "name": "Molière",
  "code": "M",
  "floor": 0
}
```

#### Update Building
```http
PUT /buildings/{id}
Content-Type: application/json

{
  "floor": 1
}
```

#### Delete Building
```http
DELETE /buildings/{id}
```

**Response (204 No Content)**

---

### Rooms

#### List Rooms (with filtering & availability)

```http
GET /rooms?building_id=1&floor=2&feature_codes=PROJ,WBOARD&is_available=true&availability_at=2024-01-15T09:00:00
```

**Query Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| building_id | integer | Filter by building |
| floor | integer | Filter by floor number |
| feature_codes | string[] | Filter by features (comma-separated codes) |
| is_available | boolean | Filter by availability status |
| availability_at | ISO datetime | Check availability at specific time |

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "number": 209,
    "name": "VH209",
    "building": {...},
    "floor": 2,
    "capacity": 40,
    "is_open": true,
    "type": {...},
    "location": [130, 47],
    "size": [60, 40],
    "features": [...]
  }
]
```

Or with availability:
```json
{
  "availability_at": "2024-01-15T09:00:00",
  "rooms": [...]
}
```

#### Get Room by ID
```http
GET /rooms/{id}
```

#### Create Room
```http
POST /rooms
Content-Type: application/json

{
  "number": 209,
  "name": "VH209",
  "building_id": 1,
  "floor": 2,
  "capacity": 40,
  "is_open": true,
  "type_id": 1,
  "locationX": 130,
  "locationY": 47,
  "sizeX": 60,
  "sizeY": 40,
  "feature_ids": [1, 2]
}
```

**Response (201 Created):**
```json
{
  "id": 1,
  "number": 209,
  "name": "VH209",
  ...
}
```

#### Update Room
```http
PUT /rooms/{id}
Content-Type: application/json

{
  "capacity": 45,
  "is_open": false,
  "feature_ids": [1, 3]
}
```

#### Delete Room
```http
DELETE /rooms/{id}
```

**Response (204 No Content)**

---

### Classes

#### List Classes
```http
GET /classes
```

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "room": {...},
    "teacher": {...},
    "group": {...},
    "subject": {...},
    "start_date": "2024-01-15",
    "end_date": "2024-06-30",
    "start_time": "09:00:00",
    "end_time": "10:00:00",
    "recurrence": "WEEKLY",
    "weekday": 0
  }
]
```

#### Get Class by ID
```http
GET /classes/{id}
```

#### Create Class
```http
POST /classes
Content-Type: application/json

{
  "room_id": 1,
  "teacher_id": 1,
  "group_id": 1,
  "subject_id": 1,
  "start_date": "2024-01-15",
  "end_date": "2024-06-30",
  "start_time": "09:00:00",
  "end_time": "10:00:00",
  "recurrence": "WEEKLY",
  "weekday": 0
}
```

**Response (201 Created):**
```json
{
  "id": 1,
  ...
}
```

#### Update Class
```http
PUT /classes/{id}
Content-Type: application/json

{
  "start_time": "10:00:00",
  "end_time": "11:00:00"
}
```

#### Delete Class
```http
DELETE /classes/{id}
```

**Response (204 No Content)**

---

## Request/Response Examples

### Error Handling

All endpoints return validation errors with detailed messages:

```http
POST /buildings
Content-Type: application/json

{
  "name": "Test"
}
```

**Response (400 Bad Request):**
```json
{
  "errors": {
    "code": ["Missing data for required field."]
  }
}
```

### Date/Time Formatting

- **Dates**: ISO format `YYYY-MM-DD`
- **Times**: ISO format `HH:MM:SS`
- **DateTime**: ISO format `YYYY-MM-DDTHH:MM:SS`

### Location & Size

Room coordinates are returned as arrays:
```json
{
  "location": [130, 47],  // [X, Y]
  "size": [60, 40]        // [width, height]
}
```

---

## Data Types & Enums

### Frequency (Class Recurrence)
```
ONCE   - "once"
WEEKLY - "weekly"
WEEK_A - "weekA"
WEEK_B - "weekB"
```

### Color (Subject Color)
```
BLUE
GREEN
RED
YELLOW
PURPLE
ORANGE
GRAY
```

### Grade (Student Grade Level)
```
10 → 2nde (Grade 10)
11 → 1ère (Grade 11)
12 → Terminale (Grade 12)
13 → CPGE 1 (Grade 13)
14 → CPGE 2 (Grade 14)
```

---

## Development Notes

### Database Migrations

```bash
# Create new migration
flask db migrate -m "Description"

# Apply migrations
flask db upgrade

# Rollback
flask db downgrade
```

### Validation

All POST/PUT requests are validated using Marshmallow schemas:
- Type checking
- Required field validation
- Relationship integrity

### Serialization

Responses automatically handle:
- Enum value conversion
- Datetime/Date/Time formatting
- Nested relationship serialization
- Field inclusion/exclusion based on context

---

## Future Endpoints (Planned)

Currently commented out but ready to implement:
- `GET/POST /room-types`
- `GET/POST /features`
- `GET/POST /teachers`
- `GET/POST /groups`

Uncomment in `app/routes/__init__.py` and `app/__init__.py` when needed.
