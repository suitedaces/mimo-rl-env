### channeldb: TestOutgoingPaymentsMigration is not self-contained against future migrations

While working on a follow-up migration in `channeldb` I noticed that `TestOutgoingPaymentsMigration` (the test for migration #9) breaks as soon as anything downstream touches the payment / route decoding path — even if I don't touch migration 9 itself.

The reason becomes obvious if you look at what the test does: it writes payment data in the on-disk format that existed at the time migration 9 was created, runs the migration, and then reads the payments back out via the regular `FetchPayments` code path to assert that things look right. But `FetchPayments` (and the deserializers it calls — for `PaymentAttemptInfo`, `Route`, `Hop`, …) keeps evolving with later migrations. So the moment migration 10+ changes that decoding path, the migration 9 test is effectively trying to read "migration 9 era" bytes with a "future" decoder, and it fails.

The serialization side of migration 9 was already pinned down for exactly this reason — there's a `serializePaymentAttemptInfoMigration9` (and matching route/hop variants) that the test uses so that the bytes it puts into the DB are stable regardless of how the live serializers evolve. But the read-back side has no equivalent: the test still goes through the current `FetchPayments`, so we only get half the isolation.

Migration tests should be frozen in time — once migration N is shipped, its test should keep passing forever, no matter how many later migrations change the surrounding code. Right now that property doesn't hold for migration 9 on the read side. Could we pin the read path for this test the same way the write path is already pinned?
