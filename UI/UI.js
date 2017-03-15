function setTouchListener(_id, _cmd) {
	document.getElementById(_id)
		.addEventListener(
			'touchstart',
			function(e){
				location.href =
					'app://' + _cmd;
			},
			false
	);
}

function updatePlaybackState(state) {
	document.getElementById('btnPlayPause').className
		= 'PlaybackState-' + state;
}
