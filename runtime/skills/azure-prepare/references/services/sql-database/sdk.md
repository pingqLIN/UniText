---
runtime_projection: true
source_of_truth: registry/skills/azure-prepare/references/services/sql-database/sdk.md
---

> Runtime projection for consumer agents.
> First-read entrypoint: `runtime/skills/azure-prepare/references/services/sql-database/sdk.md`
> Source of truth: `registry/skills/azure-prepare/references/services/sql-database/sdk.md`
> Use this runtime file first. Follow rewritten registry links only when this runtime view points you there.
> Consumer scope: `skill-support`
# SQL Database - SDK Patterns

## Node.js (mssql)

```javascript
const sql = require('mssql');

const config = {
  server: process.env.SQL_SERVER,
  database: process.env.SQL_DATABASE,
  authentication: {
    type: 'azure-active-directory-default'
  },
  options: {
    encrypt: true
  }
};

const pool = await sql.connect(config);
```

## Python (pyodbc)

> **Auth:** `DefaultAzureCredential` is for local development. See [auth-best-practices.md](../../auth-best-practices.md) for production patterns.

```python
import pyodbc
from azure.identity import DefaultAzureCredential

credential = DefaultAzureCredential()
token = credential.get_token("https://database.windows.net/.default")

conn = pyodbc.connect(
    f"Driver={{ODBC Driver 18 for SQL Server}};"
    f"Server={os.environ['SQL_SERVER']};"
    f"Database={os.environ['SQL_DATABASE']};"
    f"Authentication=ActiveDirectoryMsi"
)
```

## .NET (Entity Framework Core)

**Required NuGet Packages:**
```bash
dotnet add package Microsoft.EntityFrameworkCore.SqlServer
dotnet add package Microsoft.Data.SqlClient --version 5.1.0
dotnet add package Azure.Identity
```

**Connection string (Entra ID):**
```
Server=tcp:{server}.database.windows.net,1433;Database={database};Authentication=Active Directory Default;Encrypt=True;
```

**Configuration:**
```csharp
services.AddDbContext<AppDbContext>(options =>
    options.UseSqlServer(
        Configuration.GetConnectionString("DefaultConnection"),
        sqlOptions => sqlOptions.EnableRetryOnFailure()
    ));
```

**appsettings.json:**
```json
{
  "ConnectionStrings": {
    "DefaultConnection": "Server=tcp:myserver.database.windows.net,1433;Database=mydb;Authentication=Active Directory Default;Encrypt=True;"
  }
}
```

## Connection String Format

```
Server=tcp:{server}.database.windows.net,1433;Database={database};Authentication=Active Directory Default;Encrypt=True;
```
