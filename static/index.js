"use strict";

const WEBCAM_WIDTH = 1280;
const WEBCAM_HEIGHT = 720;

const $ = document.querySelector.bind(document);
const graphemeSplitter = new GraphemeSplitter();
const es = new EventSource("/sse");

es.addEventListener("ping", _ => {});
