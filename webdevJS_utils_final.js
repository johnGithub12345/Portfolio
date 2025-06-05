// Utility functions for snapping webapp

/**
 * cornerSnap returns the shortest 'x' and 'y' distance (px) to translate 'B'
 * onto 'A' by snapping one of B's vertices onto one of A's vertices.
 * @param {number} threshold - Maximum acceptable pythagorean distance
 * @param {object} absVerticesA - Absolute positions of A's vertices
 * @param {object} absVerticesB - Absolute positions of B's vertices
 * @returns {object} bestOffset - The shortest 'x' and 'y' distances to translate 'B'
 */
export function cornerSnap(threshold, absVerticesA, absVerticesB) {
    let minDistance = threshold; // Current shortest acceptable distance; threshold by default
    let bestOffset = null; // Current best 'x' and 'y' offsets found

    // Check all pairs, store the closest match within threshold
    for (let vb of absVerticesB) {
        for (let va of absVerticesA) {
            const dx = va.x - vb.x; 
            const dy = va.y - vb.y; 
            const dist = Math.hypot(dx, dy);

            // Update previous best solution if new best found
            if (dist < minDistance) { 
                minDistance = dist; 
                bestOffset = { dx, dy }; 
            }
        }
    }
    return bestOffset;
}

/**
 * midpointSnap returns the shortest 'x' and 'y' distance (px) to translate 'B'
 * onto 'A' by snapping one of B's vertices onto one of A's lines' midpoints.
 * @param {number} threshold - Maximum acceptable pythagorean distance
 * @param {object} absVerticesA - Absolute positions of A's vertices
 * @param {object} absVerticesB - Absolute positions of B's vertices
 * @returns {object} bestOffset - The shortest 'x' and 'y' distances to translate 'B'
 */
export function midpointSnap(threshold, absVerticesA, absVerticesB) {
    let minDistance = threshold; // Current shortest acceptable distance; threshold by default
    let bestOffset = null; // Current best 'x' and 'y' offsets found

    // Calculate A's midpoints
    let midpointsA = []
    for (let i = 0; i < absVerticesA.length; i++) {
        const nextIndex = (i + 1) % absVerticesA.length;
        const dx = Math.round((absVerticesA[nextIndex].x - absVerticesA[i].x) / 2);
        const dy = Math.round((absVerticesA[nextIndex].y - absVerticesA[i].y) / 2);
        const midpoint = {
            x: absVerticesA[i].x + dx,
            y: absVerticesA[i].y + dy
        } // 
        midpointsA.push(midpoint) 
    }

    // Check all B.vertex, A.midpoint pairs, store closest match within threshold
    for (let vb of absVerticesB) {
        for (let ma of midpointsA) {
            const dx = ma.x - vb.x;
            const dy = ma.y - vb.y;
            const dist = Math.hypot(dx, dy); 
            
            // Update previous best solution if new best found
            if (dist < minDistance) {
                minDistance = dist;
                bestOffset = { dx, dy };
            }
        }
    }
    return bestOffset;
}

/**
 * lineSnap returns the shortest 'x' and 'y' distance (px) to translate 'B'
 * onto 'A' by snapping one of B's vertices onto one of A's lines.
 * @param {number} threshold - Maximum acceptable pythagorean distance
 * @param {object} absVerticesA - Absolute positions of A's vertices
 * @param {object} absVerticesB - Absolute positions of B's vertices
 * @returns {object} bestOffset - The shortest 'x' and 'y' distances to translate 'B'
 */
export function lineSnap(threshold, absVerticesA, absVerticesB) {
    let minDistance = threshold; // Current shortest acceptable distance; threshold by default
    let bestOffset = null; // Current best 'x' and 'y' offsets found

    // Check each edge in A
    for (let i = 0; i < absVerticesA.length; i++) {
        const a1 = absVerticesA[i]; // Get i'th vertex in A
        const a2 = absVerticesA[(i + 1) % absVerticesA.length]; 
        // Check each vertex in B
        for (let vb of absVerticesB) {
            // Apply vector projection to find closest point from B.vertex to A.edge
            let A = vb.x - a1.x;
            let Bv = vb.y - a1.y;
            let C = a2.x - a1.x;
            let D = a2.y - a1.y;

            let dot = A * C + Bv * D;
            let len_sq = C * C + D * D;
            let param = -1;
            if (len_sq !== 0) param = dot / len_sq;

            let xx, yy;

            if (param < 0) {
                xx = a1.x;
                yy = a1.y;
            } else if (param > 1) {
                xx = a2.x;
                yy = a2.y;
            } else {
                xx = a1.x + param * C;
                yy = a1.y + param * D;
            }

            const dx = xx - vb.x;
            const dy = yy - vb.y;
            const dist = Math.sqrt(dx * dx + dy * dy);

            // Update previous best solution if new best found
            if (dist < minDistance) {
                minDistance = dist;
                bestOffset = { dx, dy };
            }
        }
    }
    return bestOffset;
}