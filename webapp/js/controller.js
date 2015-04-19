var myApp = angular.module('zipapp',[]);

myApp.controller('zipController', ['$scope','$http', function($scope,$http) {
  $scope.query = '';
  $scope.table_data = '';
      $scope.search_zipcode = function(){
        if($scope.query=="")
        {
          alert("Query Cannot Be Blank");
          return;
        }

        $('.loading').show();

        $http({url:'http://54.69.200.1/api/v1/search?query='+$scope.query,method:'GET'}).success(function(data){

                  $scope.table_data = data;
            $('#example').DataTable();
            $('.loading').hide();

          }).error(function(){
            $('.loading').hide();
              $scope.table_data = '';
            $('#example').DataTable({ "language": {
              "emptyTable": "No Search Results To Show."
            }});
          });
  };

}]);