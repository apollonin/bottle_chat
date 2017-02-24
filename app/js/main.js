let chatApp = angular.module('chat',[]);

chatApp.controller('AppController', ['$scope', function($scope){

	var ws;

	$scope.user = {
		name: 'apollonin' 
	};

	$scope.messages = [];

	$scope.send = function(){
		ws.send($scope.message);

		$scope.message = '';
	}

	function start(){
		ws = new WebSocket("ws://localhost:8081/websocket");
	    ws.onopen = function() {
	        ws.send('getHistory');
	    };
	    ws.onmessage = function (evt) {

	    	$scope.messages.push(evt.data);
			$scope.$apply(); 

			//scroll to bottom
			var chat_div = document.getElementById("chat_div");
			chat_div.scrollTop = chat_div.scrollHeight;
	    };
	};

	start();


}]);