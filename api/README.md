# LLG-Mapper

## API

The API for this project is a Python Flask application that manages a relational database using SQLAlchemy.

---

## Database Schema

### Enums
#### Frequency
    ONCE
    WEEKLY
    WEEK_A
    WEEK_B

---

#### Colors
    BLUE
    GREEN
    RED
    YELLOW
    PURPLE
    ORANGE
    GRAY

---

#### Grades
    10 = 2nd
    11 = 1re
    12 = Tle
    13 = CPGE 1
    14 = CPGE 2

---

### Building
- **id** (primary key)
- name
- code
- floor (use for uneven grounds, when one building is built higher than another)
- *rooms* (one-to-many)

*Data example*
| id | name        | code | floor | rooms      |
|----|-------------|------|-------|------------|
| 0  | Molière     | M    | 0     | *rooms...* |
| 1  | Victor Hugo | VH   | 1     | *rooms...* |

---

### RoomType
- **id** (primary key)  
- name  
- code  
- *rooms* (one-to-many)

*Data example*
| id | name        | code  | rooms      |
|----|-------------|-------|------------|
| 0  | Classroom   | CLASS | *rooms...* |
| 1  | Laboratory  | LAB   | *rooms...* |

---

### Feature
- **id** (primary key)
- name
- code
- *rooms* (many-to-many)

*Data example*
| id | name        | code   | rooms      |
|----|-------------|--------|------------|
| 0  | Computer    | PC     | *rooms...* |
| 1  | White board | WBOARD | *rooms...* |

---

### Room
- **id** (primary key)
- number
- name *(optional — defaults to `[Building.code][Room.number]`, e.g. `M209`)*
- *building* (many-to-one)
- floor
- capacity
- is_open
- *type* (many-to-one)
- location
- size
- *features* (many-to-many)
- classes

*Data example*
| id | number | name            | building_id | floor | capacity | is_open | type_id | locationX | locationY | sizeX | sizeY | classes      |
|----|--------|-----------------|-------------|-------|----------|---------|---------|-----------|-----------|-------|-------|--------------|
| 0  | 209    | M209 (default)  | 0           | 2     | 40       | false   | 0       | 2         | 53        | 20    | 50    | *classes...* |
| 1  | 46     | VH046 (default) | 1           | 0     | 40       | true    | 0       | 130       | 47        | 60    | 40    | *classes...* |

### room_features *(many-to-many table)*
- *room_id* (one-to-many)
- *feature_id* (one-to-many)

| room_id | feature_id |
|---------|------------|
| 0       | 0          |
| 0       | 1          |
| 1       | 1          |

---

### Subject
- **id** (primary key)
- name
- code
- color ([enum](#colors))
- *classes* ([one-to-many](#classes))

*Data example*
| id | name        | code   | color | classes      |
|----|-------------|--------|-------|--------------|
| 0  | Maths       | MATH   | BLUE  | *classes...* |
| 1  | French      | FR     | GREEN | *classes...* |

---

### Teacher
- **id** (primary key)
- name `{"M" | "Mme."} {surname} {name}`
- gender
- *subject* ([many-to-one](#subject))
- *classes* ([one-to-many](#classes))

*Data example*
| id | name   | surname   | gender | subject | classes      |
|----|--------|-----------|--------|---------|--------------|
| 0  | Dupont | Michel    | 0      | 1       | *classes...* |
| 1  | Daval  | Françoise | 1      | 3       | *classes...* |

---

### Group
- **id** (primary key)
- name
- grade (enum: [Grade](#grades))

*Data example*
| id | name   | grade |
|----|--------|-------|
| 0  | 2nd1   | 10    |
| 1  | PCSI 1 | 13    |

---

### Classes
- **id** (primary key)
- *room* ([many-to-one](#room))
- *teacher* ([many-to-one](#teacher)) <div style="border:1px solid #f1c40f; padding:10px; background: #a33400ff; border-radius:5px;">⚠️ <strong>Warning:</strong> SAFETY ISSUE, MIGHT NOT USE IN PROD</div>
- *group* ([many-to-one](#group))
- start_date
- ?end_date (leave NULL if one-off class)
- start_time
- end_time
- recurrence (enum: [Frequency](#frequency))
- weekday

---

## Endpoints

```text
api/
│
├── rooms/
│   ├── GET    /rooms
│   │          └── Optional query parameters:
│   │              ?building_id=<Integer>&floor=<Integer>&feature_codes=[<String>...]&is_available=<Boolean>&availability_at=YYYY-MM-DDTHH:MM:SS
│   │
│   ├── GET    /rooms/<id>
│   │
│   ├── POST   /rooms
│   │          └── body: {
│   │                 number,
│   │                 name?,
│   │                 building_id,
│   │                 floor,
│   │                 capacity?,
│   │                 is_open?,
│   │                 type_id?,
│   │                 [feature_id...]?
│   │              }
│   │
│   ├── PUT    /rooms/<id>
│   │          └── body: partial update
│   │
│   └── DELETE /rooms/<id>
│
├── classes/
│   ├── GET    /classes
│   │
│   ├── GET    /classes/<id>
│   │
│   ├── POST   /classes
│   │
│   ├── PUT    /rooms/<id>
│   │          └── body: partial update
│   │
│   └── DELETE /rooms/<id>
│
├── buildings/
│   ├── GET    /buildings
│   └── POST   /buildings
│
├── room-types/
│   ├── GET    /room-types
│   └── POST   /room-types
│
├── features/
│   ├── GET    /features
│   └── POST   /features
│
├── teachers/
│   ├── GET    /teachers
│   ├── GET    /teachers/<id>
│   └── POST   /teachers
│
├── groups/
│   ├── GET    /groups
│   └── POST   /groups
│
├── health/
│   └── GET    /health
│
└── __init__.py
