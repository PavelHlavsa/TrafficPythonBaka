const ContinuousVisualization = function(width,height, context) {


	this.createImage =function (shape, scale){
		var img = new Image();
		img.src = "local/".concat(shape);
		if (scale === undefined) {
			var scale = 1
		};
		img.onload = function() {
			img.width*=scale
			img.height*=scale
			context.beginPath();
			context.translate(x*width+0.5*img.width,y*height+0.5*img.height);
			context.rotate(dir * Math.PI / 180);
			context.drawImage(img,-img.width*0.5, -img.height*0.5, img.width, img.height);
			context.rotate(-(dir) * Math.PI / 180);
			context.translate(-x*width-0.5*img.width,-y*height-0.5*img.height);
		}
		return img
	};

	this.draw = function(objects) {
		
		
		for (var i in objects) {
			var p = objects[i];
			if (p.Shape == "rect"){
				this.drawRectange(p.x, p.y, p.w, p.h, p.Color,p.dir);
			}
			else if (p.Shape == "rect2"){
				this.drawRectange2(p.x, p.y, p.w, p.h, p.Color,p.dir);
			}
			else if (p.Shape == "circle"){
				this.drawCircle(p.x, p.y, p.r, p.Color, p.Filled);}
			else{
				this.drawCustomImage(images[p.Shape],p.x, p.y,p.dir);
			}

		};
	};

	this.drawCircle = function(x, y, radius, color, fill) {
		var cx = x * width;
		var cy = y * height;
		var r = radius;

		context.beginPath();
		context.arc(cx, cy, r, 0, Math.PI * 2, false);
		context.closePath();

		context.strokeStyle = color;
		context.stroke();

		if (fill) {
			context.fillStyle = color;
			context.fill();
		}

	};

	this.drawRectange = function(x, y, w, h, color,dir) {
		context.beginPath();
		var dx = w * width;
		var dy = h * height;

		context.fillStyle = color;
		var trX=x*width
		var trY=y*height

		context.translate(trX,trY)
		context.rotate(dir);

		context.fillRect(0, -dy*0.5, dx, dy);
		context.rotate(-dir);
		context.translate(-trX,-trY)
	};
	this.drawRectange2 = function(x, y, w, h, color,dir) {
		context.beginPath();
		context.fillStyle = color;
		var trX=x*width
		var trY=y*height
		context.translate(trX,trY)
		context.rotate(dir);
		context.fillRect(-w*0.5, -h*0.5, w, h);
		context.rotate(-dir);
		context.translate(-trX,-trY)
	};
	this.drawCustomImage = function (img, x=0, y=0,dir=0) {
		var trX=x*width
		var trY=y*height
		context.beginPath();
		context.translate(trX,trY);
		context.rotate(dir * Math.PI / 180);
		context.drawImage(img,-img.width*0.5, -img.height*0.5, img.width, img.height);
		context.rotate(-(dir) * Math.PI / 180);
		context.translate(-trX,-trY);
		
		
	};

	this.resetCanvas = function() {
		context.clearRect(0, 0, height, width);
		context.beginPath();
	};
	
};

const Simple_Continuous_Module = function(canvas_height,canvas_width) {
	// Create the element
	// ------------------

	const canvas = document.createElement("canvas");
	Object.assign(canvas, {
		width: canvas_width,
		height: canvas_height,
		style: 'border:1px dotted'
	});
		// Append it to body:
	document.getElementById("elements").appendChild(canvas);

	// Create the context and the drawing controller:
	const context = canvas.getContext("2d");
	const canvasDraw = new ContinuousVisualization(canvas_width, canvas_height, context);

	this.render = function(data) {
		canvasDraw.resetCanvas();
		canvasDraw.draw(data);
	};

	this.reset = function() {
		canvasDraw.resetCanvas();
	};
};
