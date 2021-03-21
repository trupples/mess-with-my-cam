"use strict";

let rotx = 0, roty = 0, rotz = 0;

es.addEventListener("doaflip", doaflip);

function doaflip() {
	/*
	let none_played = true;
	do {
		if(Math.random() < .5) {
			rotx += (Math.floor(Math.random() * 2) * 2 - 1) * 360;
			none_played = false;
		}
		if(Math.random() < .5) {
			roty += (Math.floor(Math.random() * 5) - 2) * 180;
			none_played = false;
		}
		if(Math.random() < .5) {
			rotz += (Math.floor(Math.random() * 2) * 2 - 1) * 360;
			none_played = false;
		}
	} while(none_played);*/
	rotx += (Math.floor(Math.random() * 3) - 1) * 360;
	roty += (Math.floor(Math.random() * 5) - 2) * 180;
	rotz += (Math.floor(Math.random() * 3) - 1) * 360;

	video.style.transform = `rotateX(${rotx}deg) rotateY(${roty}deg) rotateZ(${rotz}deg)`;
}

