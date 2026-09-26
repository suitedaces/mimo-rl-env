BUG: `Style` index name row does not label column class
- [x] I have checked that this issue has not already been reported.

- [x] I have confirmed this bug exists on the latest version of pandas.

- [x] (optional) I have confirmed this bug exists on the master branch of pandas.

---

The `Styler` ignores column class on the `index_name` row and just inputs `blank`, which is a pain for controlling `table_styles` using column selectors.

```
df3 = pd.DataFrame(0, index=['a'], columns=['A','B'])
df3.index.name = 'foo'
print(df3.style.render())
```

```
<style type="text/css">
</style>
<table id="T_a6821_">
  <thead>
    <tr>
      <th class="blank level0" ></th>
      <th class="col_heading level0 col0" >A</th>
      <th class="col_heading level0 col1" >B</th>
    </tr>
    <tr>
      <th class="index_name level0" >foo</th>
      <th class="blank" ></th>
      <th class="blank" ></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th id="T_a6821_level0_row0" class="row_heading level0 row0" >a</th>
      <td id="T_a6821_row0_col0" class="data row0 col0" >0</td>
      <td id="T_a6821_row0_col1" class="data row0 col1" >0</td>
    </tr>
  </tbody>
</table>
```

Internal mechanics should be fixed to add the col index class.
