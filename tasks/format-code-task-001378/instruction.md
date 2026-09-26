我用 gopass fsck 检查的时候，发现挂了好几个 mount 之后体验有点糟：跑起来啥也不输出，不知道还要等多久；输出的行也分不清是哪个 store 出来的，全混在一起；更难受的是只要某一个 sub store 报错就整个中断了，剩下的都不检查了，我得一个个排查完再重跑。还有就是发现空目录只是 WARNING 一下让我自己去清，能不能顺手帮我删了？要是能加个进度提示、每行带上 store 别名、出错也别直接 abort 把剩下的都跑完，就完美了。

Expected outcomes:
- Running `gopass fsck` should make it clear that store integrity checking has started before the longer checks run.
- While fsck is checking entries across stores, users should see progress indicating how many objects have been checked out of the total work to do; non-visible/hidden output modes should not leak progress output.
- Output produced while checking a mounted store should be attributable to that store, using the store alias as a visible line prefix.
- Empty folders found during fsck should be reported as being removed and should actually be removed from disk.
- If one mounted store fails fsck, the command should report that store’s failure, continue checking the remaining mounted stores and the main store, and return an error that preserves all fsck failures instead of only the first one.
- If all stores pass fsck, the command should still complete successfully.

Implementation notes:
- The exact progress mechanism, aggregation type, traversal order, and placement of checks are implementation details as long as the user-visible behavior above is preserved.
- Avoid coupling the solution to a single mount count or example store name; the behavior should work for multiple mounted stores and the main store.
- Keep existing fsck behavior intact except where it conflicts with progress reporting, per-store attribution, empty-folder cleanup, or continuing after per-store failures.
