union() {
	difference() {
		union() {
			cube(size = [0, 0, 0]);
			color(alpha = 1.0, c = "red") {
				translate(v = [0.0, 0.0, 0]) {
					rotate(a = [0, 0, -0.0]) {
						cube(size = [103.7, 118.25, 5]);
					}
				}
			}
			color(alpha = 1.0, c = "red") {
				translate(v = [60.0, 96.5, 0]) {
					rotate(a = [0, 0, -30.0]) {
						cube(size = [56.1, 56.1, 5]);
					}
				}
			}
		}
		union() {
			cube(size = [0, 0, 0]);
			cube(size = [0, 0, 0]);
			translate(v = [4.5, 4.5, -1]) {
				cylinder($fn = 30, h = 15, r = 1.5);
			}
			translate(v = [99, 4.5, -1]) {
				cylinder($fn = 30, h = 15, r = 1.5);
			}
			translate(v = [90, 138, -1]) {
				cylinder($fn = 30, h = 15, r = 1.5);
			}
			translate(v = [4.5, 113.5, -1]) {
				cylinder($fn = 30, h = 15, r = 1.5);
			}
		}
	}
	translate(v = [-10, 0, 0]) {
		mirror(v = [1, 0, 0]) {
			difference() {
				union() {
					cube(size = [0, 0, 0]);
					color(alpha = 1.0, c = "red") {
						translate(v = [0.0, 0.0, 0]) {
							rotate(a = [0, 0, -0.0]) {
								cube(size = [103.7, 118.25, 5]);
							}
						}
					}
					color(alpha = 1.0, c = "red") {
						translate(v = [60.0, 96.5, 0]) {
							rotate(a = [0, 0, -30.0]) {
								cube(size = [56.1, 56.1, 5]);
							}
						}
					}
				}
				union() {
					cube(size = [0, 0, 0]);
					cube(size = [0, 0, 0]);
					translate(v = [4.5, 4.5, -1]) {
						cylinder($fn = 30, h = 15, r = 1.5);
					}
					translate(v = [99, 4.5, -1]) {
						cylinder($fn = 30, h = 15, r = 1.5);
					}
					translate(v = [90, 138, -1]) {
						cylinder($fn = 30, h = 15, r = 1.5);
					}
					translate(v = [4.5, 113.5, -1]) {
						cylinder($fn = 30, h = 15, r = 1.5);
					}
				}
			}
		}
	}
}
