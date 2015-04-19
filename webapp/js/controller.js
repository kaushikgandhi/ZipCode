var myApp = angular.module('zipapp',[]);

myApp.controller('zipController', ['$scope','$http', function($scope,$http) {
  $scope.query = '';
  $scope.table_data = '';
      $scope.search_zipcode = function(){
  	$http({url:'http://54.69.200.1/api/v1/search?query='+$scope.query,method:'GET'}).success(function(data){

  			$scope.table_data = data;
  			
  	}).error(function(){
  		$scope.table_data = '';
  	});
  };

}]);