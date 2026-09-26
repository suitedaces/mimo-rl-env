Passing a controller constructor
In the current system, and if i understand it, to use a custom modal, you have to pass a controller already created : 

``` javascript
app.controler("SomeController", function($scope, close) {
 $scope.dismissModal = function(result) {
    close(result, 200); 
 };
});
```

``` javascript
ModalService.showModal({
  templateUrl: "some/template.html",
  controller: "SomeController"
});
```

I can't find a way to do this without changing the code : 

``` javascript
ModalService.showModal({
  templateUrl: "some/template.html",
  controller: function($scope, close) {
      $scope.dismissModal = function(result) {
         close(result, 200); 
      };
  }
});
```

Do you plan to add this feature ?
