# Message Passing API
| Parameter | Description |
| --------- | ----------- |
| `product_changed/{name}` | Signals that the product has changed. Its `coords`, `name`, and `time` must be sent so that the view can render the change. If the time changed, set `time_change` to `True` to improve performance |
| `changing_time` | UI-generated event telling all products to change their time. The only parameter is the `time` |
| `product_changing` | UI-generated event telling a single product to change a specific stat or stats. `name` is required, as is at least one of `size` and `performance`. Passing `None` for `time` changes a stat at the product's current time. |
