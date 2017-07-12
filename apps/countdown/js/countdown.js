(function(w,d) {
	"use strict";

	var busy=false;
	var target=null;

	w.addEventListener('load', onload, false);

	function onload() {
		var tspan=d.querySelector('#countdown #target');

		if (tspan != null)
			target=parseInt(tspan.innerHTML);

		if (target != null)
			setInterval(tick, 1000);
	}

	function tick() {
		if (busy)
			return;

		var xhr = new XMLHttpRequest();
		xhr.addEventListener('load', updateCountdown);
		xhr.open('GET', '/countdown/ajax/' + target);
		xhr.send();
	}

	function updateCountdown() {
		busy=false;

		var data=JSON.parse(this.responseText);

		var current=d.querySelector('#countdown #current');
		var remaining=d.querySelector('#countdown #remaining');

		current.innerHTML=data.current;
		remaining.innerHTML=data.target - data.current;
		
	}
})(window,document);


