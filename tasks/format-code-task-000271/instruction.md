[ts-interface-generator ] Return type for the method "remove" for aggregation of cardinality 0 .. n does not match runtime behaviour
**Describe the bug**
I was just having a look into OpenUI5 with TypeScript for a private project. I played around with custom controls.
I defined a custom aggreagation with `multiple: true`:
```ts
import Control from "sap/ui/core/Control";
import type { MetadataOptions } from "sap/ui/core/Element";
import RenderManager from "sap/ui/core/RenderManager";

/**
 * @namespace ui5.typescript.helloworld.control
 */
export default class MyControl extends Control {
    // The following three lines were generated and should remain as-is to make TypeScript aware of the constructor signatures
    constructor(idOrSettings?: string | $MyControlSettings);
    constructor(id?: string, settings?: $MyControlSettings);
    constructor(id?: string, settings?: $MyControlSettings) { super(id, settings); }
 
	static readonly metadata: MetadataOptions = {
		properties: {
			"text": "string"
		},
        aggregations: {
            "columns": { type: "sap.ui.core.Control", multiple: true},
        }
	};

	static renderer = {
		apiVersion: 2,
		render: function (rm: RenderManager, control: MyControl): void {
			rm.openStart("div", control);
			rm.openEnd();
			rm.text(control.getText());
			rm.close("div");
		}
	};

	onclick = function() {
		alert("Hello World!");
	}
}
```

This leads to the following generated interface:
```ts
export default interface MyControl {

        // property: text
        getText(): string;
        setText(text: string): this;

        // aggregation: columns
        getColumns(): Control[];
        addColumn(columns: Control): this;
        insertColumn(columns: Control, index: number): this;
        removeColumn(columns: number | string | Control): this;
        removeAllColumns(): Control[];
        indexOfColumn(columns: Control): number;
        destroyColumns(): this;
    }
}
```

Nevertheless during runtime the method `insertColumn` and ``removeColumn` return the inserted or removed element:
![image](https://github.com/user-attachments/assets/7646e89c-f25a-40b9-9689-0b096e900505)

**Expected behavior**
The interface generator should generate the return type according to runtime behaviour:
```
 insertColumn(columns: Control, index: number): Control | undefined;
removeColumn(columns: number | string | myColumn): Control | undefined;
```

I checked with other aggregations with the cardinality `0 .. n`. They have all the return type `Type of Aggregation |null` (see `sap.ui.table.Table` or `sap.m.Page`).

**Additional context**
I used version `0.8.3` of the module `@ui5/ts-interface-generator` and the following OpenUI5 version:
![image](https://github.com/user-attachments/assets/8c380f23-a931-481a-b1b1-24e2efd11cbf)
