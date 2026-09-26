# Problem Statement

我现在有一批肽/蛋白的 amino acid sequence/FASTA 字符串，想在 sklearn Pipeline 里像用 MolFromSmilesTransformer 那样直接转成 RDKit Mol，但 skfp.preprocessing 里好像没有对应的入口；能不能加一个这种序列转 Mol 的 transformer，最好也能顺手控制 RDKit 解析时的 sanitize 之类选项？

# Expected Outcomes

- 新增公开的 `MolFromAminoseqTransformer`，可从 `skfp.preprocessing` 和 `skfp.preprocessing.input_output` 导入、实例化，并作为 sklearn 风格 transformer 使用。
- `MolFromAminoseqTransformer.transform` 接收一批 amino acid sequence 或 FASTA 字符串，并返回与输入顺序一一对应的 RDKit `Mol` 对象。
- `MolFromAminoseqTransformer` 支持构造参数 `sanitize` 和 `flavor`，用于控制 RDKit 解析 amino acid/FASTA 输入时的相关行为；`flavor` 应接受 RDKit 支持的整数取值范围并拒绝非法取值。
- `MolFromAminoseqTransformer.transform` 应对 batch 输入做字符串类型校验，包含非字符串元素的输入应被拒绝，而不是被静默转换或产生不可预测结果。
- 预处理模块文档的 molecular format 读写列表应包含 `MolFromAminoseqTransformer`，使用户能从 preprocessing 文档发现该入口。

# Implementation Notes

- 具体文件组织、内部 helper、校验位置和并行实现方式由实现者决定，但新增 transformer 应与项目中现有 preprocessing transformer 的公开 API、参数处理和 sklearn Pipeline 兼容性保持一致。
- 解析结果应以外部可观察行为为准：输入数量、输出顺序、RDKit `Mol` 类型、参数效果和错误处理需要稳定；内部调用路径或私有符号名称不作要求。
