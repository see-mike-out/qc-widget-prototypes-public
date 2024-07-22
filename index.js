import CircuitViewer from "./patoka/CircuitViewer/CircuitViewer.svelte";
import CircuitWriter from "./patoka/CircuitWriter/CircuitWriter.svelte";
import MachineViewer from "./patoka/MachineViewer/MachineViewer.svelte";
import UncertaintyVis from "./patoka/Uncertainty/UncertaintyVis.svelte";

export function render({ model, el }) {
    if (model.get("mode") === "view") {
    	let view = new CircuitViewer({ target: el, props: { model } });
    	return () => view.$destroy();
    } else if (model.get("mode") === "write") {
    	let view = new CircuitWriter({ target: el, props: { model } });
    	return () => view.$destroy();
    } else if (model.get("mode") === "machine") {
    	let view = new MachineViewer({ target: el, props: { model } });
    	return () => view.$destroy();
    } else if (model.get("mode") === "uncertainty") {
    	let view = new UncertaintyVis({ target: el, props: { model } });
    	return () => view.$destroy();
    }
}
