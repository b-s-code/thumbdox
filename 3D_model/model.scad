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
}
