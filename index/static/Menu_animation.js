"use strict"
			let count = 0;
			function menu_anim () {
				event.preventDefault();
				let menu = document.getElementById("menu");
				let icon = document.getElementById("icon");
				if (count==0) {
					menu.style["animationName"] = "Animation_in";
					menu.style["animationDuration"] = "1s";
					menu.style["left"] = "0";
					icon.style["transition"] = "transform 1.1s";
					icon.style["transform"] = "rotate(90deg)";
					count = 1;
				}
				else {
					menu.style["animationName"] = "Animation_out";
					menu.style["left"] = "-400px"
					icon.style["transform"] = "rotate(0deg)";
					count = 0;
				}
				
					

			}