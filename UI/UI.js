function setTouchListener(_id, _cmd) {
	document.getElementById(_id)
		.addEventListener(
			'touchstart',
			function(e){
				location.href =
					'app://' + _cmd;
			},
			false
	)
}

function updatePlaybackState(_state) {
	let elem = document.getElementById('btnPlayPause')
	elem.className = 'PlaybackState-' + _state;
	elem.textContent = _state;
}

function setImageWithBase64(_id, _base64String) {
	try {
		document.getElementById(_id).src = 'data:image/png;base64,' + _base64String;
	} catch (e) {
		alert(e);
	}
}

function setNowPlayingSongArtwork(_base64String) {
	setImageWithBase64('NowPlayingSongArtwork', _base64String);
}

