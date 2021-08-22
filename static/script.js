let counter = 0;

function pat() {
	const http = new XMLHttpRequest();
	http.open("GET", "/pat", true);
	http.send(null);
	counter++;
	const status = document.getElementById("status")
	const hand = document.getElementById("hand")
	status.classList.remove("hidden")
	hand.classList.remove("hidden")
	setTimeout(() => {
		if (--counter === 0) {
			status.classList.add("hidden");
			hand.classList.add("hidden");
		}
	}, animationDuration);
}
