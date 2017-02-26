let chatApp = angular.module('chat',[]).config(function($interpolateProvider){
    $interpolateProvider.startSymbol('||').endSymbol('||');
});

chatApp.controller('AppController', ['$scope', '$http', function($scope, $http){

	var socket;

	$scope.user = {
		name: 'apollonin' 
	};

	$scope.messages = [];

	$scope.send = function(){

		socket.emit('chat', JSON.stringify({
			name: $scope.user.name,
			message: $scope.message	
		}));

		$scope.message = '';
	}

	function start_socket(){

		// Create and connect socket
    	socket = io.connect("", {'host': 'localhost', 'port': 9999});

    	socket.emit('login', $scope.user.name);

    	socket.on('chat', function(message) {
	        $scope.messages.push(JSON.parse(message));

	        $scope.$apply(); 

	        scrollChatToBottom();
	    });
	}

	function getHistory(){
		$http.get('http://localhost:8081/history')
			.then(function(response){
				angular.forEach(response.data.messages, function(message){
	    			$scope.messages.push(message);
	    		 });

				scrollChatToBottom();
			});
	}

	function scrollChatToBottom(){
		var chat_div = document.getElementById("chat_div");
		chat_div.scrollTop = chat_div.scrollHeight;
	}

	getHistory();
	start_socket();

}]);