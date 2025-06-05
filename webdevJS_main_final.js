// Master file for snapping webapp

import { cornerSnap, midpointSnap, lineSnap } from "./webdevJS_utils_final.js";

// Initialise Konva Stage
let stage = new Konva.Stage({
    height: 600,
    width: 600,
    container: "konva-holder",
});

// Initialise and add Konva Layer
let layer = new Konva.Layer({});
stage.add(layer);

// Relative vertices of A
const verticesA = [
    {x: 0, y: 0},
    {x: 120, y: 0},
    {x: 240, y: 100},
    {x: 300, y: 200},
    {x: 300, y: 300},
    {x: 0, y: 300}
]

// Relative vertices of B
var verticesB = [    
    {x: 0, y: 0},
    {x: 100, y: 0},
    {x: 100, y: -50},
    {x: 50, y: -100},
    {x: 0, y: -50}
]

// Create Konva Shape A
let A = new Konva.Line({
    x: 200,
    y: 200,
    stroke: "black",
    fill: "cyan",
    points: verticesA.flatMap(v => [v.x, v.y]),
    closed: true,
    draggable: false,
})

// Create Konva Shape B
let B = new Konva.Line({
    x: 100,
    y: 120,
    stroke: "black",
    fill: "red",
    points: verticesB.flatMap(v => [v.x, v.y]),
    closed: true,
    draggable: true,
});

// Absolute / current vertices of A
const absVerticesA = verticesA.map(v => ({
    x: v.x + A.x(),
    y: v.y + A.y()
}));

// masterSnap function, which controls overarching snapping logic.
function masterSnap() {
    // Absolute / current vertices of B
    const bPos = B.position();
    const absVerticesB = verticesB.map(v => ({
        x: v.x + bPos.x,
        y: v.y + bPos.y
    }));
    
    // Call snapping functions to get 'snapOffset': translation of 'B' onto 'A' for snapping.
    // Each returns 'null' if no viable translation is found.
    let snapOffset = cornerSnap(20, absVerticesA, absVerticesB);
    if (!snapOffset) snapOffset = midpointSnap(15, absVerticesA, absVerticesB);
    if (!snapOffset) snapOffset = lineSnap(10, absVerticesA, absVerticesB);

    // If a viable translation is found, perform translation to snap 'B' to 'A'.
    if (snapOffset) {
        B.position({
            x: bPos.x + snapOffset.dx,
            y: bPos.y + snapOffset.dy
        });
        layer.draw();
    }
}

// Draw layer
layer.add(A); // A is added first so it's below B
layer.add(B);
layer.draw();

B.on('dragmove', masterSnap); // Call masterSnap when 'B' is dragged