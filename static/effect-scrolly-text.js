"use strict";

es.addEventListener("scrolly-text", evt => scrollyText(evt.data));

function scrollyText(what) {
	const stx = $("#scrolly-texts");

	const st = document.createElement("div");
	st.classList.add("scrolly-text");
	st.style = `
		font-size: ${Math.random() * 5 + 2}em;
		color: rgb(${Math.random() * 155 + 100}, ${Math.random() * 155 + 100}, ${Math.random() * 155 + 100});
		top: ${Math.random() * 50 + 25}vh;
	`;

	graphemeSplitter.splitGraphemes(what).forEach((c,i) => {
		const s = document.createElement("span");
		s.classList.add("scrolly-char");
		s.style.animationDelay = `${-i*100}ms`;
		s.innerText = c;
		st.appendChild(s);
	});

	stx.appendChild(st);

	setTimeout(_ => stx.removeChild(st), 30000);
}
