Found in https://github.com/flutter/flutter/pull/129381

The flutter gold check only runs on PRs that are running golden file tests - or so we thought. 🕵️ 

The way the check determines this is by checking the already running checks on a PR. If the framework test shards or web test shards are running, flutter gold adds itself to the queue:

https://github.com/flutter/cocoon/blob/26515729f2afdf0a77b03c9bdcd06824cc4b0436/app_dart/lib/src/request_handlers/push_gold_status_to_github.dart#L122

In https://github.com/flutter/flutter/pull/129381, we found that the API docs are not accounted for by this. The API docs tests run on a different shard (I think misc?) and so flutter gold was not triggered.

This would have broken the tree if @HansMuller had not known a golden file change was expected. The PR could have landed, the new image would have shown up in post submit as untriaged, and the tree would go red.
