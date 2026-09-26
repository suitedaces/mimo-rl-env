## Attribute `xml` tags in generated structs are missing namespace info

I'm generating Go bindings for a WSDL/XSD that uses XML namespaces (in my case the EPCIS schema, target namespace `urn:epcglobal:xsd:1`). For element-backed struct types, the generated code correctly carries the schema's target namespace via `XMLName`:

```go
type Document struct {
    XMLName xml.Name `xml:"urn:epcglobal:xsd:1 EPCISDocumentType"`
    ...
}
```

But on the same types, attribute fields are emitted with no namespace info at all:

```go
SchemaVersion float64          `xml:"schemaVersion,attr,omitempty" json:"schemaVersion,omitempty"`
CreationDate  soap.XSDDateTime `xml:"creationDate,attr,omitempty"  json:"creationDate,omitempty"`
```

This is inconsistent — `XMLName` knows the type lives in `urn:epcglobal:xsd:1`, but the attributes don't. It also breaks round-tripping with real XML where the attributes are namespace-qualified: those attributes don't match the generated fields on unmarshal (they silently get dropped), and on marshal nothing tells `encoding/xml` to emit them under the right namespace either.

The same problem shows up for nested types whose attributes belong to a different schema. For example, types under the SBDH schema (`http://www.unece.org/cefact/namespaces/StandardBusinessDocumentHeader`) generate attributes with just the local name, even though those attributes really are in that namespace.

It would be great if attribute tags picked up the target namespace of the schema they were declared in, the same way element `XMLName` already does. You can reproduce this with the `fixtures/epcis` WSDL.
