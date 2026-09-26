We need to tighten up handling of pseudo-header fields.
We have a number of failures in h2spec caused by being overly lenient with pseudo-header fields. We need to resolve the following problems:


- [x] When we receive a HEADERS frame that contains a pseudo-header field defined for response only (that is, `:status`), we MUST respond with a stream error of type PROTOCOL_ERROR. Same policing needs to be applied to sending. (#514)
- [x] When we receive a HEADERS frame with an empty `:path` pseudo-header field, we MUST respond with a stream error of type PROTOCOL_ERROR. Same policing needs to be applied to sending. (#513)
- [x] When we receive a HEADERS frame that omits the `:method` pseudo-header field we MUST respond with a stream error of type PROTOCOL_ERROR. The same policing needs to be applied to sending. (#513)
- [x] When we receive a HEADERS frame that omits the `:scheme` pseudo-header field we MUST respond with a stream error of type PROTOCOL_ERROR. The same policing needs to be applied to sending. (#513)
- [x] When we receive a HEADERS frame that omits the `:path` pseudo-header field we MUST respond with a stream error of type PROTOCOL_ERROR. The same policing needs to be applied to sending. (#513)

All of these say stream error, but hyper-h2 has generally treated errors like this as connection errors, and so we may well continue down that route here.
