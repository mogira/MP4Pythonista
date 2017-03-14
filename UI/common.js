(function(){
	document.addEventListener(
		'touchmove',
		function(e){
			e.preventDefault();
		},
		false
	);
	let lastTouchEnd = 0;
	document.addEventListener(
		'touchend',
		function(e){
			const now   = window.performance.now();
			if (now-lastTouchEnd<=500)
				e.preventDefault();
			lastTouchEnd = now;
		},
		false
	);
})();

function setTouchListener(cmd_name) {
	document.getElementById(cmd_name)
		.addEventListener(
			'touchstart',
			function(e){
				location.href =
					'app://' + cmd_name;
			},
			false
	);
}
