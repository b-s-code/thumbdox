union() {
	cube(size = [0, 0, 0]);
	color(alpha = 1.0, c = "red") {
		translate(v = [0.0, 0.0, 0]) {
			rotate(a = [0, 0, 0.0]) {
				cube(size = [80.7, 95.25, 4]);
			}
		}
	}
	color(alpha = 1.0, c = "blue") {
		translate(v = [100.0, 100.0, 0]) {
			rotate(a = [0, 0, 45.0]) {
				cube(size = [38.1, 38.1, 4]);
			}
		}
	}
}
