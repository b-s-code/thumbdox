difference() {
	cube(size = [500, 500, 5]);
	translate(v = [0, 0, -0.5]) {
		union() {
			cube(size = [0, 0, 0]);
			translate(v = [0.0, 0, 0]) {
				cube(size = [14, 14, 6]);
			}
			translate(v = [19.05, 0, 0]) {
				cube(size = [14, 14, 6]);
			}
			translate(v = [38.1, 0, 0]) {
				cube(size = [14, 14, 6]);
			}
			translate(v = [57.150000000000006, 0, 0]) {
				cube(size = [14, 14, 6]);
			}
		}
	}
	translate(v = [0, 19.05, -0.5]) {
		union() {
			cube(size = [0, 0, 0]);
			translate(v = [0.0, 0, 0]) {
				cube(size = [14, 14, 6]);
			}
			translate(v = [19.05, 0, 0]) {
				cube(size = [14, 14, 6]);
			}
			translate(v = [38.1, 0, 0]) {
				cube(size = [14, 14, 6]);
			}
			translate(v = [57.150000000000006, 0, 0]) {
				cube(size = [14, 14, 6]);
			}
		}
	}
	translate(v = [0, 38.1, -0.5]) {
		union() {
			cube(size = [0, 0, 0]);
			translate(v = [0.0, 0, 0]) {
				cube(size = [14, 14, 6]);
			}
			translate(v = [19.05, 0, 0]) {
				cube(size = [14, 14, 6]);
			}
			translate(v = [38.1, 0, 0]) {
				cube(size = [14, 14, 6]);
			}
			translate(v = [57.150000000000006, 0, 0]) {
				cube(size = [14, 14, 6]);
			}
		}
	}
	translate(v = [0, 57.150000000000006, -0.5]) {
		union() {
			cube(size = [0, 0, 0]);
			translate(v = [0.0, 0, 0]) {
				cube(size = [14, 14, 6]);
			}
			translate(v = [19.05, 0, 0]) {
				cube(size = [14, 14, 6]);
			}
			translate(v = [38.1, 0, 0]) {
				cube(size = [14, 14, 6]);
			}
			translate(v = [57.150000000000006, 0, 0]) {
				cube(size = [14, 14, 6]);
			}
		}
	}
	translate(v = [0, 76.2, -0.5]) {
		union() {
			cube(size = [0, 0, 0]);
			translate(v = [0.0, 0, 0]) {
				cube(size = [14, 14, 6]);
			}
			translate(v = [19.05, 0, 0]) {
				cube(size = [14, 14, 6]);
			}
			translate(v = [38.1, 0, 0]) {
				cube(size = [14, 14, 6]);
			}
		}
	}
	translate(v = [100, 100, -0.5]) {
		rotate(a = [0, 0, -45]) {
			translate(v = [0, 0, -0.5]) {
				union() {
					cube(size = [0, 0, 0]);
					translate(v = [0, 0.0, 0]) {
						cube(size = [14, 14, 7]);
					}
					translate(v = [0, 19.05, 0]) {
						cube(size = [14, 14, 7]);
					}
				}
			}
		}
	}
}
