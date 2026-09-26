Display sorting icons only if sort is active
via @mtanco 

Our current Wave table tries to explicitly show users which columns are sortable by displaying an arrow icon. However, this may conflict with assumption that it represents the sort direction the data is sorted by default (which is not true).

According to both [aggrid](https://www.ag-grid.com/example.php) and [material design](https://material.angular.io/components/table/overview#sorting) it seems like the general accepted UX is to simply click the col, assume it's sortable and display sorting arrow only after the sort is performed in order to depict currently applied sort.
