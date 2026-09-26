## Add an opt-in retry middleware for Bot API requests

Individual Bot API calls currently have no reusable retry policy, even though aiogram already has a request-middleware pipeline and backoff utilities. Add a public `RetryRequestMiddleware` importable from `aiogram.client.session.middlewares.retry` so applications can register retry behavior on a session without changing `Bot` calls or a custom session implementation.

The middleware constructor must accept `max_attempts` (default `3`), an optional `BackoffConfig`, and an optional asynchronous `sleep` callable. Omitting the backoff configuration must still produce a usable middleware; a supplied configuration controls the delay sequence. The supplied sleep callable receives the chosen delay in seconds and is awaited. `max_attempts` is the total number of downstream calls, including the initial immediate call, and values less than one must be rejected with `ValueError`.

A successful downstream result must be returned unchanged after one call and without sleeping. Retry only failures represented by `TelegramNetworkError`, `TelegramServerError` (including its subclasses), or `TelegramRetryAfter`. `TelegramEntityTooLarge` is permanent despite inheriting from `TelegramNetworkError` and must not be retried. Every other exception, including other Telegram API errors and application exceptions, must propagate unchanged after the first call.

Between retryable failures, use successive delays from a fresh `Backoff` based on the configured `BackoffConfig`. For `TelegramRetryAfter`, wait for the greater of that backoff delay and the exception's `retry_after` value. Never sleep after the last permitted attempt. If all attempts fail, re-raise the exact exception from the last attempt. Every attempt must invoke the downstream callable with the same `bot` and `method` objects received by the middleware.

One middleware instance may be reused for sequential and concurrent requests. Each invocation must start its own backoff sequence, and concurrent invocations must not share counters, delays, results, or errors. Cancellation from either the downstream request or the sleep callable must propagate immediately, with no further attempt.

Preserve normal `RequestMiddlewareManager` composition: retrying re-enters middleware registered downstream of the retry middleware for every attempt, while middleware registered upstream surrounds the whole retry operation and runs once.
