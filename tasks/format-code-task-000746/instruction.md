我在用 GraphQL 管 sensor / schedule 的时候有点别扭：查出来的 `Sensor.id` 和 `sensorState.id` 看起来不是同一种 id，后面想调用 `stopSensor` / `stopRunningSchedule` 还得自己把 id 拆成两段。能不能让 state 里的 id 跟外层对象的 id 对齐，并且停止的时候直接拿查到的那个 id 就能用？

Expected outcomes:
- Sensor 查询结果中，同一个 sensor 的 `Sensor.id` 与 `Sensor.sensorState.id` 应表示同一个可直接复用的 id；客户端不需要从 state id 另行推导或拆分才能停止该 sensor。
- Schedule 查询结果中，同一个 schedule 的 `Schedule.id` 与 `Schedule.scheduleState.id` 应表示同一个可直接复用的 id；客户端不需要从 state id 另行推导或拆分才能停止该 schedule。
- `stopSensor` mutation 应支持通过 `id: String` 传入查询得到的 sensor id 来停止对应 sensor。
- `stopRunningSchedule` mutation 应支持通过 `id: String` 传入查询得到的 schedule id 来停止对应 schedule。
- 旧的两参数调用方式仍应可用：`stopSensor(jobOriginId: String, jobSelectorId: String)` 与 `stopRunningSchedule(scheduleOriginId: String, scheduleSelectorId: String)` 不应被移除。
- 为兼容已有调用方，使用旧参数名但传入查询得到的完整 sensor/schedule id 的停止调用，也应无需客户端拆分该 id 即可定位并停止对应实体。
- `stopSensor` 的停止参数应允许客户端只提供可用的单个查询 id，或提供完整的旧式两参数信息；当缺少可用 id 组合时，应返回错误信息 `Must specify id or jobOriginId and jobSelectorId`。
- `stopRunningSchedule` 的停止参数应允许客户端只提供可用的单个查询 id，或提供完整的旧式两参数信息；当缺少可用 id 组合时，应返回错误信息 `Must specify id or scheduleOriginId and scheduleSelectorId`。

Implementation notes:
- 保持 GraphQL API 的向后兼容性：已有使用旧参数名的客户端应继续工作，新客户端可以直接复用查询返回的 id。
- 具体如何表示、解析、校验这些 id，以及校验逻辑放在哪一层，由实现者根据现有代码结构决定。
- 不要求改变 sensor 或 schedule 的启动、重置、权限检查语义；本任务只关注查询返回的 id 一致性和停止 mutation 的入参兼容性。
