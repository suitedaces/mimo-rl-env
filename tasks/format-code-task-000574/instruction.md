### Block fetcher still accepts blocks at or below finalized height

After Fast Finality was enabled on BSC, blocks at or below the finalized height are deterministically final — they cannot be reorged out. However, the block fetcher in `eth/fetcher` still accepts propagated blocks within the legacy side-chain window (roughly `[CurrentBlock - maxUncleDist, CurrentBlock + maxQueueDist]`, i.e. about `[head-11, head+32]`).

This means peers can announce / broadcast blocks whose number is `<=` our current finalized height, and the fetcher will happily queue and try to import them. Those blocks will never become part of the canonical chain, so the work spent announcing, queuing, and verifying them is wasted, and they show up as noise in fetcher debug logs on a node that already has finality information available locally (`chain.CurrentFinalBlock()`).

Could the block fetcher be made aware of the local finalized height and skip any propagated block / announcement whose number is at or below it? On BSC with finality enabled there is simply no reason to fetch them.
