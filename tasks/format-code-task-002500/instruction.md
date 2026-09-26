我在 Swift 里写了个泛型的 Realm 对象工厂，类型约束是 `T: Object`，里面直接 `T()` 想创建具体的 model，结果运行时抛 `RLMException` 说 `Object type 'Object' not persisted in Realm`。感觉它好像没有按实际传进来的子类去初始化；这种场景能不能正常 new 出那个 RealmSwift `Object` 子类啊？

当泛型参数满足 `T: Object` 时，`T()` 应该返回实际传入的具体子类实例，并保留该子类的默认属性值；这个无参构造也应在 Swift 类型系统里保持可用，调用时不应再落到 Realm 的运行时异常。

具体实现方式、内部校验位置、是否复用现有辅助逻辑或中间类型都由实现者自行决定；只要外部可观察到的构造结果与初始化契约符合上述行为即可。
