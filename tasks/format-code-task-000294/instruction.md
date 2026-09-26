## 希望增加一条审核规则：禁止使用 EVENT

我们在用 SQLE 做 SQL 审核，希望能在使用建议类规则里加一条"禁止使用 event"。

业务背景：MySQL 的 event scheduler 在我们这边一直是不推荐的写法。一方面 event 会让数据库自身承担定时任务的执行职责，运维上很难追踪到底有哪些 event 在跑、什么时候跑、谁加的；和应用侧的调度系统也容易出现重复触发。另一方面 event 里通常带 DEFINER，权限问题也比较敏感。所以我们希望直接在审核阶段把 event 相关的 DDL 拦下来。

具体来说，下面这类 SQL 在开启该规则时应该被审核出问题（出错级别）：

```sql
CREATE EVENT my_event
  ON SCHEDULE EVERY 1 DAY
  DO DELETE FROM logs WHERE created_at < NOW() - INTERVAL 30 DAY;

CREATE DEFINER = 'admin'@'%' EVENT my_event2
  ON SCHEDULE AT '2025-01-01 00:00:00'
  DO ...;

ALTER EVENT my_event DISABLE;
ALTER DEFINER = 'admin'@'%' EVENT my_event ON SCHEDULE EVERY 1 HOUR DO ...;
```

普通的 DDL/DML（CREATE TABLE / ALTER TABLE / SELECT 等）当然不应该被这条规则误报。

希望这条规则归类到"使用建议"下，跟现有的 ddl_avoid_text、ddl_avoid_full_text、ddl_avoid_geometry 这些"避免使用 xxx"的规则风格一致，便于我们在模板里统一开启。
