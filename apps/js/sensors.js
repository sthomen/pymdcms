(function(w,d) {
	w.addEventListener('load', function(evt) {
		setupDatapoints();
		w.setInterval(function(evt) {
			update();
		}, 900000);	/* 15 minutes */
	}, false);

	function update() {
		ajax('GET', [w.location.href, "ajax"].join("/"), function (evt) {
			var data=JSON.parse(this.responseText);
			for (var key in data) {
				var element=d.querySelector('.value-' + data[key][1]);
				element.innerHTML=(parseInt(data[key][3])/100);

				updateGraph(key);
			}
		});
	}

	function updateGraph(index) {
		ajax('GET', [w.location.href, "graph", index].join("/"), function (evt) {
			var data=this.responseText;
			var element=d.querySelector('.graph-' + index);
			element.innerHTML=data;
		});
	}

	function setupDatapoints() {
		var datapoints=d.querySelectorAll('.datapoint');
		var dp=new Datapopup();
		dp.render();

		for (var i=0;i<datapoints.length;i++) {
			if (!datapoints[i].hasOwnProperty('dp')) {
				dp.register(datapoints[i]);
			}
		}
	}

	function Datapopup() {
		var self = this;

		this.popup = null;
		this.date = "Unknown";
		this.value = "&#8734;";

		// popup offsets, if they're right below the cursor it goes flickery, I could
		// use cursor-events but I can't be arsed
		this.offsetX = 10;
		this.offsetY = 10;

		this.render=function() {
			this.popup=d.createElement('div');
			this.date=d.createElement('span');
			this.value=d.createElement('span');

			this.popup.appendChild(this.date);
			this.popup.appendChild(this.value);

			this.popup.className='datapoint-popup';
			d.querySelector('body').appendChild(this.popup);
		}

		this.register=function(element) {
			element.addEventListener('mouseenter', this.show, false);
			element.addEventListener('mouseleave', this.hide, false);
		}


		/* callbacks */
		this.show=function(evt) {
			var scrollTop=d.documentElement.scrollTop || d.body.scrollTop;
			var scrollLeft=d.documentElement.scrollLeft || d.body.scrollLeft;

			var data=JSON.parse(evt.target.querySelector('desc').innerHTML);

			self.date.innerHTML=data.date;
			self.value.innerHTML=data.value;

			self.popup.style.left=(scrollLeft + evt.clientX + self.offsetX) + "px";
			self.popup.style.top=(scrollTop + evt.clientY + self.offsetY) + "px";
			self.popup.style.visibility='visible';
		}

		this.hide=function(evt) {
			self.popup.style.visibility='hidden';
		}
	}

	function ajax(method, url, onload, params) {
		if (!url)
			return;

		var req=new XMLHttpRequest();

		if (onload)
			req.onload=onload;

		req.open(method, url, true);
		req.send(params);
	}
})(window,document);
