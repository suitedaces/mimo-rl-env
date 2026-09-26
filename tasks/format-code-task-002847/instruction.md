# Add a Baidu ERNIE (文心一言) LLM provider

langchaingo ships providers for OpenAI, Anthropic, Cohere, etc. under the LLM
package. Add a new provider for Baidu's ERNIE / 文心一言 large language model
platform (Wenxin Workshop / Qianfan API) so it can be used like any other
langchaingo model.

Expose it as a package importable at `github.com/tmc/langchaingo/llms/ernie`
whose constructor `New(opts ...Option) (*LLM, error)` returns a value that
implements the standard `llms.LLM` interface (`Call` and `Generate`). It must
talk to the real Baidu HTTP API, but allow callers to inject a custom
`*http.Client` so the transport can be controlled.

## Authentication

The Baidu API is reached with a short‑lived **access token**. Credentials may be
supplied three ways, resolved in this order:

- An access token passed directly via `WithAccessToken(token)`.
- An API key / secret key pair passed via `WithAKSK(apiKey, secretKey)`.
- The environment variables `ERNIE_API_KEY` and `ERNIE_SECRET_KEY`, used as the
  key/secret pair when not given explicitly.

Rules:

- If, after resolution, there is **neither** an access token **nor** a complete
  key+secret pair, `New` must return a non‑nil error and not return a usable
  client.
- When only a key/secret pair is available (no direct access token), the client
  must exchange them for an access token by issuing a POST to the OAuth token
  endpoint `https://aip.baidubce.com/oauth/2.0/token` with query parameters
  `grant_type=client_credentials`, `client_id=<apiKey>`,
  `client_secret=<secretKey>`. The `access_token` from that JSON response is then
  used for subsequent API calls. If supplying an access token directly, no token
  request is made.

## Completions

`Generate` (and `Call`, which is the single‑prompt convenience wrapper) must POST
to the chat completion endpoint:

```
https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/<model-path>?access_token=<token>
```

The JSON request body carries the prompt as a single message
`{"role":"user","content":"<prompt>"}` together with `temperature`, `top_p` and
`penalty_score` taken from the langchaingo call options (temperature, top‑p and
repetition penalty respectively). The response body contains a `result` string;
that string is the generated text. `Generate` returns one generation per input
prompt, in order; `Call` returns the text of the first generation. A non‑2xx HTTP
response must be reported as an error.

### Model selection

The `<model-path>` segment depends on the selected model name. The model is taken
from `WithModelName(name)` if set, otherwise from the per‑call `llms.WithModel`
option, otherwise the default. The mapping is:

| model name         | path          |
|--------------------|---------------|
| `ERNIE-Bot`        | `completions` |
| `ERNIE-Bot-turbo`  | `eb-instant`  |
| `BLOOMZ-7B`        | `bloomz_7b1`  |
| `Llama-2-7b-chat`  | `llama_2_7b`  |
| `Llama-2-13b-chat` | `llama_2_13b` |
| `Llama-2-70b-chat` | `llama_2_70b` |

When no model is selected, or the name is not one of the above, the default path
`completions` is used.

### Streaming

When a streaming callback is supplied through `llms.WithStreamingFunc`, the
request must be made in streaming mode (the request body sets the stream flag),
and the response is read as server‑sent‑event lines, each prefixed with
`data: ` and followed by a JSON object with a `result` field. The callback is
invoked once per chunk with that chunk's `result` bytes, and the final returned
text is the concatenation of all chunks' results.

## Embeddings

Add a method `CreateEmbedding(ctx context.Context, texts []string) ([][]float64, error)`
that POSTs to the embedding endpoint:

```
https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/embeddings/embedding-v1?access_token=<token>
```

with a JSON body of the form `{"input": [<texts>]}`. The response body has a
`data` array whose entries each carry an `embedding` vector (and an `index`), and
may carry a top‑level `error_code`/`error_msg`. The method returns one embedding
vector per input text, in input order. If the API response carries a non‑zero
`error_code`, the method must return an error instead of embeddings.
