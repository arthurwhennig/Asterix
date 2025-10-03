**Simulator component**

The Simulator.tsx component wraps a CesiumJS viewer which represents
a 3D space model of the Earth. Based on some input data, e.g. an
asteroid's initial position and its force direction towards Earth,
the simulation viewer plays an animation of the moving asteroid and
its impact on Earth based orbital physics. The simulator will
calculate the exact impact on earth based on atmospheric density and
provide the point of impact on the surface of the Earth if the
asteroid hits the surface.
