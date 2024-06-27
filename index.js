import CircuitViewer from "./patoka/CircuitViewer/CircuitViewer.svelte";
import CircuitWriter from "./patoka/CircuitWriter/CircuitWriter.svelte";

export function render({ model, el }) {
    
    if (model.get("mode") === "view") {
    	let view = new CircuitViewer({ target: el, props: { model } });
    	return () => view.$destroy();
    } else if (model.get("mode") === "write") {
    	let view = new CircuitWriter({ target: el, props: { model } });
    	return () => view.$destroy();
    }
}
