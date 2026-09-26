## 希望新增一条审核规则：禁止使用 rename / change 修改表名和字段名

我们在用 sqle 给开发团队做 SQL 上线审核。最近线上接连出过几次故障，根因都是 DDL 里把已经在用的表名或字段名给改掉了，但应用代码里还有 SQL 依赖旧名字，发版之后业务直接报错。

我们组里定的规范是：一旦表 / 字段已经上线了，就不允许直接改名。要换名字必须走"加新字段（或新表）→ 双写 / 数据迁移 → 灰度切流 → 删旧字段（或旧表）"这一整套流程，而不是 DBA 一条 DDL 直接 rename 过去。

但目前 sqle 现有的 DDL 规范里没有一条专门拦截"改名"操作的规则。下面这几种写法审核都能正常通过：

```sql
-- 改表名
RENAME TABLE t1 TO t2;
ALTER TABLE t1 RENAME TO t2;

-- 改字段名
ALTER TABLE t1 RENAME COLUMN c1 TO c2;
ALTER TABLE t1 CHANGE COLUMN c1 c2 INT;   -- CHANGE 顺带就能把字段名改了，最容易漏
```

希望能在 DDL 规范分类里加一条新规则，把上面这几类语句识别出来并直接报错。这样开发提交改名 DDL 的时候就能在审核阶段被拦下来，引导他们走规范的迁移流程，而不是等故障了再追查。

新规则的 const key 建议叫 `DDLNotAllowRenaming`。
