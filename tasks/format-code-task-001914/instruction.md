[Rewriter] Cannot create an op with a name
Currently, when applying a rewrite rule, I cannot pass a name with the replacement op.
#### Minimal example
```python
import onnx
import onnx_ir as ir

from onnxscript.rewriter import pattern, rewrite


def custom_rewrite(model):
    def target_pattern(op, x):
        return op.Relu(x, _outputs=["relu"])

    def replacement_pattern(op, x, relu):
        ir_node = relu.producer()
        return op.Clip(x, name=ir_node.name)
       """Workaround
        out = op.Clip(x)
        clip_node = out.producer()
        clip_node.name = ir_node.name
        """

    rules = [pattern.RewriteRule(target_pattern, replacement_pattern)]
    model = rewrite(model, rules)
    return model


ir_model = ir.from_onnx_text("""
            < ir_version: 10, opset_import: ["" : 20] >
            test_model (float[N, 16, 16] X) => (float [N, ?, ?] Y)
            {
                Y = Relu(X)
            }
        """)
ir_model.graph[0].name = "relu_1"
ir_model = custom_rewrite(ir_model)
proto = ir.to_proto(ir_model)
onnx.save(proto, "tmp.onnx")
```
Doing this will result in node with attribute **name** 

![Image](https://github.com/user-attachments/assets/5a67eab9-10dd-48fc-9c9a-4a2871079b69)

### Potential fix
Other op parameters (see https://github.com/onnx/ir-py/blob/c7879f7bab341e27ca19ab31b084b449f8a82378/src/onnx_ir/_tape.py#L74) should be extracted just like it is already done for `domain, version, and outputs` https://github.com/microsoft/onnxscript/blob/87baf8ff4b8ef7e75e17bb9383398a10dba8bd91/onnxscript/ir/_tape.py#L25

I can submit a PR if you find the fix convenient
