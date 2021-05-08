function pat() {
	const http = new XMLHttpRequest();
	http.open("GET", "/pat", true);
	http.send(null);
}
