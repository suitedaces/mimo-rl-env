## Prepared statement returns empty table / column names in result metadata

I'm connecting to TiDB from a C++ app using MySQL Connector/C++. When I run a query through a prepared statement and try to read columns by name, it fails — but the exact same code against MySQL works fine.

Minimal repro:

```cpp
#include <stdlib.h>
#include <iostream>
#include "mysql_connection.h"

#include <cppconn/driver.h>
#include <cppconn/exception.h>
#include <cppconn/resultset.h>
#include <cppconn/statement.h>
#include <cppconn/prepared_statement.h>

int main() {
    sql::Driver* driver = get_driver_instance();
    sql::Connection *conn = driver->connect("127.0.0.1:4000", "root", "");
    conn->setSchema("test");
    conn->setClientOption("libmysql_debug", "d:t:0,client.trace");
    int on_off = 1;
    conn->setClientOption("clientTrace", &on_off);

    sql::PreparedStatement *stmt = conn->prepareStatement("select * from test limit ?");
    stmt->setInt(1, 2);
    stmt->execute();

    sql::ResultSet *res = stmt->executeQuery();
    while (res->next()) {
        std::cout << res->getInt64("a") << std::endl;
    }

    delete stmt;
    delete conn;
}
```

Pointed at TiDB (port 4000) this blows up inside the connector when it tries to look up column `"a"`. Pointed at MySQL with the same schema, it just works.

With the client trace turned on I can see what the server is sending back: for the prepared statement's column metadata, the table name and column name fields are coming back empty. So when the connector builds its name-to-index map for the result set, there's nothing to match `"a"` against.

If I rewrite the same query as a plain (non-prepared) `SELECT * FROM test LIMIT 2`, the column metadata comes back populated correctly and `getInt64("a")` works. It's specifically the prepared statement path where the names are missing.

Table / column names in the result metadata of a prepared statement should be populated the same way they are for a normal query, so clients that look columns up by name work against TiDB the way they do against MySQL.
