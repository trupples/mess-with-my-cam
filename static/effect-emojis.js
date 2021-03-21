"use strict";

es.addEventListener("emojis", evt => emojis(evt.data));

function emojis(what) {
	const ex = $("#emojis");

	graphemeSplitter.splitGraphemes(what).forEach((c,i) => {
		const e = document.createElement("span");
		e.classList.add("emoji");
		e.style.left = `${Math.random() * (WEBCAM_WIDTH - 100)}px`;
		e.style.top = `${Math.random() * (WEBCAM_HEIGHT - 100)}px`;
		const delay = Math.random();
		e.style.animationDelay = `${delay}s`;
		e.innerText = c;
		ex.appendChild(e);
		setTimeout(_ => {
			ex.removeChild(e);
		}, 1000 * (delay + 1));
	});
}
