(function(w,d) {
	w.addEventListener('load', function(evt) {
		setupDatapoints();
	}, false);

	function setupDatapoints() {
		var datapoints=d.querySelectorAll('.datapoint');

		for (var i=0;i<datapoints.length;i++) {
			datapoints[i].dp=new Datapoint(datapoints[i]);
			datapoints[i].dp.register();
		}
	}

	function Datapoint(element) {
		var self = this;
		this.element = element;		// holds the current element
		this.data = null;		// holds data
		this.popup = null;		// popup Element

		// popup offsets, if they're right below the cursor it goes flickery, I could
		// use cursor-events but I can't be arsed
		this.offsetX = 10;
		this.offsetY = 10;

		this.register=function() {
			this.data=JSON.parse(this.element.querySelector('desc').innerHTML);
	
			this.element.addEventListener('mouseenter', this.show, false);
			this.element.addEventListener('mouseleave', this.hide, false);

			this.popup=d.createElement('div');

			var date=d.createElement('span');
			date.innerHTML=this.data.date;

			var value=d.createElement('span');
			value.innerHTML=this.data.value;

			this.popup.appendChild(date);
			this.popup.appendChild(value);

			this.popup.className='datapoint-popup';
			d.querySelector('body').appendChild(this.popup);
		}

		/* callbacks */
		this.show=function(evt) {
			self.popup.style.visibility='visible';
			self.popup.style.left=(evt.clientX + self.offsetX) + "px";
			self.popup.style.top=(evt.clientY + self.offsetY) + "px";
		}

		this.hide=function(evt) {
			self.popup.style.visibility='hidden';
		}
	}
})(window,document);
