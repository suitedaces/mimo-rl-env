Vertica's `COPY` grammar currently handles ordinary file, `LOCAL`, and `VERTICA` sources, input formats, column options, and load options, but it rejects the UDx and execution-node clauses that are needed for production loads. Extend the public Vertica dialect parser so both direct `COPY` statements and the `COPY` clause of `CREATE EXTERNAL TABLE ... AS COPY` accept these options after the `FROM` source (and any input format):

- `WITH PARSER <parser UDx>`;
- `WITH FILTER <filter UDx>`; and
- `ON <node name>` or `ON ANY NODE`.

The UDx references must support the parenthesized call form used by Vertica. A statement may combine parser, filter, and node options, and those options must coexist with the existing quoted-file source, `LOCAL` plus `NATIVE VARCHAR`, and `ORC` input forms. Existing column lists and `COLUMN OPTION` clauses, such as a `FILLER VARCHAR(...)` definition, must remain usable. Existing COPY load options such as `REJECTMAX` and `TRAILING NULLCOLS` must continue to parse when combined with the new clauses.

Keep the option placement unambiguous: these extensions belong after the source, so a parser or filter clause before `FROM` must remain unparsable. Successful statements must consume their complete input without parse violations or an `unparsable` segment, and the existing Vertica COPY fixture behavior must remain unchanged.
