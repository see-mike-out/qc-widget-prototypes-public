import CircuitViewer from "./patoka/CircuitViewer.svelte";

export function render({ model, el }) {
	let viewer = new CircuitViewer({ target: el, props: { model } });
	return () => viewer.$destroy();
}
