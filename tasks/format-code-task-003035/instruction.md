This logic will cause a failing txn if `self.token.balanceOf(msg.sender) > self.depositLimit - self._totalAssets()`:
https://github.com/iearn-finance/yearn-vaults/blob/958d380c61c993abbfaa5d3c4191feb204c14de2/contracts/Vault.vy#L608-L609
