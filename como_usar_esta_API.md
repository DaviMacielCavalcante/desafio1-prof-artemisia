# **API Documentation (main.py)**

This API was developed for CRUD operations on specific tables in a PostgreSQL database. Below is a detailed description of each endpoint, the data models used, and how to configure the application for deployment.

---

## **Endpoints**

### **1. Create a New Data Entry**

- **URL**: `/data/{table}/`
- **Method**: `POST`
- **Description**: Inserts a new entry into the specified table.
- **Parameters**:
  - `table` (path): Table name (e.g., `telecom`, `ti`, `serv_audiovisuais`).
- **Request Body**:
  ```json
  {
      "ano": 2022,
      "receita_liquida": 5000.00,
      "custo_mercadorias": 1500.00
  }
  ```

**Response**: `201 Created`, returns the created entry.

### **2. List All Entries in a Table**

- **URL**: `/data/{table}/`
- **Method**: `GET`
- **Description**: Returns a list of all entries in a table.
- **Parameters**:
    - `table` (path): Table name.

**Response**: `200 OK`, returns a list of `DataEntry` objects.

### **3. Get Entry by Year**

- **URL**: `/data/{table}/{year}`
- **Method**: `GET`
- **Description**: Returns a specific entry for a given year in a table.
- **Parameters**:
    - `table` (path): Table name.
    - `year` (path): Specific year.

**Response**: `200 OK`, returns a `DataEntry` object.

### **4. Update Entry by Year**

- **URL**: `/data/{table}/{year}`
- **Method**: `PUT`
- **Description**: Updates an existing entry with the provided data.
- **Parameters**:
    - `table` (path): Table name.
    - `year` (path): Specific year of the entry to be updated.
- **Request Body**:
  ```json
  {
      "ano": 2022,
      "receita_liquida": 5500.00
  }
  ```

**Response**: `200 OK`, returns the updated entry.

### **5. Delete Entry by Year**

- **URL**: `/data/{table}/{year}`
- **Method**: `DELETE`
- **Description**: Removes a specific entry for a given year in a table.
- **Parameters**:
    - `table` (path): Table name.
    - `year` (path): Specific year.

**Response**: `200 OK`, returns a confirmation message.

---

## **Data Models: `DataEntry`**

Model used to represent and validate the input and output data of the API.

```json
{
    "ano": int,
    "receita_liquida": float,
    "custo_mercadorias": float,
    "subvencoes_receitas_op": float,
    "valor_bruto_producao": float,
    "consumo_intermediario_total": float,
    "consumo_combustiveis": float,
    "numero_empresas": float
}
```

### **Table Structure**
All tables have a similar base structure, with fields for financial data, consumption, and company numbers.

---

## **Usage Examples**

### **1. Create a New Entry:**
```bash
curl -X POST "http://localhost:8000/data/telecom/" -d '{
    "ano": 2023,
    "receita_liquida": 4500.0
}'
```

### **2. List All Entries in a Table:**
```bash
curl -X GET "http://localhost:8000/data/telecom/"
```

### **3. Get Data by Year:**
```bash
curl -X GET "http://localhost:8000/data/telecom/2022"
```

### **4. Update Data:**
```bash
curl -X PUT "http://localhost:8000/data/telecom/2022" -d '{
    "ano": 2022,
    "receita_liquida": 4800.0
}'
```

### **5. Delete Data:**
```bash
curl -X DELETE "http://localhost:8000/data/telecom/2022"
```

---

*Through victory, my chains are broken. The Force shall free me.*

