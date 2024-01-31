document.addEventListener('DOMContentLoaded', function() {
	var homePageButton = document.getElementById('home-page');
	var userPageButton = document.getElementById('user-page');

	if (homePageButton) {
		homePageButton.addEventListener('click', function () {
			window.location.href = '/dashbord.html';
		});
	}
	
	if (userPageButton) {
		userPageButton.addEventListener('click', function() {
			window.location.href = '/user.html';
		});
	}
});
