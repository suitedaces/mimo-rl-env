Batch requests are not replacing token placeholders in request URLs, resulting in bad payloads
@shemogumbe 
To reproduce:

```python
# Use the request builder to generate a regular
# request to /me
user_request = graph_client.me.to_get_request_information()

today = datetime.today()
tomorrow = today + timedelta(days=1)

# Use the request builder to generate a regular
# request to /me/calendarview?startDateTime="start"&endDateTime="end"
query_params = CalendarViewRequestBuilder.CalendarViewRequestBuilderGetQueryParameters(
    start_date_time=today.isoformat(timespec='seconds'),
    end_date_time=tomorrow.isoformat(timespec='seconds')
)

config = CalendarViewRequestBuilder.CalendarViewRequestBuilderGetRequestConfiguration(
    query_parameters=query_params
)
events_request = graph_client.me.calendar_view.to_get_request_information(config)

# Build the batch
user_batch_item = BatchRequestItem(request_information=user_request)
events_batch_item = BatchRequestItem(request_information=events_request)
batch_request_content = BatchRequestContentCollection()
batch_request_content.add_batch_request_item(user_batch_item)
batch_request_content.add_batch_request_item(events_batch_item)

# Create batch request builder (temporary?)
batch_request_builder = BatchRequestBuilder(request_adapter=graph_client.request_adapter)

batch_response = await batch_request_builder.post(batch_request_content)
```

This results in the following payload going over the wire. Note the `users/me-token-to-replace` in the URLs - this should have been updated to `/me`.

```json
[
  {
    "id": "1c4593e4-b600-4945-85bf-d58f552ae414",
    "url": "https://graph.microsoft.com/v1.0/users/me-token-to-replace",
    "depends_on": []
  },
  {
    "id": "e4bb3047-d4eb-4ed6-b051-7f21a13f3f5f",
    "url": "https://graph.microsoft.com/v1.0/users/me-token-to-replace/calendarView?endDateTime=2024-09-26T14%3A12%3A59&startDateTime=2024-09-25T14%3A12%3A59",
    "depends_on": []
  }
]
```

Similar issue was in the Go SDK: https://github.com/microsoftgraph/msgraph-sdk-go-core/issues/179.
