var app = angular.module('myApp', []); 
	
app.config(function($routeProvider) {
	$routeProvider.when('/index/', {templateUrl: 'home'});
});
			
app.controller('MainCtrl', function($scope, $route) {
	$scope.instance = null;

	$scope.stop_instance_by_id = function(id) {
		console.log('stopping instance:', id)
	}
});


