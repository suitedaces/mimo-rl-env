我在写 ecocredit 模块的 genesis 测试，发现一件挺怪的事：我故意往 Params 里塞了个明显非法的 bech32 地址到 AllowedClassCreators，再调 GenesisState.Validate()，居然过了，没报任何错。同样的，我 ClassInfo 里写了个 Params.CreditTypes 里根本没声明过的 credit type 缩写，Validate 也照样放行，感觉上线之后 InitGenesis 才会爆炸。是不是 genesis 校验这块压根没去校 Params 本身？能不能让 Validate 把 Params 这些字段也一起查了，顺便也确认下 ClassInfo 引用的 CreditType 在 Params 里是真的存在、对得上的？

Expected outcomes:
- Params validation: ecocredit Params should expose a Validate() error method that validates Params fields according to the module’s existing parameter validation rules; it should return an error when an invalid parameter value is present and nil when all parameter values are valid.
- Genesis parameter validation: GenesisState.Validate() should reject genesis states whose Params contain invalid values, including invalid allowed class creator addresses or invalid credit type definitions.
- Credit type references from class info: GenesisState.Validate() should reject any ClassInfo whose CreditType is not declared by the Params credit type configuration.
- Credit type consistency from class info: GenesisState.Validate() should reject any ClassInfo whose CreditType declaration does not match the corresponding declaration in Params.
- Error reporting: invalid allowed class creator addresses should be reported with invalid-address semantics and context indicating that the creator address is invalid; unknown credit type declarations and mismatched credit type definitions should produce errors that make those respective conditions observable to callers.

Implementation notes:
- The exact control flow, helper structure, and lookup data structures are up to the implementer.
- Reuse the module’s existing validation conventions and public error semantics where applicable.
- The change should be observable through public validation calls rather than by requiring any particular private helper or internal organization.
